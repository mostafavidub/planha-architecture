import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'finite_comparison358'))
from build_transitive_manifest359 import closure
from dynamic_readset362 import kernel_readset
files,edges=closure(['finite_comparison365/service_closure365.py'])
explicit=['staging365_balanced_portals/actual365.json','review365_balanced_source_validation/result.json','staging362_core_notch/actual362.json','review362_source_validation/result.json','staging359_hall_clamp/actual359.json','review359_source_validation/result.json','staging274_evaluator_transport_fix/quality_contract.json']
for v in (359,362,365):explicit += [f'semantic_rules357/group_readsets{v}_pins.json',f'semantic_rules357/method_registry_source{v}.json']
explicit += ['semantic_rules357/network365_manifest.json','semantic_rules357/network365_freeze.json']
files|={ROOT/p for p in explicit};files|={ROOT/p for p in kernel_readset()};seen=set()
def discover(v,key=None):
 if isinstance(v,dict):
  for k,val in v.items():
   if key in ('source_inventory','sources','code_pins','files','source_before','source_after','readset')and isinstance(val,str)and len(val)==64:
    for base in (ROOT,ROOT/'semantic_rules357',ROOT/'planha_general150_runtime_work'):
     p=base/k
     if p.is_file():
      if hashlib.sha256(p.read_bytes()).hexdigest()!=val:raise ValueError('DEPENDENCY_PIN_DRIFT:'+str(p))
      files.add(p.resolve())
   discover(val,k)
 elif isinstance(v,list):
  for z in v:discover(z,key)
while files-seen:
 batch=files-seen;seen|=batch
 for p in batch:
  if p.suffix=='.json':discover(json.loads(p.read_text()))
 py=[str(p.relative_to(ROOT))for p in batch if p.suffix=='.py']
 if py:
  more,e=closure(py);files|=more;edges.update(e)
manifest={'schema':'SERVICE365_FIXED_TRANSITIVE_SOURCE_MANIFEST','files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)},'import_edges':edges,'scope':'Source365 current and source362/359 finite bath-WC baselines; actual ownfresh guards, no global minimum or wholeplan admission.'}
p=HERE/'service_manifest365.json';p.write_text(json.dumps(manifest,indent=2));print(hashlib.sha256(p.read_bytes()).hexdigest(),len(files))
