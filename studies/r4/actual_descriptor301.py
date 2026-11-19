"""Actual same-lifecycle model descriptor study. No model/artifact upload.
One original bounded producer attempt; frozen source and original FAILs unchanged.
Projection transformations test descriptor algebra, not transformed-plan validity.
"""
import copy,hashlib,inspect,json,math,os,re,signal,subprocess,sys,tempfile,time,uuid
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import semantic_descriptor301 as c
ROOT=c.ROOT;ENGINE=c.ENGINE
PINS={"app/local_integration/left_right_two_source_binding.py":"9b4c6fa08ba53051cb4f7ffda683d7561a509514","app/reconstruction357/staging400_e1_5_schema_states/guard400.py":"33a4052700d94778abe86af060b3d561865cc746","app/reconstruction357/planha_general150_runtime_work/core_wall_audit118.py":"e2873b155a777e40df866c353db62e47130eee90","app/reconstruction357/planha_general150_runtime_work/private_domain121.py":"d40f622ab05b7d2f6221724db5a6a463bd813db3","studies/r4/semantic_descriptor301.py":"8bdcf838386ea798405b8bc3d43b355fe0957777","app/local_integration/front_rear_runtime_adapter.py":"92ce916b71bb05f0087e2527a51dd8de4d40a676","app/local_integration/same_version_front_rear_contract.py":"0c182a3e26ba48ef6a42df2bf40c2a2ab67c055c","app/local_integration/public_wln_contract.py":"80fd2b2710342735dc35e484c9b0da790995d830","app/local_integration/dimension_contract.py":"058502cd97b5131908b82fdbdba34c62d3376ea3","app/local_integration/program_profile_registry.py":"af549f86f39e2e57554cd48e0ffdea54d5444262","app/local_integration/current_programme_evaluator.py":"99ada55f405e0c205d1a431469d1faae55a149dd","app/local_integration/source_guest_route_evaluator.py":"17fb50e08d153aee4aa2ecd4fa4d13928f522a4e","app/local_integration/source_living_evaluator.py":"2f368ae2a1d5db32d7163076f90eb5a7e991f76f","app/local_integration/source_wall_function_evaluator.py":"84233b6bba2c4835af5e59c203ecf51a6765b8e0","app/local_integration/current_entry_boundary_x03.py":"8383c54d4f6bfd3d94580ede2ab20276b917f414"}
BODY=b'{"W":"18","L":"20","n":2}'
CURRENT=('current_programme_evaluator','source_guest_route_evaluator','source_living_evaluator','source_wall_function_evaluator')
TASK_END=datetime(2026,11,19,19,53,11,tzinfo=timezone.utc)
STAGES={'START','RUNTIME','CURRENT_ASSESS','DESCRIPTOR','NEGATIVES','REVERIFY','WRITE_RECEIPT'}
_STAGE='START'
SAFE_CODES={'RUNTIME_INTEGRITY','ACTUAL_REPLAY','ACTUAL_MODEL_REPORT','CURRENT_INTEGRITY_AUTHORITY','CURRENT_MODEL_STATE','CURRENT_ERROR_OR_MUTATION','PROGRAMME_EVALUATOR_ERROR','PROGRAMME_PHYSICAL_BINDING','PROGRAMME_REPORT_HASH','CURRENT_PHYSICAL_BINDING','CURRENT_SUBREPORT_ERROR','CURRENT_REPLAY_BINDING','ACTUAL_MODULE_INVENTORY','ACTUAL_SOURCE_ROOM_INVENTORY','ACTUAL_DOOR_HOST_CHECK_NOT_PASSED','ACTUAL_SOURCE_ROOM_BINDING','ACTUAL_SOURCE_FIXTURE_BINDING','ACTUAL_SOURCE_WALL_BINDING','ACTUAL_SOURCE_OPENING_BINDING','SOURCE_HASH_BINDING','EXPECTED_CHECK_NOT_ESTABLISHED','CHILD_SOURCE_CHANGED','FINAL_WORKER_SOURCE_CHANGED','DESCRIPTOR_ENGINE_SOURCE_CHANGED','ACTUAL_SOURCE_PIN','CURRENT_MUTATION','FINAL_BUNDLE_MUTATION','FINAL_REPORT_MUTATION','UNCLASSIFIED_STAGE_FAILURE'}
ERROR_TYPES={'ValueError','KeyError','TypeError','IndexError','OSError','RuntimeError','OTHER'}
def need(v,k):c.require(v,k)
def json_types(v):
 if type(v)in(str,int,bool,type(None)):return
 if type(v)is float:
  need(math.isfinite(v),'NONFINITE_JSON');return
 if type(v)is list:
  for x in v:json_types(x)
 elif type(v)is dict:
  need(all(type(k)is str for k in v),'JSON_KEY')
  for x in v.values():json_types(x)
 else:raise ValueError('EXACT_JSON_TYPES')
