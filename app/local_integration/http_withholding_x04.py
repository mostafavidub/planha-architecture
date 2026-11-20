"""X04 HTTP withholding only. No scheduler budget change, cancellation or recovery."""
import copy,hashlib,json,math,re,threading,time,uuid
from collections import deque
LIMIT_SECONDS=180.0
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def encoded(value):
 return json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()
def digest(value):return hashlib.sha256(encoded(value)).hexdigest()
def denied(code,request_id,generation_started):
 return {'schema':'HTTP_WITHHOLDING_X04_V1','code':code,'request_id':request_id,
  'generation_started':generation_started,'evidence_usable':False,'receipt_verified':False,
  'plan_count_available':0,'plan_payload':None,'download_available':False,
  'cancelled':False,'deadline_preemption':False,'durable_record':False,**{k:False for k in AUTH}}
def diagnostic_record(value,request_digest):
 # Private bounded observation only; never modifies the HTTP decision or authority.
 if type(value)is not dict or value.get('schema')!='P17_PRIVATE_DIAGNOSTIC_V1':return {'state':'NOT_REPORTED'}
 if value.get('request_digest')!=request_digest:return {'state':'REQUEST_MISMATCH_REJECTED'}
 out={'state':'OBSERVED_UNVERIFIED','schema':value['schema'],'request_digest':request_digest,
      'evidence_usable':False,'receipt_verified':False,'raw_archive_durable':False}
 for key in ('parent_stage','worker_stage','worker_state','error_code'):
  v=value.get(key);out[key]=v if type(v)is str and re.fullmatch(r'[A-Z][A-Z0-9_]{0,95}',v)else None
 v=value.get('error_type')
 out['error_type']=v if type(v)is str and v in ('ValueError','KeyError','TypeError','AssertionError','OSError','FileNotFoundError','RecursionError','RuntimeError','JSONDecodeError')else 'UNREPORTED_EXCEPTION_TYPE'
 for key,size in (('runtime_nonce',32),('observed_model_digest',64)):
  v=value.get(key);out[key]=v if type(v)is str and re.fullmatch('[0-9a-f]{'+str(size)+'}',v)else None
 for key in ('source_integrity_observed','within_budget_observed'):out[key]=value.get(key)is True
 files=value.get('observed_file_hashes');out['observed_file_hashes']={}
 if type(files)is dict:
  for key in ('request','summary','bundle','current','decision','originals','proposal','model','negatives'):
   v=files.get(key)
   if type(v)is str and re.fullmatch(r'[0-9a-f]{64}',v):out['observed_file_hashes'][key]=v
 return out
