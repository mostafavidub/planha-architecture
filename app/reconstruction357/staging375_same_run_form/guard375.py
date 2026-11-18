import json,hashlib
from pathlib import Path
W=Path(__file__).resolve().parents[2]
def guard(expected):
 p=W/'review375_preaudit/source_freeze.json'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise ValueError('FREEZE_CHANGED')
 files=json.loads(p.read_text())['files']
 for n,h in files.items():
  if hashlib.sha256((W/n).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_OR_EVIDENCE_CHANGED:'+n)
 return len(files)
