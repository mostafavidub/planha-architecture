"""Read-only HTTP exercise of current loopback product path; no mocks or product edits.
Fifty seeded integer lots and a separate existing 18x20 control. No raw plan output.
"""
import hashlib,http.client,inspect,json,os,random,re,sys,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
PINS={"app/local_integration/automatic_program_search.py":"686e29e65384a8b6990cbb65b63050ca6aef4208","app/local_integration/public_wln_contract.py":"80fd2b2710342735dc35e484c9b0da790995d830","app/local_integration/public_input_errors403.py":"4dba239c1484c6eda7985cde0b590680ec9ed3f3","app/local_integration/live_program_scheduler.py":"1b671b6632d01c1012fcb39b2c33e731fb619fbc","app/local_integration/http_withholding_x04.py":"d2237f58367ccec40699e581632883bb5d95815d","app/local_integration/http_evidence_x07.py":"b23153874b7a4b2f10f170afcd38c6d4238cb852","app/local_integration/public_wln_server.py":"da45aa429bf055ec021e3e4110024b05a85ae49c","app/local_integration/current_entry_launch_x03.py":"771efe4180d03eb420e926b7c070f22937e31685"}
EXPECTED_CASES='f92f4f89fdb83c823a01ab582810c458dd8cea111627cf5a6074b0eaa3e5ef03'
BASELINE='84022bd9ea5c3876a72911ed4dc1544d90957c67'
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def need(ok,code):
 if not ok:raise ValueError(code)
def sha(b):return hashlib.sha256(b).hexdigest()
def compact(x):return json.dumps(x,separators=(',',':'),allow_nan=False).encode()
def emit(value):print(json.dumps(value,sort_keys=True,allow_nan=False),flush=True)
def source():
 for name,pin in PINS.items():
  b=(ROOT/name).read_bytes()
  need(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==pin,'PRODUCT_PIN_CHANGED')
 files=list((ROOT/'app/local_integration').rglob('*.py'))
 engine=ROOT/'app/reconstruction357/planha_general150_runtime_work'
 files+=list(engine.glob('*.py'))+list(engine.glob('*.json'))+[p for p in(engine/'references').rglob('*')if p.is_file()]
 rows={str(p.relative_to(ROOT)):sha(p.read_bytes())for p in sorted(set(files))}
 return {'source_file_count':len(rows),'source_manifest_digest':sha(compact(rows))}
def enum(value):
 return value if type(value)is str and re.fullmatch('[A-Z0-9_]+',value)else None
def hexid(value):
 return value if type(value)is str and re.fullmatch('[0-9a-f]{32}|[0-9a-f]{64}',value)else None
def count(value):return value if type(value)is int and value>=0 else None
def boolean(value):return value if type(value)is bool else None
def projection(data,status):
 need(type(data)is dict,'RESPONSE_OBJECT')
 life=data.get('http_lifecycle',{});binding=data.get('full_evidence_binding',{});decision=data.get('decision',{})
 need(all(type(x)is dict for x in(life,binding,decision)),'RESPONSE_SECTIONS')
 state=enum(data.get('status'));code=enum(data.get('code'))
 stage='PREFLIGHT_UNSUPPORTED'if status==409 and state=='UNSUPPORTED_SELECTED_SAME_VERSION_CASE'else'DEADLINE_WITHHELD'if status==504 else'HTTP_COMPLETED'if status==200 else'HTTP_ERROR_OR_OTHER_REJECTION'
 return {'http_status':status,'stage':stage,'status':state,'code':code,'input_valid':boolean(data.get('input_valid')),
  'plan_count_available':count(data.get('plan_count_available')),'qualified_count':count(data.get('qualified_count')),
  'qualified_count_evidence':'EXPLICIT_FIELD'if count(data.get('qualified_count'))is not None else'NOT_REPORTED',
  'actual_live_attempts':count(data.get('actual_live_attempts')),'fresh_model_executed':boolean(data.get('fresh_model_executed')),
  'attempt_states':[enum(x)for x in data.get('attempt_states',[])],'decision_state':enum(decision.get('state')),
  'decision_blockers':[enum(x)for x in decision.get('blockers',[])],
  'source_integrity_verified':boolean(data.get('source_integrity_verified')),
  'request_id':hexid(life.get('request_id',data.get('request_id'))),'request_digest':hexid(life.get('request_digest')),
  'nonce_digest':hexid(binding.get('nonce_digest')),'model_digest':hexid(binding.get('model_digest')),
  'evidence_source_digest':hexid(binding.get('source_digest')),'file_hashes_digest':hexid(binding.get('file_hashes_digest')),
  'full_evidence_state':enum(binding.get('state')),'full_evidence_binding_verified':boolean(binding.get('binding_verified')),
  'http_receipt_verified':boolean(life.get('receipt_verified',data.get('receipt_verified'))),
  'authority_flags':{k:boolean(data.get(k))for k in AUTH},'response_bytes_digest':None,
  'scope':'Observed current HTTP response only; unavailable counts are not inferred from authority flags or booleans.'}
