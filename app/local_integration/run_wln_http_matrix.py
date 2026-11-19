"""Task5.2 real nonready loopback HTTP matrix plus separately reused actual UI witness.
No new solver execution; subprocess denial is a test-harness guard, not product policy.
"""
import copy,hashlib,json,pathlib,sys,threading,urllib.request,urllib.error
from public_wln_server import server,public_summary
from public_wln_contract import parse_public
from live_program_scheduler import bind_completed
from same_version_front_rear_contract import digest,ENGINE_REVISION
from validate_wln_preregistration import validate
ROOT=pathlib.Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
SPEC_SHA='48a618b9bfc0b1f2ab015a4845ce7899fbc48b1e601a266a5852c98d3ff0732d'
def one(root,name):
 fs=list(root.rglob(name));assert len(fs)==1,(name,len(fs));return json.loads(fs[0].read_text())
def source_compatible(runtime,scheduler):
 pins={}
 for snap in (runtime['source_snapshot'],scheduler['source_snapshot']):
  for p,h in snap.items():
   assert p not in pins or pins[p]==h
   assert '..' not in pathlib.Path(p).parts and (ROOT/p).resolve().is_relative_to(ROOT.resolve())
   assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h;pins[p]=h
 # Same byte-revision calculation as frozen engine114.revision without importing solver.
 files=[*ENGINE.glob('*.py'),*ENGINE.glob('*.json'),*(p for p in (ENGINE/'references').rglob('*') if p.is_file())]
 revision=digest({str(p.relative_to(ENGINE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)})
 assert revision==runtime['engine_revision']==ENGINE_REVISION
 return {'integration_source_hashes':pins,'engine_revision':revision,'engine_files_hashed':len(files),'scope':'Read-only current byte compatibility with retained runtime; no new replay, geometry or solver execution'}
def main(evidence_root):
 path=ROOT/'specs/V25_TASK_5_1_WLN_MATRIX_PREREGISTRATION.json'
 assert hashlib.sha256(path.read_bytes()).hexdigest()==SPEC_SHA
 validation=validate(path);spec=json.loads(path.read_text())
 browser=one(evidence_root,'browser-receipt.json');runtime=one(evidence_root,'runtime-bundle.json')
 request=one(evidence_root,'request.json');child=one(evidence_root,'child-complete.json');scheduler=one(evidence_root,'scheduler.json');decision=one(evidence_root,'decision.json')
 assert browser['schema']=='PUBLIC_THREE_FIELD_BROWSER_EVIDENCE_V1'
 bind_completed(child,request,runtime,decision)
 assert scheduler['attempts'][0]['receipt_verified'] is True and scheduler['attempts'][0]['runtime_digest']==digest(runtime)
 assert scheduler['attempts'][0]['decision_digest']==digest(decision)
 assert digest(browser['actual_response'])==digest(public_summary(scheduler))
 assert digest(browser['actual_request'])==digest(json.loads(bytes.fromhex(request['body_hex'])))
 expected=next(c for c in spec['cases'] if c['id']=='SUPPORTED_18_20')
 assert digest(parse_public(bytes.fromhex(request['body_hex']))['canonical_request'])==digest(parse_public(expected['body'].encode())['canonical_request'])
 assert browser['actual_response']['fresh_model_executed'] is True and browser['actual_response']['decision']['state']=='BLOCKED'
 assert all(browser['actual_response'][k] is False for k in AUTH)
 compatibility=source_compatible(runtime,scheduler)
 attempts=[]
 def audit(event,args):
  if event=='subprocess.Popen':
   attempts.append(event);raise RuntimeError('MATRIX_TEST_HARNESS_FORBIDS_NEW_GENERATION_SUBPROCESS')
 sys.addaudithook(audit)
 s=server(0);thread=threading.Thread(target=s.serve_forever,daemon=True);thread.start()
 url='http://127.0.0.1:'+str(s.server_address[1])+'/api/public/plan'
 rows=[]
 try:
  for case in spec['cases']:
   e=case['expected']
   if e['execution_ready']:
    rows.append({'id':case['id'],'execution':'NOT_POSTED_NO_NEW_SOLVER','evidence':'REUSED_ACTUAL_SELECTED_CASE_WITNESS' if case['id']=='SUPPORTED_18_20' else 'PREFLIGHT_CANONICAL_EQUIVALENCE_ONLY_NOT_NEW_HTTP_OR_GENERATION'})
    continue
   req=urllib.request.Request(url,data=case['body'].encode(),headers={'Content-Type':'application/json'},method='POST')
   try:
    with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req,timeout=5) as r:status=r.status;response=json.loads(r.read())
   except urllib.error.HTTPError as ex:status=ex.code;response=json.loads(ex.read())
   assert status==e['http_status'],(case['id'],status,response)
   assert response.get('status',response.get('code'))==e['state_or_code'],(case['id'],response)
   assert all(response.get(k) is False for k in AUTH)
   if e['input_valid']:
    assert response['input_valid'] is True and response['fresh_model_executed'] is False and response['actual_live_attempts']==0
    assert response['plan_count_available']==0 and response['plan_payload'] is None and response['download_available'] is False
   assert not any(k in response for k in ('world_model','packet','svg','dxf','routes'))
   rows.append({'id':case['id'],'execution':'REAL_LOOPBACK_HTTP','status':status,'response':response})
 finally:s.shutdown();s.server_close();thread.join(timeout=5)
 assert not thread.is_alive() and attempts==[]
 assert hashlib.sha256(path.read_bytes()).hexdigest()==SPEC_SHA
 assert source_compatible(runtime,scheduler)==compatibility
 # Recheck all five preregistered API/source blobs after HTTP, without dispatch.
 assert validate(path)['spec_sha256']==SPEC_SHA
 assert len([r for r in rows if r['execution']=='REAL_LOOPBACK_HTTP'])==26
 assert not (ROOT/'live-program-evidence').exists(),'Unexpected new runtime directory'
 out={'schema':'TASK5_2_ACTUAL_HTTP_MATRIX_V1','spec_sha256':SPEC_SHA,'rows':rows,'actual_new_http_posts':26,
  'ready_cases_not_posted':2,'fresh_geometry_executed':False,'new_solver_calls':0,'subprocess_attempts':attempts,
  'subprocess_guard_scope':'Temporary negative-test Popen hook only, not a universal in-process solver ban. Zero new solver follows the real nonready/no-dispatch branch and actual_live_attempts0; production server unchanged',
  'reused_supported_witness':{'source_run':44462498782,'source_artifact':14500313851,'source_artifact_sha256':'fcbfe269bf8189882145b85570625c7f3f40491cc1296d19ecf53c357fbcb02b','request':browser['actual_request'],'public_response':browser['actual_response'],'browser_receipt_digest':digest(browser),'runtime_digest':digest(runtime),'decision_digest':digest(decision),'compatibility':compatibility,
   'scope':'Previous actual browser/public POST and fresh runtime witness reused; not a new positive plan or fresh full matrix'},
  'scope':'Current three-field API distinguishes valid-but-unsupported and rejected wire inputs. Geometry generation across variable dimensions remains unimplemented/unverified.',
  **{k:False for k in AUTH}}
 pathlib.Path('actual-http-matrix.json').write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True))
if __name__=='__main__':main(pathlib.Path(sys.argv[1]))
