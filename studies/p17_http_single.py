"""One actual n1 HTTP call. Only metadata/counts/digests leave temporary runtime."""
import hashlib,http.client,json,sys,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
from current_entry_launch_x03 import server
def main():
 start=time.monotonic();s=server('PUBLIC_WLN_18X20');t=threading.Thread(target=s.serve_forever,daemon=True);t.start()
 source=ROOT/'app/local_integration/live_program_scheduler.py';pin=hashlib.sha256(source.read_bytes()).hexdigest()
 out={'scope':'One actual same-family n1 API construction/replay/full evaluation; not qualified/P25/durable archive','request':{'W':'18','L':'20','n':1},'attempt_limit':1,'retry':False}
 try:
  c=http.client.HTTPConnection('127.0.0.1',s.server_port,timeout=190)
  c.request('POST','/api/public/plan',b'{"W":"18","L":"20","n":1}',{'Content-Type':'application/json'})
  response=c.getresponse();raw=response.read();c.close();data=json.loads(raw)
  out.update(http_status=response.status,response=data,response_byte_sha256=hashlib.sha256(raw).hexdigest())
  assert response.status==200 and data['schema']=='PUBLIC_WLN_STUDY_SUMMARY_V1'
  assert data['actual_live_attempts']==1 and data['fresh_model_executed']is True
  assert data['source_integrity_verified']is True and data['full_evidence_binding']['binding_verified']is True
  assert data['decision']['state']=='BLOCKED' and 'P25_DELIVERY_NOT_IMPLEMENTED'in data['decision']['blockers']
  assert data['single_unit_evidence'][0]['receipt_verified']is True
  assert len(data['single_unit_evidence'][0]['current_states'])==4
  assert all(data[k]is False for k in ('accepted','qualified','display_allowed','delivery_allowed'))
  out['actual_http_chain_complete']=True
 except Exception as ex:
  out.update(actual_http_chain_complete=False,error_type=type(ex).__name__)
 finally:
  import public_wln_server as service
  expected=hashlib.sha256(b'{"W":"18","L":"20","n":1}').hexdigest()
  rid=out.get('response',{}).get('request_id',out.get('response',{}).get('http_lifecycle',{}).get('request_id'))
  records=[r for r in service.HTTP_BOUNDARY.snapshot()if r['request_id']==rid and r['request_digest']==expected]
  out['private_boundary_observation']=records[0]if len(records)==1 else {'state':'NOT_BOUND_NOT_REPORTED'}
  s.shutdown();s.server_close();t.join(timeout=5)
  out.update(elapsed_seconds=time.monotonic()-start,old_pair_scheduler_unchanged=hashlib.sha256(source.read_bytes()).hexdigest()==pin,raw_archive_durable=False)
  print(json.dumps(out,sort_keys=True,ensure_ascii=False),flush=True)
 return 0 if out['actual_http_chain_complete'] and out['old_pair_scheduler_unchanged'] else 1
if __name__=='__main__':raise SystemExit(main())
