"""Task4.2 typed protected-state contract, not child provenance or model acceptance.
Geometry may move; unchanged instance dimensions/programme/profile/core are required.
Original replay and full gates are separate mandatory task4.3 execution obligations.
"""
import copy,hashlib,inspect
from fractions import Fraction as F
from pathlib import Path
from front_rear_runtime_adapter import ROOT,transport,ensure
from same_version_front_rear_contract import digest
from explicit_pair_redirection import inventory
SELECTION_SOURCES={'app/local_integration/'+p for p in ('rejection_operator_selection.py','explicit_pair_redirection.py','live_program_scheduler.py','current_four_decision.py','candidate/four_seat_group_candidate.py')}
def verify_selection_sources(value):
 ensure(type(value) is dict and set(value)==SELECTION_SOURCES,'SELECTION_SOURCE_SET')
 for path,h in value.items():ensure(type(h) is str and hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,'SELECTION_SOURCE_CHANGED:'+path)
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
SOURCES=['app/local_integration/protected_repair_contract.py','app/local_integration/explicit_pair_redirection.py']
def snapshot():
 return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES}
def protected(packet):
 packet=transport(packet)[0]
 model=packet['world_model'];units=model['units']
 ensure(type(units) is list and len(units)==2,'PROTECTED_UNIT_COUNT')
 ids=[u['id'] for u in units]
 ensure(all(type(x) is str for x in ids) and len(set(ids))==2 and set(ids)=={'A','B'},'PROTECTED_UNIT_IDS')
 ensure(model.get('accepted') is False and model.get('release_allowed') is False,'MODEL_AUTHORITY')
 ensure(Path(inspect.getsourcefile(inventory)).resolve()==(ROOT/SOURCES[1]).resolve(),'INVENTORY_IMPORT')
 for u in units:
  ensure(type(u['fixtures']) is dict and type(u['fixture_metadata']) is dict and set(u['fixtures'])==set(u['fixture_metadata']),'FIXTURE_ID_SET')
  for fid,q in u['fixtures'].items():
   ensure(type(fid) is str and type(q) is list and len(q)==4,'FIXTURE_RECT_SHAPE')
   ensure(all(type(v) in (str,int,float) for v in q),'FIXTURE_COORD_TYPE')
   z=[F(str(v)) for v in q];ensure(z[2]>z[0] and z[3]>z[1],'FIXTURE_POSITIVE_RECT')
   md=u['fixture_metadata'][fid]
   ensure(type(md) is dict and type(md.get('kind')) is str and md['kind'],'FIXTURE_KIND')
 # Inventory source uses actual rectangle dimensions, not metadata counts alone.
 return {'inputs':copy.deepcopy(model['inputs']),'program':copy.deepcopy(model['program']),
  'profile':copy.deepcopy(model['profile']),'fixture_inventory':inventory(model),
  'core_digest':digest(packet['core']),'unit_count':2}
def freeze_parent(selection,runtime,*,expected_selection_digest,expected_runtime_digest):
 selection=transport(selection)[0];runtime=transport(runtime)[0];pin=digest([selection,runtime])
 before=snapshot()
 verify_selection_sources(selection['source_snapshot'])
 ensure(digest(selection)==expected_selection_digest and digest(runtime)==expected_runtime_digest,'PARENT_RECEIPTS')
 ensure(selection['schema']=='SOURCE_BOUND_REJECTION_OPERATOR_SELECTION_V1' and selection['integrity_verified'] is True,'SELECTION_INTEGRITY')
 ensure(all(selection.get(k) is False for k in AUTH),'SELECTION_AUTHORITY')
 ensure(selection['selected_operator']['execution_started'] is False and selection['selected_operator']['child_generated'] is False,'NOT_EXECUTED_SELECTION')
 packet=runtime['packet'];mh=digest(packet['world_model'])
 ensure(mh==runtime['model_digest']==selection['parent_model_digest'],'PARENT_MODEL_BINDING')
 ensure(digest(runtime['context'])==selection['parent_context_digest'],'PARENT_CONTEXT_BINDING')
 ensure(digest(runtime['reports']['physical'])==selection['full_physical_digest']==digest(selection['full_physical_report']),'ORIGINAL_PHYSICAL_BINDING')
 value=protected(packet)
 ensure(digest(value)==selection['protected_digest']==digest(selection['protected']),'PROTECTED_SELECTION_BINDING')
 out={'schema':'TYPED_FIXED_PROGRAM_REPAIR_CONTRACT_V1','parent_model_digest':mh,
  'parent_context_digest':selection['parent_context_digest'],'parent_attempt_id':selection['parent_attempt_id'],
  'selection_digest':digest(selection),'runtime_digest':digest(runtime),
  'operator_id':selection['selected_operator']['id'],'protected':value,'protected_digest':digest(value),
  'source_snapshot':before,'selection_source_snapshot':copy.deepcopy(selection['source_snapshot']),'scope':'Exact typed inputs/programme/profile/core and instance IDs/kinds/source-size plus exact rational actual dimensions. Position may change. This is not independent fixture provenance, activity adequacy, replay, physical or current-functional acceptance.',
  'requires_fresh_child_replay_and_all_gates':True,'lower_program_is_repair':False,**{k:False for k in AUTH}}
 verify_selection_sources(selection['source_snapshot'])
 ensure(digest([selection,runtime])==pin and snapshot()==before,'PARENT_CONTRACT_INTEGRITY')
 return out
def verify_child(contract,expected_contract_digest,packet,context):
 contract=transport(contract)[0];packet=transport(packet)[0];context=transport(context)[0]
 pin=digest([contract,packet,context])
 ensure(digest(contract)==expected_contract_digest,'CONTRACT_RECEIPT')
 ensure(contract['schema']=='TYPED_FIXED_PROGRAM_REPAIR_CONTRACT_V1','CONTRACT_SCHEMA')
 ensure(all(contract.get(k) is False for k in AUTH),'CONTRACT_AUTHORITY')
 ensure(contract['source_snapshot']==snapshot(),'CONTRACT_SOURCE_CHANGED')
 verify_selection_sources(contract['selection_source_snapshot'])
 ensure(digest(contract['protected'])==contract['protected_digest'],'CONTRACT_PROTECTED_DIGEST')
 mh=digest(packet['world_model']);trace=context['construction_trace']
 ensure(trace['model_hash']==mh,'CHILD_CONTEXT_MODEL_BINDING')
 actual=protected(packet)
 ensure(digest(actual)==contract['protected_digest'],'PROTECTED_TYPED_STATE_CHANGED')
 verify_selection_sources(contract['selection_source_snapshot'])
 ensure(digest([contract,packet,context])==pin and contract['source_snapshot']==snapshot(),'CHILD_CONTRACT_INTEGRITY')
 return {'schema':'TYPED_REPAIR_PRESERVATION_RESULT_V1','protected_state_verified':True,
  'parent_model_digest':contract['parent_model_digest'],'child_model_digest':mh,
  'model_changed':mh!=contract['parent_model_digest'],'contract_digest':digest(contract),
  'fresh_origin_verified':False,'physical_verified':False,'current_requirements_verified':False,
  'scope':'Preservation only. No permission to skip fresh original provenance, evaluator or current four checks.',
  **{k:False for k in AUTH}}
