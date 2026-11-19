"""R4-1.08 targeted counterexample proof; no admission or natural-failure claim."""
import hashlib,inspect,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'studies/r4')]
from same_version_front_rear_contract import digest
from source_fit_profile207 import profiles,source_check
PINS={'app/reconstruction357/planha_general150_runtime_work/search114.py':'65e0f278c9f9ef480388d3ea8056161c0a938a36',
 'app/local_integration/cause_directed_candidate108.py':'5851a0e98162776ca292b40a5707d0ef8f477c8b',
 'app/local_integration/cause_directed_contract108.py':'f07e20e250199a51fce9a9042ea854258345310f',
 'studies/r4/actual_descriptor301.py':'02c3126479b9fee410d985afb7e58205bb55c0b3',
 'studies/r4/semantic_descriptor301.py':'8bdcf838386ea798405b8bc3d43b355fe0957777'}
PINS.update({'app/reconstruction357/planha_general150_runtime_work/entry117.py':'56483ecd624dee7fddca5097ba284f8689bcfd9c',"app/reconstruction357/planha_general150_runtime_work/assemble114.py":"6e19b12c62820e015055765e0fe56d6339cd4312","app/reconstruction357/planha_general150_runtime_work/public_witness118.py":"36f49057da712f29953bbc940a0dd8e9285ee64b","app/local_integration/cause_regression_support108.py":"343758e578800ee3aa26c61629e9e80a79705af1"})
def need(ok,code):
 if not ok:raise ValueError(code)
def source_guard():
 for name,pin in PINS.items():
  b=(ROOT/name).read_bytes()
  need(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==pin,'PLANNED_SOURCE_PIN')
 import search114,planned_witness_contract108 as c,compound_panel_candidate108 as panel
 for fn,path in ((search114.propose,ENGINE/'search114.py'),(c.diagnose,ROOT/'app/local_integration/planned_witness_contract108.py'),(panel.propose,ROOT/'app/local_integration/compound_panel_candidate108.py')):
  need(Path(inspect.getsourcefile(fn)).resolve()==path,'PLANNED_SOURCE_PATH')
 need(strip_panel_source((ROOT/'app/local_integration/compound_panel_candidate108.py').read_text())[0]==(ROOT/'app/local_integration/cause_directed_candidate108.py').read_text(),'PANEL_ORIGINAL_SOURCE_CHANGED')
 source_check()
 return True

def bind_current(name,report,evidence):
 import actual_descriptor301 as a
 need(Path(inspect.getsourcefile(a.current_report_binding)).resolve()==ROOT/'studies/r4/actual_descriptor301.py','CURRENT_BINDER_PATH')
 a.current_report_binding(name,report,evidence)

