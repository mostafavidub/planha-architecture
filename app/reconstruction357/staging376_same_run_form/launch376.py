import sys,json
from pathlib import Path
from guard376 import guard
HERE=Path(__file__).resolve().parent;W=HERE.parent.parent;expected=sys.argv[1];count=guard(expected)
P=W/'review376_actual_v1';P.mkdir(exist_ok=False)
(P/'preregistration.json').write_text(json.dumps({'freeze_sha256':expected,'outer_seconds':360,'owner_seconds':244,'cycle_shared_seconds':240,'phase_caps':[45,90,3,90,90,10],'retry':False,'browser_submissions':1,'test_only':True,'requested_count':2,'tested_branch_count':1,'source_file_count':count},indent=2))
sys.path.insert(0,str(HERE.parent/'staging368_final_pipeline'))
from supervisor import supervise
e=P/'outer_supervision_evidence';e.mkdir()
s=supervise([sys.executable,'-B',str(HERE/'browser376.py'),str(P),expected],360,evidence_directory=e)
(P/'outer_supervision.json').write_text(json.dumps(s,indent=2))
(P/'containment_outcome.json').write_text(json.dumps({'outer_reason':s['reason'],'owner_clean_shutdown_observed':(P/'server_shutdown.json').exists()and json.loads((P/'server_shutdown.json').read_text()).get('safe_idle')is True,'emergency_outer_containment':s['reason']!='COMPLETED'or(P/'drain_unresolved.json').exists(),'not_equivalent_to_owner_clean_shutdown':s['reason']!='COMPLETED'or(P/'drain_unresolved.json').exists()},indent=2))
guard(expected)
(P/'source_evidence_unchanged.json').write_text(json.dumps({'verified':True,'count':count}))
print(json.dumps(s))
if s['reason']!='COMPLETED'or s['worker_returncode']!=0 or not s['cleanup_verified']or not s['worker_reaped']or s['unresolved']:raise SystemExit(1)
