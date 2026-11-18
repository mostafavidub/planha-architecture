import sys,json,hashlib,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'finite_comparison358'))
from build_transitive_manifest359 import closure
from dynamic_readset362 import kernel_readset
files,edges=closure(['finite_comparison367/q04_closure367_v2.py'])
explicit=['staging365_balanced_portals/actual365.json','review365_balanced_source_validation/result.json','staging362_core_notch/actual362.json','review362_source_validation/result.json','staging359_hall_clamp/actual359.json','review359_source_validation/result.json','staging274_evaluator_transport_fix/quality_contract.json']
for v in (359,362,365):explicit += [f'semantic_rules357/group_readsets{v}_pins.json',f'semantic_rules357/method_registry_source{v}.json']
explicit += ['semantic_rules357/network365_manifest.json','semantic_rules357/network365_freeze.json']
explicit += ['actual_run/actual_response.json','staging357_comparative/attached_service_final357.json','staging358_comparative/row_candidate358.json','staging360_core_notch/actual360.json','review360_source_validation/result.json','staging364_balanced_portals/actual364.json','review364_diagnostic/geometry_operations.json','staging365_service_grammar/candidate365.json','review365_service_source_validation/result.json','review365_launcher/selector_preselection.json','staging358_core_branch/actual_full_band358.json','finite_comparison358/core_branch_bound358.json','finite_comparison358/active_dispatch_actual361.json','finite_comparison358/bound_comparison_actual358.json','semantic_rules357/eligibility_intrinsic365.py','semantic_rules357/eligibility_intrinsic365_pins.json','semantic_rules357/method_registry.json','semantic_rules357/eligibility_intrinsic_service365.py','semantic_rules357/eligibility_intrinsic_service365_pins.json','semantic_rules357/group_readsets_service365_pins.json','semantic_rules357/method_registry_service365.json']
explicit += ['review367_joint_attempt2/actual367.json','review367_joint_source_validation_attempt2/result.json','semantic_rules357/group_readsets367_pins.json','semantic_rules357/method_registry_source367.json','semantic_rules357/network367_manifest.json','semantic_rules357/group_network367_freeze.json','semantic_rules357/intrinsic_roles_joint367_source_freeze.json']
explicit += ['semantic_rules357/eligibility_intrinsic367_pins.json','semantic_rules357/intrinsic_private367_manifest.json','review367_joint_attempt2/source_delta.json']
files|={ROOT/p for p in explicit};files|={ROOT/p for p in kernel_readset()};seen=set()
def discover(v,key=None):
 if isinstance(v,dict):
  for k,val in v.items():
   if key in ('source_inventory','sources','code_pins','files','source_before','source_after','readset')and isinstance(val,str)and len(val)==64:
    for base in (ROOT,ROOT/'semantic_rules357',ROOT/'planha_general150_runtime_work'):
     p=base/k
     if p.is_file():
      if hashlib.sha256(p.read_bytes()).hexdigest()!=val:raise ValueError('DEPENDENCY_PIN_DRIFT:'+str(p)+' IN '+str(current_json))
      files.add(p.resolve())
   discover(val,k)
 elif isinstance(v,list):
  for z in v:discover(z,key)
while files-seen:
 batch=files-seen;seen|=batch
 for p in batch:
  if p.suffix=='.json':
   current_json=p
   if os.path.relpath(p,ROOT) not in ['staging365_service_grammar/preregistered_v2.json', 'staging365_service_grammar/manifest_v2.json', 'staging365_service_grammar/v2_preserved/preregistered_v2.json', 'staging365_service_grammar/v2_preserved/manifest_v2.json', 'staging357_comparative/attached_service_candidate357.json', 'staging357_comparative/anchored_candidate357.json']:discover(json.loads(p.read_text()))
 py=[os.path.relpath(p,ROOT)for p in batch if p.suffix=='.py']
 if py:
  more,e=closure(py);files|=more;edges.update(e)
manifest={'schema':'Q04_367_FIXED_TRANSITIVE_MANIFEST','files':{os.path.relpath(p,ROOT):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)},'import_edges':edges,'historical_opaque_json':['staging365_service_grammar/preregistered_v2.json', 'staging365_service_grammar/manifest_v2.json', 'staging365_service_grammar/v2_preserved/preregistered_v2.json', 'staging365_service_grammar/v2_preserved/manifest_v2.json', 'staging357_comparative/attached_service_candidate357.json', 'staging357_comparative/anchored_candidate357.json'],'historical_reason':'Independently audited path-specific retired preregistration; current source inventory hash-reads its bytes, active adapter does not parse or execute its retired internal pins. Its file bytes remain pinned; no current dependency mismatch exception.','scope':'SOURCE_JOINT367 intrinsic access cost ledger; finite baseline source359/362, no final necessity acceptance.'}
p=HERE/'q04_manifest367_v2.json';p.write_text(json.dumps(manifest,indent=2));print(hashlib.sha256(p.read_bytes()).hexdigest(),len(files))
