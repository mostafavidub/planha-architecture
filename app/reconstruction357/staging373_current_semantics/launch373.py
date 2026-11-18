"""One fixed-current372 semantic proof run,60s; no source/fresh rerun."""
import hashlib,json,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;W=HERE.parent.parent
F=W/'review373_preaudit/source_freeze.json';expected=sys.argv[1]
if hashlib.sha256(F.read_bytes()).hexdigest()!=expected:raise ValueError('FREEZE_CHANGED')
files=json.loads(F.read_text())['files']
def check():
 for n,h in files.items():
  p=(W/n).resolve()
  if not p.is_relative_to(W)or hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_OR_EVIDENCE_CHANGED:'+n)
check();P=W/'review373_actual_v1';P.mkdir(exist_ok=False)
from gate373 import load_inputs,validate,D
inputs=load_inputs();binding=validate(inputs['record'],inputs['fresh'],inputs['lineage']);payload={k:inputs[k]for k in ('record','fresh','lineage')}
(P/'input_payload.json').write_text(json.dumps(payload));payload_sha=hashlib.sha256((P/'input_payload.json').read_bytes()).hexdigest()
(P/'preregistration.json').write_text(json.dumps({'execution_id':str(uuid.uuid4()),'max_seconds':60,'retry':False,'scope':'CURRENT372_SEMANTIC_PROOF_RECOMPUTATION_ONLY','binding':binding,'test_only':True,'no_new_fresh_checker':True,'freeze_sha256':expected,'input_payload_sha256':payload_sha},indent=2))
sys.path.insert(0,str(HERE.parent/'staging368_final_pipeline'))
from supervisor import supervise
e=P/'supervision_evidence';e.mkdir()
s=supervise([sys.executable,'-B',str(HERE/'worker373.py'),str(P)],60,evidence_directory=e)
(P/'supervision.json').write_text(json.dumps(s,indent=2));check()
if hashlib.sha256((P/'input_payload.json').read_bytes()).hexdigest()!=payload_sha:raise ValueError('TRANSPORTED_INPUT_CHANGED')
(P/'source_evidence_unchanged.json').write_text(json.dumps({'verified':True,'file_count':len(files),'input_payload_unchanged':True}))
print(json.dumps(s))
if s['reason']!='COMPLETED'or s['worker_returncode']!=0 or not s['worker_reaped']or not s['cleanup_verified']or s['unresolved']:raise SystemExit(1)
