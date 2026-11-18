"""Verify preregistered closure before imports, then supervise exactly one cycle."""
import hashlib,json,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;WORKSPACE=ROOT.parent
FREEZE=WORKSPACE/'review369_current_family_preaudit/controlled_source_freeze.json'
expected=sys.argv[1]
if hashlib.sha256(FREEZE.read_bytes()).hexdigest()!=expected:raise ValueError('PREREGISTERED_FREEZE_CHANGED')
freeze=json.loads(FREEZE.read_text())
def check():
 for name,want in freeze['files'].items():
  p=(WORKSPACE/name).resolve()
  if not p.is_relative_to(WORKSPACE)or hashlib.sha256(p.read_bytes()).hexdigest()!=want:raise ValueError('SOURCE_CHANGED:'+name)
check()
folder=WORKSPACE/'review369_current_family_actual_v1'
folder.mkdir(exist_ok=False);run_id=str(uuid.uuid4())
(folder/'preregistration.json').write_text(json.dumps({'run_id':run_id,'freeze_sha256':expected,
 'overall_seconds':240,'construct_max_seconds':45,'fresh_max_each':90,
 'repair_reconstruct_max_seconds':90,'operator_max_seconds':3,'test_only':True,'retry':False,
 'translation':{'source_key':'sofa1_use','dx':'-3/2','dy':'0'},
 'expected_collision':{'unit':'A','fixtures':['sofa1','armchair2']},
 'natural_generation_failure':False,'form_path_executed':False},indent=2))
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from supervisor import supervise
evidence=folder/'outer_supervision_evidence';evidence.mkdir()
s=supervise([sys.executable,'-B',str(HERE/'cycle369.py'),str(folder),run_id],240,evidence_directory=evidence)
(folder/'outer_supervision.json').write_text(json.dumps(s,indent=2));check()
(folder/'source_unchanged.json').write_text(json.dumps({'source_unchanged':True,'freeze_sha256':expected}))
print(json.dumps({'run_id':run_id,'outer_supervision':s,'result_exists':(folder/'cycle_result.json').exists()}))
if s.get('reason')!='COMPLETED'or s.get('worker_returncode')!=0 or not s.get('cleanup_verified')or not s.get('worker_reaped')or s.get('unresolved'):raise SystemExit(1)