def digest(v):
 json_types(v)
 return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def guard():
 c.guard()
 for p,pin in PINS.items():
  b=(ROOT/p).read_bytes();need(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==pin,'ACTUAL_SOURCE_PIN')
 need(Path(c.__file__).resolve()==ROOT/'studies/r4/semantic_descriptor301.py','SEMANTIC_IMPORT')
 for fn in(c.digest,c.transform,c.box,c.relation):
  need(Path(inspect.getsourcefile(fn)).resolve()==ROOT/'studies/r4/semantic_descriptor301.py','SEMANTIC_CALLABLE')
 need(Path(__file__).resolve()==ROOT/'studies/r4/actual_descriptor301.py','ACTUAL_SELF_PATH')
 return {'pins':dict(PINS),'self_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
def imports():
 sys.path[:0]=[str(ROOT/'app/local_integration'),str(ENGINE),str(ROOT/'frontend')]
 import front_rear_runtime_adapter as runtime
 import diversity124 as base
 import diversity_multidim126 as multi
 for mod,fn,path in((runtime,'run',ROOT/'app/local_integration/front_rear_runtime_adapter.py'),(base,'describe_model',ENGINE/'diversity124.py'),(multi,'spatial_variants',ENGINE/'diversity_multidim126.py')):
  need(Path(mod.__file__).resolve()==path and Path(inspect.getsourcefile(getattr(mod,fn))).resolve()==path,'ACTUAL_IMPORT')
 return runtime,base
def project(model):
 runtime,_=imports();before=runtime.source_audit()
 import core_wall_audit118,private_domain121
 for mod,name in((core_wall_audit118,'opening_hosts'),(private_domain121,'examine')):
  need(Path(mod.__file__).resolve()==ENGINE/(mod.__name__+'.py')and Path(inspect.getsourcefile(getattr(mod,name))).resolve()==ENGINE/(mod.__name__+'.py'),'DESCRIPTOR_DEPENDENCY_PATH')
 try:
  out=_project(model)
  out['descriptor_engine_source_state_digest']=digest(before)
  out['descriptor_guard_count']=12991
  return out
 finally:
  need(digest(runtime.source_audit())==digest(before),'DESCRIPTOR_ENGINE_SOURCE_CHANGED')
def _project(model):
 guard();_,base=imports();mh=digest(model)
 need(digest(model['inputs'])==digest(['18','20',2]),'ACTUAL_INPUT_SCOPE')
 need(len(model['units'])==2 and {u['id']for u in model['units']}=={'A','B'},'ACTUAL_UNIT_INVENTORY')
 expected=Counter((u,s)for u in('A','B')for s in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118','KITCHEN_MODULE117','BATHROOM_MODULE117'))
 need(Counter((r['unit_id'],r['module']['schema'])for r in model['module_placements'])==expected,'ACTUAL_MODULE_INVENTORY')
 bound=base.describe_model(model) # No fake gate, no describe_candidate.
 need(len(bound['units'])==2,'ACTUAL_DESCRIPTION_UNITS')
 labels={(r['unit'],r['room']):r['functional_label']for r in bound['witness']['source_rooms']}
 need(len(labels)==8,'ACTUAL_SOURCE_ROOM_INVENTORY')
 rows=[]
 for u,bd in zip(model['units'],bound['units']):
  regions={labels[(u['id'],r['room_id'])]:copy.deepcopy(u['rooms'][r['room_id']])for r in model['module_placements']if r['unit_id']==u['id']}
  dp=u['dining_module_placement'];tr=base.transform(dp)
  regions['dining_source_fixtures']=[list(map(str,tr(r)))for r in dp['module']['fixtures'].values()]
  regions.update({'common_stair':[copy.deepcopy(model['common_spaces']['stair'])],
    'common_lift':[copy.deepcopy(model['common_spaces']['lift'])],'common_lobby':copy.deepcopy(model['common_spaces']['lobby'])})
  rows.append({'unit':u['id'],'access':copy.deepcopy(bd['access_edges']),'regions':regions})
 out={'input':copy.deepcopy(model['inputs']),'programme':copy.deepcopy(model['program']),'profile':copy.deepcopy(model['profile']),
  'frame':'ACTUAL_FRONT_REAR_WORLD_XY','model_digest':mh,'units':rows,'source_witness_digest':digest(bound['witness'])}
 need(digest(model)==mh,'MODEL_MUTATED_BY_DESCRIPTOR');guard();return out
def canonical(p):
 variants=[]
 for M in c.D4:
  rows=[]
  for u in p['units']:
   boxes={k:c.transform(c.box(v),{'matrix':M,'translation':['0','0']})for k,v in u['regions'].items()}
   pairs=[[a,b,c.relation(boxes[a],boxes[b])]for a,b in __import__('itertools').combinations(sorted(boxes),2)]
   # Same unit assignment and same global D4 for access AND spatial.
   rows.append({'access':sorted(u['access']),'spatial':pairs})
  variants.append(sorted(rows,key=lambda r:json.dumps(r,sort_keys=True)))
 return min(variants,key=lambda r:json.dumps(r,sort_keys=True))
def descriptor(p):
 return {'schema':'ACTUAL_MODEL_BOUND_DESCRIPTOR301_V1','model_digest':p['model_digest'],
  'projection_digest':digest(p),'signature':digest(canonical(p)),'input_digest':digest(p['input']),
  'programme_digest':digest(p['programme']),'profile_digest':digest(p['profile']),'frame':p['frame'],
  'unit_count':len(p['units']),'region_counts':[len(u['regions'])for u in p['units']],
  'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
  'architectural_diversity_verified':False}
def compare_projections(a,b):
 # Projection-layer contract only; no independent runtime authenticity.
 if any(digest(a[k])!=digest(b[k])for k in('input','programme','profile','frame')):
  return {'state':'NOT_COMPARABLE','architectural_diversity_verified':False}
 same=descriptor(a)['signature']==descriptor(b)['signature']
 return {'state':'EXACT_DESCRIPTOR_EQUIVALENT'if same else'DESCRIPTOR_DIFFERENCE_NOT_QUALITY','architectural_diversity_verified':False}
def projection_checks(p):
 original=digest(p);sig=descriptor(p)['signature'];checks={}
 q=copy.deepcopy(p);q['units'].reverse()
 for u in q['units']:u['unit']='renamed-'+u['unit'];u['access'].reverse()
 checks['opaque_unit_and_order_projection_only']=descriptor(q)['signature']==sig
 q=copy.deepcopy(p)
 for u in q['units']:
  u['regions']={k:[c.transform(r,{'matrix':[[-1,0],[0,1]],'translation':['18','0']})for r in rs]for k,rs in u['regions'].items()}
 checks['global_mirror_projection_only']=descriptor(q)['signature']==sig
 q=copy.deepcopy(p)
 for u in q['units']:u['regions']['kitchen']=[['100','100','103','104']]
 checks['synthetic_organization_difference_only']=descriptor(q)['signature']!=sig
 need(digest(p)==original,'PROJECTION_MUTATION')
 return checks
def actual_negatives(model):
 rows=[];pin=digest(model)
 for kind in('fixture_geometry','opening_reference','module_inventory'):
  q=copy.deepcopy(model)
  if kind=='fixture_geometry':
   u=q['units'][0];k=next(iter(u['fixtures']));u['fixtures'][k][0]=str(c.F(u['fixtures'][k][0])+c.F('1/10'))
  elif kind=='opening_reference':q['openings'][0]['connects'][0]='ORPHAN_REFERENCE'
  else:q['module_placements'].pop()
  try:project(q);rejected=False
  except (ValueError,KeyError,TypeError,IndexError):rejected=True
  rows.append({'kind':kind,'descriptor_binding_rejected':rejected,'geometry_or_quality_rejection_not_claimed':True})
 need(digest(model)==pin,'NEGATIVE_ORIGINAL_MUTATION');return rows
def write(path,value):
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(value,sort_keys=True,allow_nan=False));tmp.replace(path)
def current_report_binding(name,r,bundle):
 mh=bundle['model_digest'];physical=bundle['reports']['physical'];ph=bundle['report_digests']['physical']
 need(r.get('integrity_verified')is True and all(r.get(k)is False for k in('accepted','qualified','display_allowed','delivery_allowed')),'CURRENT_INTEGRITY_AUTHORITY')
 need(r.get('model_digest')==mh and r.get('state')in('PASS','FAIL','UNKNOWN','NOT_EVALUATED'),'CURRENT_MODEL_STATE')
 need(not r.get('report_mutations')and not r.get('integrity_error')and not r.get('missing'),'CURRENT_ERROR_OR_MUTATION')
 if name=='current_programme_evaluator':
  need(not any(x.get('kind')in('EVALUATOR_OR_SOURCE_BINDING_ERROR','INTEGRITY_ERROR')for x in r['findings']),'PROGRAMME_EVALUATOR_ERROR')
  replay=r['reports']['replay']
  need(r['historical_physical_digest']==ph and digest(r['historical_physical_report'])==digest(physical),'PROGRAMME_PHYSICAL_BINDING')
  need(all(digest(v)==r['report_digests'][k]for k,v in r['reports'].items()),'PROGRAMME_REPORT_HASH')
 else:
  replay=r['replay']
  need(r['original_physical_digest']==ph and digest(r['original_physical_report'])==digest(physical),'CURRENT_PHYSICAL_BINDING')
 def error_states(v):
  if type(v)is dict:
   return v.get('state')in('EVALUATOR_ERROR','UNKNOWN_EVALUATOR_OR_BINDING_ERROR')or any(error_states(x)for x in v.values())
  return any(error_states(x)for x in v)if type(v)is list else False
 need(not error_states(r.get('units',[]))and not error_states(r.get('walls',[])),'CURRENT_SUBREPORT_ERROR')
 need(replay['verified']is True and replay['model_hash']==mh,'CURRENT_REPLAY_BINDING')
def check_results(out):
 expected={'opaque_unit_and_order_projection_only','global_mirror_projection_only','synthetic_organization_difference_only'}
 need(set(out['projection_checks'])==expected and all(v is True for v in out['projection_checks'].values()),'PROJECTION_CHECK_SET')
 rows=out['actual_negatives']
 need(type(rows)is list and len(rows)==3 and {r['kind']for r in rows}=={'fixture_geometry','opening_reference','module_inventory'}and all(r['descriptor_binding_rejected']is True for r in rows),'ACTUAL_NEGATIVE_SET')
def child(folder,nonce):
 global _STAGE
 _STAGE='START'
 initial_sources=guard();runtime,_=imports();out={'nonce':nonce,'state':'STARTED','reports':{},'qualified':False}
 write(folder/'observed.json',out)
 _STAGE='RUNTIME'
 bundle=runtime.run(BODY,solver_seconds=30)
 out['bundle']=bundle;write(folder/'observed.json',out)
 bp=digest(bundle)
 need(bundle['completed']is True and bundle['status']=='FULL_REPORTS_RETAINED_NOT_QUALIFIED' and bundle['object_integrity_verified']is True and not bundle.get('report_mutations') and not bundle.get('object_mutations'),'RUNTIME_INTEGRITY')
 need(bundle['model_binding_verified']is True and bundle['reports']['replay']['verified']is True,'ACTUAL_REPLAY')
 model=bundle['packet']['world_model'];mh=digest(model)
 need(bundle['model_digest']==mh and bundle['reports']['physical']['model_hash']==mh,'ACTUAL_MODEL_REPORT')
 _STAGE='CURRENT_ASSESS'
 for name in CURRENT:
  mod=__import__(name);path=ROOT/'app/local_integration'/(name+'.py')
  need(Path(mod.__file__).resolve()==path and Path(inspect.getsourcefile(mod.assess)).resolve()==path,'CURRENT_IMPORT')
  result=mod.assess(bundle)
  out['reports'][name]=copy.deepcopy(result)
  out.setdefault('report_digests',{})[name]=digest(result);write(folder/'observed.json',out)
  need(result['model_digest']==mh and result['state']in('PASS','FAIL','UNKNOWN','NOT_EVALUATED'),'CURRENT_REPORT_STATE_BINDING')
  current_report_binding(name,result,bundle)
  need(digest(bundle)==bp,'CURRENT_MUTATION')
 _STAGE='DESCRIPTOR'
 projection=project(model);out['projection']=projection;out['descriptor']=descriptor(projection)
 _STAGE='NEGATIVES'
 out['projection_checks']=projection_checks(projection);out['actual_negatives']=actual_negatives(model)
 need(all(out['projection_checks'].values())and all(r['descriptor_binding_rejected']for r in out['actual_negatives']),'EXPECTED_CHECK_NOT_ESTABLISHED')
 need(digest(bundle)==bp,'FINAL_BUNDLE_MUTATION')
 need(all(digest(v)==out['report_digests'][k]for k,v in out['reports'].items()),'FINAL_REPORT_MUTATION')
 check_results(out);need(guard()==initial_sources,'CHILD_SOURCE_CHANGED')
 out.update(state='ACTUAL_MODEL_BOUND_DESCRIPTOR',bundle_digest=bp,model_digest=mh,
   report_digests={k:digest(v)for k,v in out['reports'].items()},source_pins=guard())
 write(folder/'observed.json',out)
 # All heavy re-derivation/negative/source verification stays in supervised worker.
 _STAGE='REVERIFY'
 summary=consume(out,nonce)
 need(guard()==initial_sources,'FINAL_WORKER_SOURCE_CHANGED')
 _STAGE='WRITE_RECEIPT'
 summary['observed_file_sha256']=hashlib.sha256((folder/'observed.json').read_bytes()).hexdigest()
 write(folder/'receipt.json',summary)
def consume(out,nonce):
 need(out['nonce']==nonce and out['state']=='ACTUAL_MODEL_BOUND_DESCRIPTOR','CHILD_COMPLETION')
 bundle=out['bundle'];mh=digest(bundle['packet']['world_model'])
 need(digest(bundle)==out['bundle_digest']and mh==out['model_digest']==bundle['model_digest'],'PARENT_BUNDLE_BINDING')
 need(bundle['reports']['replay']['verified']is True and bundle['object_integrity_verified']is True,'PARENT_REPLAY_INTEGRITY')
 check_results(out)
 need(set(out['reports'])==set(CURRENT),'CURRENT_INVENTORY')
 for k,r in out['reports'].items():
  need(digest(r)==out['report_digests'][k]and r['model_digest']==mh,'CURRENT_REPORT_BINDING')
  current_report_binding(k,r,bundle)
 need(digest(project(bundle['packet']['world_model']))==digest(out['projection']),'PARENT_PROJECTION_BINDING')
 need(digest(descriptor(out['projection']))==digest(out['descriptor']),'PARENT_DESCRIPTOR_BINDING')
 need(out['source_pins']==guard(),'PARENT_SOURCE_BINDING')
 return {'schema':'ACTUAL_DESCRIPTOR301_RUN_SUMMARY_V1','state':out['state'],'nonce':nonce,'model_digest':mh,
  'descriptor_digest':digest(out['descriptor']),'descriptor_signature':out['descriptor']['signature'],
  'projection_digest':digest(out['projection']),'report_digests':out['report_digests'],
  'original_report_digests':bundle['report_digests'],'original_physical_status':bundle['reports']['physical']['status'],
  'original_physical_errors':len(bundle['reports']['physical'].get('errors',[])),
  'original_physical_pending':len(bundle['reports']['physical'].get('pending',[])),
  'current_states':{k:r['state']for k,r in out['reports'].items()},
  'original_functional_states':{r['id']:r['state']for r in bundle['reports']['functional']['requirements']},
  'projection_check_count':len(out['projection_checks']),'actual_negative_count':len(out['actual_negatives']),
  'source_digest':digest(guard()),'receipt_verified':True,'qualified':False,'accepted':False,'display_allowed':False,'delivery_allowed':False,
  'durable_raw_archive_created':False,'full_reports_retained_until_temporary_cleanup':True,
  'budget_scope':'All executable source audit/runtime/descriptor/negative/rederive/finalsource work is in supervised child. Parent bounded receipt/bytehash checking is measured against remaining allocation, not preemptively bounded. Final output encoding excluded.',
  'scope':'One actual source-bound descriptor, not a distinct pair or qualification. Original functional report is not the four current reports; both retained separately. Projection mirror/order checks do not approve transformed geometry.'}
def bounded_bytes(path,limit):
 with path.open('rb')as f:data=f.read(limit+1)
 need(len(data)<=limit,'PARENT_BYTE_LIMIT')
 return data
def write_failure(folder,nonce,ex):
 kind=type(ex).__name__
 receipt={'nonce':nonce,'stage':_STAGE,'code':str(ex)if str(ex)in SAFE_CODES else'UNCLASSIFIED_STAGE_FAILURE',
  'error_type':kind if kind in ERROR_TYPES else'OTHER','receipt_verified':False,'qualified':False,
  'request_binding':digest({'body_sha256':hashlib.sha256(BODY).hexdigest(),'nonce':nonce})}
 write(folder/'failure.json',receipt)
def read_failure(folder,nonce):
 r=json.loads(bounded_bytes(folder/'failure.json',8192))
 need(type(r)is dict and set(r)=={'nonce','stage','code','error_type','receipt_verified','qualified','request_binding'},'FAILURE_FIELDS')
 need(r['nonce']==nonce and r['request_binding']==digest({'body_sha256':hashlib.sha256(BODY).hexdigest(),'nonce':nonce}),'FAILURE_NONCE_OR_REQUEST')
 need(all(type(r[k])is str for k in('stage','code','error_type')),'FAILURE_ENUM_TYPES')
 need(r['stage']in STAGES and r['code']in SAFE_CODES and r['error_type']in ERROR_TYPES and r['receipt_verified']is False and r['qualified']is False,'FAILURE_ENUM_AUTHORITY')
 return r
def parent_receipt(folder,nonce,initial_sources):
 payload=bounded_bytes(folder/'receipt.json',65536);summary=json.loads(payload)
 need(type(summary)is dict and summary.get('nonce')==nonce and summary.get('state')=='ACTUAL_MODEL_BOUND_DESCRIPTOR','PARENT_RECEIPT')
 need(summary.get('receipt_verified')is True and all(summary.get(k)is False for k in('accepted','qualified','display_allowed','delivery_allowed')),'PARENT_AUTHORITY')
 need(summary.get('projection_check_count')==3 and type(summary['projection_check_count'])is int and summary.get('actual_negative_count')==3 and type(summary['actual_negative_count'])is int,'PARENT_CHECK_COUNTS')
 need(set(summary.get('current_states',{}))==set(CURRENT),'PARENT_CURRENT_SET')
 need(all(v in('PASS','FAIL','UNKNOWN','NOT_EVALUATED')for v in summary['current_states'].values()),'PARENT_CURRENT_STATES')
 need(summary.get('source_digest')==digest(initial_sources),'PARENT_SOURCE_DIGEST')
 data=bounded_bytes(folder/'observed.json',32*1024*1024)
 need(hashlib.sha256(data).hexdigest()==summary['observed_file_sha256'],'PARENT_FILE_HASH')
 return summary
def run():
 start=time.monotonic();remaining=(TASK_END-datetime.now(timezone.utc)).total_seconds();budget=min(240,remaining-5)
 need(budget>0,'TASK_DEADLINE');initial_sources=guard();nonce=uuid.uuid4().hex
 summary={'state':'NOT_COMPLETED','qualified':False,'accepted':False,'display_allowed':False,'delivery_allowed':False,'receipt_verified':False,'durable_raw_archive_created':False}
 with tempfile.TemporaryDirectory(prefix='descriptor301-')as tmp:
  folder=Path(tmp);proc=None;timed=False
  try:
   need(time.monotonic()-start<budget,'BUDGET_BEFORE_SPAWN')
   proc=subprocess.Popen([sys.executable,'-B',__file__,'--child',str(folder),nonce],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
   try:proc.wait(timeout=max(.001,budget-(time.monotonic()-start)))
   except subprocess.TimeoutExpired:
    timed=True
    try:os.killpg(proc.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    finally:proc.wait()
   if proc.returncode!=0 or timed:raise ValueError('PROCESS_INCOMPLETE_NOT_INFEASIBLE')
   summary=parent_receipt(folder,nonce,initial_sources);need(guard()==initial_sources,'PARENT_SOURCE_CHANGED')
  except Exception as ex:
   summary.update(state='FAILED_CLOSED',receipt_verified=False,error_type=type(ex).__name__)
   failure=folder/'failure.json'
   if failure.exists():
    try:summary['worker_failure']=read_failure(folder,nonce)
    except (OSError,ValueError):summary['worker_failure_unreadable']=True
   p=folder/'observed.json'
   if p.exists():
    try:summary['observed_unverified_file_digest']=hashlib.sha256(bounded_bytes(p,32*1024*1024)).hexdigest()
    except (OSError,ValueError):summary['forensic_bytes_unavailable_or_over_limit']=True
  finally:
   elapsed=time.monotonic()-start
   if elapsed>=budget:summary.update(state='BUDGET_EXHAUSTED',receipt_verified=False)
   summary.update(observed_only=summary.get('receipt_verified')is not True,outer_timeout=timed,elapsed_seconds=elapsed,allocation_seconds=budget,
    wait_completed=proc is not None and proc.poll()is not None,solver_attempt_limit=1,solver_seconds=30,full_model_uploaded=False)
 print(json.dumps(summary,sort_keys=True),flush=True)
 need(summary.get('receipt_verified')is True,'DESCRIPTOR_RUN_NOT_VERIFIED')
if __name__=='__main__':
 if len(sys.argv)==4 and sys.argv[1]=='--child':
  try:child(Path(sys.argv[2]),sys.argv[3])
  except Exception as ex:
   write_failure(Path(sys.argv[2]),sys.argv[3],ex)
   raise SystemExit(1)
 elif len(sys.argv)==1:run()
 else:raise ValueError('CLI_ARGUMENTS')
