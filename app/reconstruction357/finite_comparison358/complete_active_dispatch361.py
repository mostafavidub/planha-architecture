"""Write-once bounded completion of actual source150 stopped branches."""
import json,sys,time,hashlib,copy,importlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'planha_general150_runtime_work';HERE=Path(__file__).resolve().parent
prereg=json.loads((HERE/'dispatch361_preregistration.json').read_text())
for path,expected in prereg['code_pins'].items():
 if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=expected:raise ValueError('PREIMPORT_SOURCE_CHANGED:'+path)
sys.path.insert(0,str(SRC))
from constructor129 import frame,build,context
from contract114 import digest
import engine150

def sources():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted([*SRC.glob('*.py'),*SRC.glob('*.json'),*(p for p in(SRC/'references').rglob('*')if p.is_file())])}
def execute():
 target=HERE/'active_dispatch_actual361.json'
 if target.exists()or list(HERE.glob('dispatch361_*_LEFT_RIGHT.json')):raise ValueError('WRITE_ONCE_PRESERVE_COMPLETED_ATTEMPTS')
 original=json.loads((ROOT/'actual_run/actual_response.json').read_text());raw=original['raw'];before=sources();attempts=copy.deepcopy(original['attempts']);new=[];start=time.monotonic();solvercalls=0;core,_=frame(raw,'LEFT_RIGHT')
 from private_t_source133 import build as private_t
 template=private_t(core);new.append({'organization':'TURN_T','family':'LEFT_RIGHT','status':'UNSUPPORTED_BUNDLE_FIT'if template is None else'FIT_REQUIRES_EVALUATION','source_primitive':'private_t_source133.build','core_digest':digest(core),'template':template,'solver_called':False,'scope':'EXACT_SOURCE_PRIMITIVE_FIT_NOT_GLOBAL_INFEASIBILITY'})
 def one(org,module,extra):
  nonlocal solvercalls
  old=next(a for a in attempts if a['organization']==org and a['family']=='LEFT_RIGHT');t=time.monotonic();r={'organization':org,'family':'LEFT_RIGHT','prior_status':old['status'],'source_callable':module+'.propose','time_limit':3,'not_global_infeasibility':True}
  solvercalls+=1
  try:
   p=importlib.import_module(module).propose(core,time_limit=3,**extra);r['proposal']=p;r['status']=p['status'];r['solver_seconds']=time.monotonic()-t
   if p['status']=='PROPOSAL_ONLY':
    if org=='SIDECAR_GROUP138':engine150.require_runtime_group_proposal(p,expected_marker=engine150.GROUP_MARKER,core=core)
    if org=='SIDECAR_COMPACT144':
     if p.get('generation_method')!=engine150.COMPACT_MARKER:raise ValueError('COMPACT150_DISPATCH_MARKER_REQUIRED')
     engine150.validate_compact(p)
    r['dispatcher_source_preconditions']='EXECUTED_OR_NOT_APPLICABLE_EXACT_ENGINE150_CALLSITE'
    packet=build(raw,'LEFT_RIGHT',p);ctx=context(raw,p,packet);r['candidate']={'request':raw,'request_digest':digest(raw),'packet':packet,'model':packet['world_model'],'model_digest':digest(packet['world_model']),'generation_context':ctx};r['eligibility']='UNKNOWN_REQUIRES_FRESH_SOURCE_REGISTERED_REVIEW';r['accepted']=False
  except Exception as ex:r.update(status='STOPPED_EXECUTION_ERROR',error=type(ex).__name__+':'+str(ex))
  old.update(r);new.append(r)
  checkpoint=HERE/('dispatch361_'+org+'_LEFT_RIGHT.json')
  if checkpoint.exists():raise ValueError('ATTEMPT_CHECKPOINT_ALREADY_EXISTS')
  checkpoint.write_text(json.dumps(r,ensure_ascii=False,indent=2))
 new.append({'organization':'TURN_T_CONNECTED','family':'LEFT_RIGHT','status':next(a['status']for a in original['attempts']if a['organization']=='TURN_T_CONNECTED'),'historical_actual_pointer':'actual_run/actual_response.json#/attempts/3','source_primitive_fit_current':template is not None,'solver_called':False})
 for org,module,extra in [('SIDECAR_GROUP138','coarse_sidecar_group138',{'gap_bodies':2}),('SIDECAR_PROTECTED','coarse_sidecar_seating136',{}),('ROW','coarse_master129',{})]:one(org,module,extra)
 if engine150.compact_policy(attempts):one('SIDECAR_COMPACT144','coarse_sidecar_circulation144',{})
 else:new.append({'organization':'SIDECAR_COMPACT144','family':'LEFT_RIGHT','status':'NOT_SCHEDULED_POLICY','reason':'SOURCE_COMPACT_POLICY_FALSE_AFTER_GROUP_COMPLETION','solver_called':False})
 after=sources();out={'schema':'BOUNDED_ACTIVE_SOURCE150_DISPATCH_COMPLETION361','raw':raw,'original_artifact_sha256':hashlib.sha256((ROOT/'actual_run/actual_response.json').read_bytes()).hexdigest(),'original_attempts':original['attempts'],'completed_attempts':new,'source_before':before,'source_after':after,'source_unchanged':before==after,'solver_call_count':solvercalls,'solver_budget_per_call':3,'wall_seconds':time.monotonic()-start,'fresh_executed':False,'parent_acceptance':False,'global_infeasibility':False};target.write_text(json.dumps(out,ensure_ascii=False,indent=2));print([(a['organization'],a['status'])for a in new])
if __name__=='__main__':execute()
