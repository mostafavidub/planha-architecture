"""Exactly one audited continuation; freeze is verified before imports."""
import hashlib,json,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;W=HERE.parent.parent
F=W/'review371_preaudit/source_freeze.json';expected=sys.argv[1]
if hashlib.sha256(F.read_bytes()).hexdigest()!=expected:raise ValueError('FREEZE_CHANGED')
files=json.loads(F.read_text())['files']
def check():
 for n,h in files.items():
  p=(W/n).resolve()
  if not p.is_relative_to(W)or hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_OR_BOUND_EVIDENCE_CHANGED:'+n)
check();P=W/'review371_actual_v1';P.mkdir(exist_ok=False)
(P/'preregistration.json').write_text(json.dumps({'execution_id':str(uuid.uuid4()),'overall_seconds':190,'phase_maxima':{'propose':3,'construct':90,'fresh':90,'compare':3},'prior_run_id':'5caf57c9-82d9-4aa6-87f0-1c0362abaf21','prior_review_id':'eaecdc51-eb4c-4ddd-a2c4-8ce5c64c5ad0','first_review_reused_from_actual369':True,'fresh_after_repair_required':True,'test_only':True,'retry':False,'freeze_sha256':expected},indent=2))
sys.path.insert(0,str(HERE.parent/'staging368_final_pipeline'))
from supervisor import supervise
e=P/'outer_supervision_evidence';e.mkdir()
s=supervise([sys.executable,'-B',str(HERE/'cycle371.py'),str(P)],190,evidence_directory=e)
(P/'outer_supervision.json').write_text(json.dumps(s,indent=2));check()
(P/'source_and_evidence_unchanged.json').write_text(json.dumps({'verified':True,'file_count':len(files),'freeze_sha256':expected}))
print(json.dumps(s))
if s['reason']!='COMPLETED'or s['worker_returncode']!=0 or not s['cleanup_verified']or not s['worker_reaped']or s['unresolved']:raise SystemExit(1)