class Boundary:
 def __init__(self):
  self._mutex=threading.Lock();self._records=deque(maxlen=64)
 def snapshot(self):
  with self._mutex:return copy.deepcopy(list(self._records))
 def execute(self,body,*,accepted_at,lock,run,project):
  # Called with the existing server lock held. Only worker owns release after spawn.
  limit=LIMIT_SECONDS
  if type(limit) not in (int,float) or not math.isfinite(limit) or not 0<limit<=180:
   lock.release();raise ValueError('INTERNAL_HTTP_LIMIT')
  request_id=uuid.uuid4().hex;deadline=accepted_at+limit;event=threading.Event();box={}
  record={'schema':'HTTP_WITHHOLDING_RECORD_X04_V1','request_id':request_id,
   'request_digest':hashlib.sha256(body).hexdigest(),'accepted_at':accepted_at,'deadline':deadline,
   'worker_state':'NOT_STARTED','response_state':'PENDING','generation_started':False,
   'receipt_verified':False,'evidence_usable':False,'durable_record':False}
  with self._mutex:self._records.append(record)
  def reject(code):
   return 504,denied(code,request_id,record['generation_started'])
  if time.monotonic()>=deadline:
   with self._mutex:record.update(worker_state='NOT_STARTED_DEADLINE',response_state='WITHHELD')
   lock.release();return reject('DEADLINE_EXCEEDED_BEFORE_DISPATCH')
  def worker():
   try:
    if time.monotonic()>=deadline:
     with self._mutex:record['worker_state']='NOT_STARTED_DEADLINE'
     return
    with self._mutex:record.update(worker_state='RUNNING',generation_started=True)
    with self._mutex:record['boundary_stage']='RUN'
    raw=run(body)
    with self._mutex:record['runtime_diagnostic']=diagnostic_record(raw.get('http_diagnostic'),record['request_digest'])
    # Retain only bounded public projection in this in-memory boundary, not raw model.
    with self._mutex:record['boundary_stage']='PROJECT'
    summary=project(raw)
    rows=raw.get('attempts',[])
    receipts_observed=type(rows)is list and len(rows)>0 and all(type(r)is dict and r.get('receipt_verified')is True for r in rows)
    if not receipts_observed:
     summary=copy.deepcopy(summary);summary['decision']={'state':'NO_VERIFIED_DECISION','blockers':['RUNTIME_RECEIPT_NOT_VERIFIED']}
    payload=encoded(summary)
    if len(payload)>1024*1024:raise ValueError('SUMMARY_LIMIT')
    rows=raw.get('attempts',[])
    observed={'source_integrity_observed':raw.get('source_integrity_verified') is True,
     'attempt_count_observed':len(rows) if type(rows)is list else None,
     'runtime_identity_digest':digest([{'nonce':r.get('nonce'),'runtime_digest':r.get('runtime_digest'),'model_digest':r.get('model_digest'),'receipt_verified':r.get('receipt_verified')} for r in rows]) if type(rows)is list and all(type(r)is dict for r in rows) else None,
     'summary_digest':hashlib.sha256(payload).hexdigest()}
    with self._mutex:
     record.update(observed)
     record['worker_state']='COMPLETED_OBSERVED'
     # Source failure remains observed failure; no decision is promoted to verified.
     if not observed['source_integrity_observed']:record['worker_state']='SOURCE_UNVERIFIED_OBSERVED'
     if observed['source_integrity_observed']:box['payload']=payload
   except Exception as ex:
    with self._mutex:
     record['worker_state']='WORKER_FAILED_OBSERVED'
     record['boundary_error']=diagnostic_record({'schema':'P17_PRIVATE_DIAGNOSTIC_V1','request_digest':record['request_digest'],'parent_stage':record.get('boundary_stage'),'error_type':type(ex).__name__,'error_code':str(ex)},record['request_digest'])
     if 'runtime_diagnostic'not in record:record['runtime_diagnostic']=diagnostic_record(getattr(ex,'http_diagnostic',None),record['request_digest'])
   finally:
    with self._mutex:
     record['finished_at']=time.monotonic()
     if record['finished_at']>=deadline or record['response_state']=='WITHHELD':
      record['worker_state']='LATE_'+record['worker_state'];box.clear()
     record['elapsed_seconds']=record['finished_at']-accepted_at
    lock.release()
    event.set()
  thread=threading.Thread(target=worker,daemon=False)
  try:thread.start()
  except Exception:
   with self._mutex:record.update(worker_state='THREAD_START_FAILED',response_state='ERROR')
   lock.release();return 500,denied('HTTP_WORKER_START_FAILED',request_id,False)
  event.wait(max(0,deadline-time.monotonic()))
  with self._mutex:
   if not event.is_set() or time.monotonic()>=deadline:
    record['response_state']='WITHHELD';box.clear()
    return reject('DEADLINE_EXCEEDED_RESULT_WITHHELD')
   if 'payload' not in box:
    record['response_state']='ERROR'
    return 500,denied('STUDY_FAILED_CLOSED',request_id,record['generation_started'])
   payload=box.pop('payload')
   out=json.loads(payload)
   out['http_lifecycle']={'schema':'HTTP_WITHHOLDING_X04_V1','request_id':request_id,
    'request_digest':record['request_digest'],'response_state':'ON_TIME_OBSERVED',
    'evidence_usable':False,'receipt_verified':False,'durable_record':False,
    'budget_scope':'Clock before input preflight through worker projection and serialization; final response encoding/network outside cutoff. No preemption/cancellation.',
    'summary_digest':record['summary_digest']}
   # Final lightweight assembly is also measured; never reset at completion.
   if time.monotonic()>=deadline:
    record['response_state']='WITHHELD';return reject('DEADLINE_EXCEEDED_RESULT_WITHHELD')
   record['response_state']='ON_TIME_OBSERVED'
   return 200,out