def readback(folder,result):
 """Data consistency only, no replay/evaluator/solver execution."""
 import json,math
 def read(path):
  with path.open('rb')as f:data=f.read(96*1024*1024+1)
  need(len(data)<=96*1024*1024,'READBACK_BYTE_LIMIT')
  def bad(value):raise ValueError('READBACK_NONFINITE')
  def unique(rows):
   out={}
   for k,v in rows:need(k not in out,'READBACK_DUPLICATE_KEY');out[k]=v
   return out
  return json.loads(data,parse_constant=bad,object_pairs_hook=unique)
 modules=('current_programme_evaluator','source_guest_route_evaluator','source_living_evaluator','source_wall_function_evaluator')
 states={'BLOCKED_NO_PARENT_PROPOSAL':(False,False,1),'BLOCKED_NO_SUPPORTED_CAUSE':(True,False,1),
  'BLOCKED_BOUNDED_CHILD_NO_WITNESS':(True,False,2),'CAUSE_RESOLVED_NOT_QUALIFIED':(True,True,2),
  'CHILD_TARGET_CAUSE_UNRESOLVED':(True,True,2)}
 state=result.get('state');need(type(state)is str and state in states,'READBACK_STATE')
 parent,child,attempts=states[state]
 need(result.get('parent_observed')is parent and result.get('child_observed')is child,'READBACK_OBSERVATION_STATE')
 need(type(result.get('attempt_count'))is int and result['attempt_count']==attempts,'READBACK_ATTEMPT_COUNT')
 need(result.get('cause_repair_verified')is(state=='CAUSE_RESOLVED_NOT_QUALIFIED'),'READBACK_REPAIR_STATE')
 expected=set()
 for label,observed in(('parent',parent),('child',child)):
  if observed:
   expected.update({label+'_replay',label+'_physical',label+'_cause'})
   expected.update(label+'_current_'+name for name in modules)
   need(label+'_bundle_digest'in result and label+'_model_digest'in result,'READBACK_STATE_BUNDLE_REQUIRED')
  else:need(label+'_bundle_digest'not in result and label+'_model_digest'not in result,'READBACK_UNEXPECTED_MODEL')
 if not parent:expected.add('parent_no_witness')
 if attempts==2:
  expected.update({'parent_contract','child_constraint_retention'})
  need(result.get('actual_parent_contract_negative_rejections')==4 and type(result.get('actual_parent_contract_negative_rejections'))is int,'READBACK_CONTRACT_NEGATIVES')
 if attempts==2 and not child:expected.add('child_no_witness')
 if child:expected.update({'child_preservation','cause_resolution'})
 reports=read(folder/'reports.json')
 need(type(reports)is dict and set(reports)==expected,'READBACK_STATE_REPORT_SET')
 need(type(reports)is dict and type(result.get('report_digests'))is dict,'READBACK_REPORT_FIELDS')
 need(set(reports)==set(result['report_digests']),'READBACK_REPORT_SET')
 for key,value in reports.items():need(digest(value)==result['report_digests'][key],'READBACK_REPORT_DIGEST')
 bundles=0
 for label in('parent','child'):
  key=label+'_bundle_digest'
  if result.get(label+'_observed')is True:need(key in result,'READBACK_OBSERVED_BUNDLE_REQUIRED')
  if key not in result:continue
  bundle=read(folder/(label+'-bundle.json'));bundles+=1
  need(digest(bundle)==result[key],'READBACK_BUNDLE_DIGEST')
  mh=digest(bundle['packet']['world_model'])
  need(mh==result[label+'_model_digest'],'READBACK_MODEL')
  if label+'_cause'in reports:
   cause=reports[label+'_cause']
   need(cause['model_digest']==mh and cause['physical_digest']==result['report_digests'][label+'_physical'],'READBACK_CAUSE_MODEL_PHYSICAL')
  if label+'_physical'in reports:
   physical=reports[label+'_physical'];need(physical['model_hash']==mh,'READBACK_PHYSICAL_MODEL')
   from one_bed_pair_source_study import code_counts
   expected={'status':physical.get('status'),'errors':code_counts(physical.get('errors',[])),'pending':code_counts(physical.get('pending',[])),
    'not_evaluated_count':len(physical.get('not_evaluated',[])),'out_of_scope_count':len(physical.get('out_of_scope',[]))}
   need(digest(result[label+'_physical'])==digest(expected),'READBACK_PHYSICAL_SUMMARY')
  if label+'_replay'in reports:need(reports[label+'_replay']['model_hash']==mh,'READBACK_REPLAY_MODEL')
  if label+'_physical'in reports and label+'_replay'in reports:
   evidence={'model_digest':mh,'reports':{'physical':reports[label+'_physical'],'original_replay':reports[label+'_replay']},
    'report_digests':{'physical':result['report_digests'][label+'_physical'],'original_replay':result['report_digests'][label+'_replay']}}
   modules=('current_programme_evaluator','source_guest_route_evaluator','source_living_evaluator','source_wall_function_evaluator')
   for name in modules:
    key=label+'_current_'+name
    need(key in reports,'READBACK_CURRENT_REPORT_REQUIRED')
    report=reports[key];bind_current(name,report,evidence)
    expected={'state':report['state'],'integrity_verified':True,'missing_count':0,'evaluator_error_count':0}
    need(digest(result[label+'_current'][name])==digest(expected),'READBACK_CURRENT_SUMMARY')
 if 'child_constraint_retention'in reports:
  need(reports['child_constraint_retention'].get('verified')is True and digest(reports['child_constraint_retention'])==digest(result.get('constraint_retention')),'READBACK_CONSTRAINT_RETENTION')
 if 'parent_cause'in reports:need(digest(result.get('selected_causes'))==digest(reports['parent_cause']['selected_causes']),'READBACK_SELECTED_CAUSES')

 if 'cause_resolution'in reports:
  resolution=reports['cause_resolution']
  from planned_witness_contract108 import resolution as recompute_resolution,check_child
  need(digest(recompute_resolution(reports['parent_cause'],reports['child_cause']))==digest(resolution),'READBACK_RESOLUTION_RECOMPUTE')
  from planned_witness_contract108 import candidate_contract
  need(digest(result.get('operator_adapter'))==digest(candidate_contract(reports['parent_contract'])['operator_adapter']),'READBACK_OPERATOR_ADAPTER')
  cb=read(folder/'child-bundle.json')
  need(digest(check_child(reports['parent_contract'],cb['packet'],cb['proposals']))==digest(reports['child_preservation']),'READBACK_CHILD_PROTECTION')
  need(digest(result.get('new_supported_causes'))==digest(resolution['new_supported_causes']),'READBACK_NEW_CAUSES')
  need(digest(result.get('resolution_rows'))==digest(resolution['rows']),'READBACK_RESOLUTION_ROWS')
  expected=resolution['all_target_causes_resolved'] and not resolution['new_supported_causes']
  need(result.get('cause_repair_verified')is expected,'READBACK_RESOLUTION_STATE')
  need(result.get('protected_verified')is reports['child_preservation']['protected_verified'],'READBACK_PROTECTION_STATE')
 return {'verified':True,'bundle_count':bundles,'full_report_count':len(reports),'reports_file_digest':hashlib.sha256((folder/'reports.json').read_bytes()).hexdigest(),
  'state':'FULL_PARENT_CHILD_COLLECTION_READBACK'if child else'PARENT_ONLY_COLLECTION_READBACK'if parent else'NO_MODEL_COLLECTION_READBACK',
  'scope':'State-specific same-process file consistency readback, not independent engine replay or durable archive'}