def post(port,w,l,index,kind):
 body=compact({'W':str(w),'L':str(l),'n':2});start=time.monotonic()
 row={'index':index,'kind':kind,'input':{'W':w,'L':l,'n':2},'body_digest':sha(body),'attempted_http_posts':1}
 conn=http.client.HTTPConnection('127.0.0.1',port,timeout=190 if kind=='CONTROL'else 20)
 try:
  conn.request('POST','/api/public/plan',body=body,headers={'Content-Type':'application/json'})
  response=conn.getresponse();row['received_http_status']=response.status;row['http_status']=response.status
  payload=response.read(1024*1024+1);row['response_bytes_digest']=sha(payload);need(len(payload)<=1024*1024,'RESPONSE_BYTE_LIMIT')
  def reject(value):raise ValueError('RESPONSE_NONFINITE')
  def unique(pairs):
   out={}
   for key,value in pairs:need(key not in out,'RESPONSE_DUPLICATE');out[key]=value
   return out
  data=json.loads(payload,parse_constant=reject,object_pairs_hook=unique)
  row.update(projection(data,response.status));row['response_bytes_digest']=sha(payload);row['response_contract_valid']=True
 except Exception as ex:row.update(stage='RESPONSE_CONTRACT_ERROR'if 'received_http_status'in row else'TRANSPORT_ERROR',exception_type=type(ex).__name__,http_status=row.get('received_http_status'),response_contract_valid=False)
 finally:conn.close()
 row['elapsed_seconds']=time.monotonic()-start;emit({'schema':'PUBLIC50_CASE_V1',**row});return row
def main():
 start=time.monotonic();pairs=random.Random(20261119).sample([(w,l)for w in range(5,26)for l in range(5,26)],50)
 need(len(set(pairs))==50 and(18,20)not in pairs and sha(compact(pairs))==EXPECTED_CASES,'CASE_PREREGISTRATION_MISMATCH')
 before=source()
 import current_entry_launch_x03 as launch,public_wln_server as product
 need(Path(inspect.getsourcefile(launch.server)).resolve()==ROOT/'app/local_integration/current_entry_launch_x03.py','LAUNCH_IMPORT_PATH')
 server=launch.server('PUBLIC_WLN_18X20',0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 emit({'schema':'PUBLIC50_PREREGISTERED_V1','product_baseline':BASELINE,'execution_commit':os.environ.get('GITHUB_SHA'),
  'seed':20261119,'case_list_digest':EXPECTED_CASES,'random_case_count':50,'control_count':1,'n':2,
  'requested_count_sent':False,'random_sample_is_unbiased_quality_validation':False,**before,
  'budget_scope':'Unchanged server X04 response cutoff180s and scheduler child180s/solver30; HTTP client190s waiting is not a new runtime budget. Workflow8min external test cap.'})
 rows=[]
 try:
  for i,(w,l)in enumerate(pairs,1):rows.append(post(server.server_port,w,l,i,'SEEDED_RANDOM'))
  control=post(server.server_port,18,20,51,'CONTROL')
  # Do not cancel a worker when its response is withheld. Observe existing lock release.
  cleanup_start=time.monotonic()
  while product.LOCK.locked()and time.monotonic()-cleanup_start<30:time.sleep(.1)
  after=source();unchanged=after==before
  summary={'schema':'PUBLIC50_COLLECTION_V1','case_list_digest':EXPECTED_CASES,'random_rows':len(rows),
   'random_http_status_counts':{str(k):sum(r.get('http_status')==k for r in rows)for k in sorted({r.get('http_status')for r in rows},key=str)},
   'random_preflight_unsupported':sum(r.get('stage')=='PREFLIGHT_UNSUPPORTED'for r in rows),
   'random_response_available_count_sum':sum(r['plan_count_available']for r in rows if type(r.get('plan_count_available'))is int),
   'random_available_count_missing':sum(type(r.get('plan_count_available'))is not int for r in rows),
   'control':control,'control_complete_receipt_observed':control.get('http_status')==200 and control.get('full_evidence_binding_verified')is True,'product_sources_unchanged':unchanged,'source_after':after,'worker_lock_released':not product.LOCK.locked(),
   'total_seconds':time.monotonic()-start,'raw_models_logged':False,'artifact_upload':False,'durable_raw_archive':False,
   'current_product_qualified':False,'scope':'Fifty real public POSTs plus one separately labelled existing-case control; rejection is not infeasibility.'}
  emit(summary);need(unchanged,'PRODUCT_SOURCE_CHANGED')
  need(len(rows)==50 and all(r.get('response_contract_valid')is True for r in rows)and control.get('response_contract_valid')is True,'HTTP_COLLECTION_INCOMPLETE')
 finally:server.shutdown();server.server_close();thread.join(timeout=5)
if __name__=='__main__':main()
