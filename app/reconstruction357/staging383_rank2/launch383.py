"""Exactly one preregistered rank2 candidate. No browser or repair search."""
import json,sys,uuid
from pathlib import Path
from guard383 import guard,clean,cycle_complete,launch_complete
HERE=Path(__file__).resolve().parent;W=HERE.parents[1];expected=sys.argv[1]
count=guard(expected);P=W/'review383_actual_v1';P.mkdir(exist_ok=False)
reg={'schema':'FINITE383_SINGLE_CANDIDATE_PREREGISTRATION','run_id':str(uuid.uuid4()),'raw':{'W':'26','L':'28','n':2,'requested_count':2},'selection_rank':2,'family_policy':'WIDEST_OPERATION_COMPONENT_INTERIOR_QUARTILES_MAX_SLACK_THEN_PARAMETER_SPREAD_V1','selection_policy':'PREDECLARED_FINITE_FAMILY_RANK2_FOR_COHORT_REVIEW','shared_seconds':145,'outer_seconds':160,'phase_maxima':{'construct':45,'fresh':90,'audit':5},'retry':False,'search_until_failure':False,'browser_executed':False,'repair_authorized':False,'semantic_reuse':False,'freeze_sha256':expected}
(P/'preregistration.json').write_text(json.dumps(reg,indent=2))
sys.path.insert(0,str(HERE.parent/'staging368_final_pipeline'))
from supervisor import supervise
e=P/'outer_supervision_evidence';e.mkdir()
(P/'launch_state.json').write_text(json.dumps({'state':'RUNNING_UNVERIFIED','cleanup_verified':False,'run_id':reg['run_id']}))
try:
 receipt=supervise([sys.executable,'-B',str(HERE/'cycle383.py'),str(P),expected],160,evidence_directory=e)
except Exception as error:
 receipt={'reason':'OUTER_SUPERVISOR_EXCEPTION','cleanup_verified':False,'worker_reaped':False,'unresolved':['OUTER_SUPERVISION_STATE_UNKNOWN'],'error':type(error).__name__+':'+str(error)}
(P/'outer_supervision.json').write_text(json.dumps(receipt,indent=2))
try:
 count=guard(expected);source={'verified':True,'file_count':count,'freeze_sha256':expected}
except Exception as error:
 source={'verified':False,'error':type(error).__name__+':'+str(error)}
(P/'post_outer_source_audit.json').write_text(json.dumps(source,indent=2))
cycle_path=P/'cycle_result.json';cycle=None
try:
 if cycle_path.is_file():cycle=json.loads(cycle_path.read_text())
except Exception:pass
cycle_ok=cycle_complete(cycle)
success=launch_complete(receipt,source,cycle)
outcome={'run_id':reg['run_id'],'outer_clean_success':clean(receipt),'source_unchanged':source['verified'],'cycle_result_present':cycle_path.is_file(),'cycle_completed':cycle_ok,'execution_completed':success,'accepted':False,'delivery_allowed':False,'request_fulfilled':False,'browser_executed':False,'emergency_containment_or_failure':not clean(receipt)}
(P/'launch_result.json').write_text(json.dumps(outcome,indent=2))
(P/'launch_state.json').write_text(json.dumps({'state':'COMPLETED'if success else'STOPPED_OR_UNRESOLVED','cleanup_verified':clean(receipt),'run_id':reg['run_id']}));print(json.dumps(outcome))
if not success:raise SystemExit(1)