def solver_observation(proposal):
 import math
 if proposal.get('status')=='NO_PROPOSAL_IN_THIS_PROGRAM'and proposal.get('reason')=='ROOM_OR_CORE_BOUND_CONFLICT':
  need(not any(key in proposal for key in('solver_status','solver_seconds','budget_seconds')),'PRE_SOLVER_OBSERVATION_CONFLICT')
  return {'solver_called':False,'solver_status':None,'solver_seconds':None,'budget_seconds':None,'state':'SOURCE_BOUND_CONFLICT_BEFORE_MILP'}
 out={}
 for key in('solver_status','solver_seconds','budget_seconds'):
  value=proposal.get(key)
  need(type(value)is int if key=='solver_status'else type(value)in(int,float)and math.isfinite(value)and value>=0,'SOLVER_OBSERVATION_TYPE')
  out[key]=value
 return out

def strip_panel_source(text):
 lines=text.splitlines(keepends=True);kept=[];mapping={};active=None;seen=[]
 pairs={' # R4_COMPOUND_CAPTURE_ROOT\n':' # R4_COMPOUND_CAPTURE_ROOT_END\n','  # R4_COMPOUND_CAPTURE_BRANCH\n':'  # R4_COMPOUND_CAPTURE_BRANCH_END\n',' # R4_COMPOUND_APPEND_PANEL\n':' # R4_COMPOUND_APPEND_PANEL_END\n'}
 for number,line in enumerate(lines,1):
  if active is not None:
   if line==active:active=None
   continue
  if line in pairs:seen.append(line);active=pairs[line];continue
  kept.append(line);mapping[number]=len(kept)
 need(active is None and len(seen)==3 and set(seen)==set(pairs),'PANEL_SOURCE_MARKERS')
 return ''.join(kept),mapping

def panel_capture(core,operator):
 import cause_directed_candidate108 as old,compound_panel_candidate108 as new
 opts={'sleep_roles':['double','twin'],'variant':0,'topology':'SIDE_ROOTED_SERVICES','parent_contract':operator,'enabled_causes':operator['enabled_causes'],'diagnostic_capture':lambda d:d}
 a=old.propose(core,2,**opts);b=new.propose(core,2,**opts)
 need('matrix'in a and 'matrix'in b,'PANEL_CAPTURE_NO_MASTER')
 return compare_panel_capture(a,b)

def compare_panel_capture(a,b):
 A=a['matrix'];B=b['matrix'];m,n=A.shape;C=B[:m,:n].tocsr()
 for key in('data','indices','indptr'):need(np.array_equal(getattr(A,key),getattr(C,key)),'PANEL_OLD_CSR_CHANGED')
 need(B[:m,n:].nnz==0,'PANEL_OLD_ROWS_NEW_COLUMNS')
 for key in('objective','integrality'):need(np.array_equal(a[key],b[key][:n]),'PANEL_OLD_VECTOR_CHANGED')
 for key in('lb','ub'):need(np.array_equal(getattr(a['bounds'],key),getattr(b['bounds'],key)[:n]),'PANEL_OLD_BOUNDS_CHANGED')
 for key in('lower','upper'):need(np.array_equal(a[key],b[key][:m]),'PANEL_OLD_ROW_BOUNDS_CHANGED')
 _,mapping=strip_panel_source((ROOT/'app/local_integration/compound_panel_candidate108.py').read_text())
 meta=[dict(r,source_line=mapping[r['source_line']])for r in b['row_metadata'][:m]]
 need(a['row_metadata']==meta and a['specs']==b['specs'],'PANEL_OLD_METADATA_CHANGED')
 k=(B.shape[0]-m)//5
 need(k>0 and B.shape==(m+5*k,n+4*k),'PANEL_APPENDED_SHAPE')
 need(np.all(b['objective'][n:]==0)and np.all(b['integrality'][n:]==1)and np.all(b['bounds'].lb[n:]==0)and np.all(b['bounds'].ub[n:]==1),'PANEL_APPENDED_VARIABLES')
 need(all(r['group']=='source_entry_open_panel_all_network_reservation'for r in b['row_metadata'][m:]),'PANEL_APPENDED_GROUP')
 return {'verified':True,'original_rows':m,'original_columns':n,'added_rows':5*k,'added_binary_columns':4*k,'reserved_body_segments':k,
  'scope':'All existing constraints/objective exact; source-line offsets mapped to byte-identical original. Appended source-panel reservation for this conservative network family.'}
