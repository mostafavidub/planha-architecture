import sys,json
from pathlib import Path
from guard385 import guard
HERE=Path(__file__).resolve().parent;W=HERE.parent.parent;expected=sys.argv[1];count=guard(expected)
P=W/'review385_actual_v1';P.mkdir(exist_ok=False)
(P/'preregistration.json').write_text(json.dumps({'freeze_sha256':expected,'outer_seconds':660,'owner_seconds':540,'cycle_shared_seconds':530,'phase_caps':{'balanced':[45,90,5,90],'joint':[90,90,5,60],'seal':25},'retry':False,'browser_submissions':1,'source_schemas':{'balanced':'FINITE_PORTALS378_SOURCE_TRACE_V1','joint':'SOURCE_SERVICE_JOINT367_TRACE_V1'},'balanced_selection_rank':1,'test_only':False,'experimental':True,'requested_count':2,'tested_branch_count':2,'source_file_count':count},indent=2))
sys.path.insert(0,str(HERE.parent/'staging368_final_pipeline'))
from supervisor import supervise
e=P/'outer_supervision_evidence';e.mkdir()
(P/'launch_state.json').write_text(json.dumps({'state':'RUNNING_UNVERIFIED','cleanup_verified':False}))
try:s=supervise([sys.executable,'-B',str(HERE/'browser385.py'),str(P),expected],660,evidence_directory=e)
except Exception as error:s={'reason':'OUTER_SUPERVISOR_EXCEPTION','cleanup_verified':False,'worker_reaped':False,'unresolved':['UNKNOWN'],'error':type(error).__name__+':'+str(error)}
(P/'outer_supervision.json').write_text(json.dumps(s,indent=2))
clean=s.get('reason')=='COMPLETED'and s.get('worker_returncode')==0 and s.get('cleanup_verified')is True and s.get('worker_reaped')is True and s.get('unresolved')==[]
shutdown=P/'server_shutdown.json';owner_clean=shutdown.exists()and json.loads(shutdown.read_text()).get('safe_idle')is True
source_ok=False
try:
 guard(expected);source_ok=True
 (P/'source_evidence_unchanged.json').write_text(json.dumps({'verified':True,'count':count}))
except Exception as error:(P/'source_evidence_unchanged.json').write_text(json.dumps({'verified':False,'error':str(error)}))
result=None
try:result=json.loads((P/'browser_result.json').read_text())
except Exception:pass
audit_ok=False
try:audit_ok=json.loads((P/'browser_binding_audit.json').read_text())['verified']is True and json.loads((P/'listener_closed.json').read_text())['verified']is True and json.loads((P/'server_identity_audit.json').read_text())['original_process_gone']is True
except Exception:pass
success=clean and owner_clean and source_ok and isinstance(result,dict)and result.get('state')=='COMPLETED_CURRENT_TWO_BUILDER_REVIEW'and result.get('semantic_state')in('UNKNOWN_CURRENT_DEPENDENCIES','PASS_SCOPED_CURRENT_SET') and audit_ok
(P/'containment_outcome.json').write_text(json.dumps({'outer_reason':s['reason'],'owner_clean_shutdown_observed':owner_clean,'emergency_outer_containment':not clean,'not_equivalent_to_owner_clean_shutdown':not clean or not owner_clean,'completed':success},indent=2))
(P/'launch_state.json').write_text(json.dumps({'state':'COMPLETED'if success else'STOPPED_OR_UNRESOLVED','cleanup_verified':clean and owner_clean}));print(json.dumps(s))
if not success:raise SystemExit(1)
