"""Preimport freezecheck then byte-identical audited dedicated supervisor reuse."""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def main():
 prereg=HERE/'dispatch361_preregistration.json'
 if len(sys.argv)!=2 or hashlib.sha256(prereg.read_bytes()).hexdigest()!=sys.argv[1]:raise ValueError('EXTERNAL_PREREG_PIN')
 pins=json.loads(prereg.read_text())
 for path,h in pins['code_pins'].items():
  if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=h:raise ValueError('PREIMPORT_FREEZE_CHANGED:'+path)
 target=HERE/'dispatch361_supervision.json'
 if target.exists():raise ValueError('SUPERVISOR_WRITE_ONCE')
 from containment361 import supervise
 result=supervise([sys.executable,str(HERE/'complete_active_dispatch361.py')],90)
 result.update(schema='DISPATCH361_SUPERVISION',prereg_sha256=sys.argv[1],fresh_executed=False,accepted=False)
 result['source_changed']=[path for path,h in pins['code_pins'].items() if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=h]
 target.write_text(json.dumps(result,indent=2));print(json.dumps(result))
 if not result['cleanup_verified'] or result['source_changed'] or not (HERE/'active_dispatch_actual361.json').exists():raise SystemExit(1)
if __name__=='__main__':main()
