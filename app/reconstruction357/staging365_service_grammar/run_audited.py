"""External pre-import freeze anchor. Old frozen source remains untouched."""
import sys,json,hashlib,types
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
EXPECTED_PREREG_SHA='5da104f3129f207c47dab970dc890ca2bdfeb4975619ac3063b38eefbb51152d'

def load_verified(name,pins):
 path=HERE/(name+'.py');data=path.read_bytes();key=str(path.relative_to(ROOT))
 if hashlib.sha256(data).hexdigest()!=pins['source_inventory'].get(key):raise ValueError('PREIMPORT_SOURCE_CHANGED:'+name)
 module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module;exec(compile(data,str(path),'exec'),module.__dict__);return module

def main():
 if sys.argv[1:]not in (['--execute-after-audit'],['--worker'],['--check']):raise SystemExit('OFF: audited launch required')
 data=(HERE/'runtime_preregistered.json').read_bytes()
 if hashlib.sha256(data).hexdigest()!=EXPECTED_PREREG_SHA:raise ValueError('EXTERNAL_PREREG_FREEZE_CHANGED')
 pins=json.loads(data)
 for name,sha in pins['source_inventory'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('PREIMPORT_INVENTORY_CHANGED:'+name)
 sys.path.insert(0,str(ROOT/'planha_general150_runtime_work'))
 contract=load_verified('contract',pins)
 contract.check_pins()
 if sys.argv[1]=='--check':
  print(json.dumps({'preimport_inventory':'PASS','execution':False}));return
 if sys.argv[1]=='--worker':
  oldout,olderr=sys.stdout,sys.stderr
  try:
   with (HERE/'stdout.jsonl').open('x')as out,(HERE/'stderr.log').open('x')as err:
    sys.stdout=out;sys.stderr=err
    load_verified('service_anchor365',pins);load_verified('coarse_branch365',pins);load_verified('adapter365',pins);load_verified('worker',pins).main()
  finally:sys.stdout,sys.stderr=oldout,olderr
 else:
  load_verified('containment',pins);load_verified('supervisor',pins).main()
if __name__=='__main__':main()
