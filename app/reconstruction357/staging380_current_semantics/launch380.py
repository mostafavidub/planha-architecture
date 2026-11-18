"""One fixed current378 semantic-only pass, bounded60s; no generator or fresh."""
import json,hashlib,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;W=HERE.parents[1];expected=sys.argv[1]
F=W/'review380_preaudit/source_freeze.json'
def check():
 if hashlib.sha256(F.read_bytes()).hexdigest()!=expected:raise ValueError('FREEZE_CHANGED')
 files=json.loads(F.read_text())['files']
 for n,h in files.items():
  p=(W/n).resolve()
  if not p.is_relative_to(W)or hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_CHANGED:'+n)
 return len(files)
count=check();P=W/'review380_actual_v1';P.mkdir(exist_ok=False)
from gate380 import load_inputs,validate
i=load_inputs();binding=validate(i['record'],i['fresh'])
(P/'preregistration.json').write_text(json.dumps({'execution_id':str(uuid.uuid4()),'max_seconds':60,'retry':False,'binding':binding,'scope':'PINNED_CURRENT378_ESSENTIAL_SEMANTIC_REASSESSMENT','new_fresh':False,'construction':False,'candidate_optimization':False,'freeze_sha256':expected},indent=2))
(P/'state.json').write_text(json.dumps({'state':'RUNNING_UNVERIFIED','cleanup_verified':False}))
sys.path.insert(0,str(HERE.parent/'staging368_final_pipeline'))
from supervisor import supervise
e=P/'supervision_evidence';e.mkdir()
try:s=supervise([sys.executable,'-B',str(HERE/'worker380.py'),str(P)],60,evidence_directory=e)
except Exception as e:s={'reason':'SUPERVISOR_ERROR','error':str(e),'cleanup_verified':False,'unresolved':['UNKNOWN']}
(P/'supervision.json').write_text(json.dumps(s,indent=2));count=check()
(P/'source_unchanged.json').write_text(json.dumps({'verified':True,'files':count}))
ok=s.get('reason')=='COMPLETED'and s.get('worker_returncode')==0 and s.get('worker_reaped')is True and s.get('cleanup_verified')is True and s.get('unresolved')==[] and(P/'result.json').is_file()
(P/'state.json').write_text(json.dumps({'state':'COMPLETED'if ok else'STOPPED_OR_UNRESOLVED','cleanup_verified':s.get('cleanup_verified',False),'accepted':False,'delivery_allowed':False}))
print(json.dumps(s))
if not ok:raise SystemExit(1)
