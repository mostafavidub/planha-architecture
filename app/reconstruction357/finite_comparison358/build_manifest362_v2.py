"""Static imports, explicit data roots, recursively named source inventories."""
from build_transitive_manifest359 import ROOT,HERE,closure,json,hashlib,Path
roots=['finite_comparison358/q04_closure362_v2.py','finite_comparison358/run_q04_362_v2.py']
files,edges=closure(roots)
explicit=['finite_comparison358/bound_comparison_actual358.json','finite_comparison358/core_branch_bound358.json','finite_comparison358/dispatch361_preregistration.json','finite_comparison358/active_dispatch_actual361.json','staging358_core_branch/actual_full_band358.json','actual_run/actual_response.json','staging357_comparative/attached_service_final357.json','staging358_comparative/row_candidate358.json','staging359_hall_clamp/actual359.json','staging360_core_notch/actual360.json','staging362_core_notch/actual362.json','review360_source_validation/result.json','review362_source_validation/result.json','staging274_evaluator_transport_fix/quality_contract.json']
# All fixed JSON metadata consumed by imported semantic modules. Conservative
# snapshot, not a permission to remove later safety pins when a dependency moves.
explicit += ['semantic_rules357/'+n for n in ['eligibility_intrinsic362_pins.json','group_readsets362_pins.json','method_registry_source362.json','method_registry.json','acceptance357_comparison_source_map.json']]
files|={ROOT/p for p in explicit};seen=set()
def discover(v, key=None):
 if isinstance(v,dict):
  for k,val in v.items():
   if key in ('source_inventory','code_pins','files','source_before','source_after','readset') and isinstance(k,str)and isinstance(val,str)and len(val)==64:
    for base in (ROOT,ROOT/'semantic_rules357',ROOT/'planha_general150_runtime_work'):
     p=base/k
     if p.is_file():
      if hashlib.sha256(p.read_bytes()).hexdigest()!=val:raise ValueError('NAMED_SOURCE_PIN_DRIFT:'+str(p))
      files.add(p.resolve())
   discover(val,k)
 elif isinstance(v,list):
  for z in v:discover(z,key)
while files-seen:
 batch=files-seen;seen|=batch
 for p in batch:
  if p.suffix=='.json':discover(json.loads(p.read_text()))
 py=[str(p.relative_to(ROOT)) for p in batch if p.suffix=='.py']
 if py:
  more,e=closure(py);files|=more;edges.update(e)
m={'schema':'Q04_362_V2_TRANSITIVE_FIXED_MANIFEST','roots':roots,'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)},'import_edges':edges,'live_authority':False,'scope':'Stored-artifact bound reassessment; COMMON role remains pending; external caller must pin manifest SHA.'}
p=HERE/'q04_manifest362_v2.json';p.write_text(json.dumps(m,indent=2));print(hashlib.sha256(p.read_bytes()).hexdigest(),len(files))
