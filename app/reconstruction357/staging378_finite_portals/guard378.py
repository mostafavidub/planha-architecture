"""All-source/evidence guard; stdlib only, called before computational imports."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parents[2]
def guard(expected):
 p=W/'review378_preaudit/source_freeze_harness.json'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise ValueError('FREEZE_CHANGED')
 files=json.loads(p.read_text())['files']
 for n,h in files.items():
  path=(W/n).resolve()
  if not path.is_relative_to(W)or not path.is_file()or hashlib.sha256(path.read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_OR_EVIDENCE_CHANGED:'+n)
 return len(files)
def clean(receipt):
 return receipt.get('reason')=='COMPLETED' and receipt.get('worker_returncode')==0 and receipt.get('cleanup_verified')is True and receipt.get('worker_reaped')is True and receipt.get('unresolved')==[]
def cycle_complete(cycle):
 return isinstance(cycle,dict)and cycle.get('status')in('UNSUPPORTED_REPAIR_REASON','UNKNOWN_PENDING_REVIEW','NO_CURRENT_REJECTION_SCOPED_PHYSICAL_ONLY','UNKNOWN_REVIEW_STATUS')
def launch_complete(receipt,source,cycle):
 return clean(receipt)and source.get('verified')is True and cycle_complete(cycle)
