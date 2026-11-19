"""X04 HTTP withholding only. No scheduler budget change, cancellation or recovery."""
import copy,hashlib,json,math,threading,time,uuid
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
    raw=run(body)
    # Retain only bounded public projection in this in-memory boundary, not raw model.
    summary=project(raw);payload=encoded(summary)
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
     box['payload']=payload
   except Exception:
    with self._mutex:record['worker_state']='WORKER_FAILED_OBSERVED'
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
