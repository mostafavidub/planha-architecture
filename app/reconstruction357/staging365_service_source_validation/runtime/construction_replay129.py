"""Exact hierarchical construction origin only; never operational admission."""
import copy
from construction_replay127 import digest,revision,ROOT
import hashlib
REQUIRED=('constructor129.py','coarse_master129.py','private_bundle129.py','assemble114.py','world_transform125.py','frame_contract125.py','common_core125.py','private_l3_source131.py','private_l3_hall131.py','coarse_l3_master131.py','private_l3_binding131.py','private_stagger_source132.py','private_stagger_hall132.py','coarse_stagger_master132.py','private_stagger_binding132.py','private_access_source132.py','coarse_access_master132.py','private_access_binding132.py','private_t_source133.py','private_t_hall133.py','coarse_t_master133.py','private_t_binding133.py','source_rotation133.py','checker_source133.py','place_module133.py','coarse_t_connected134.py','private_sidecar_source136.py','private_sidecar_hall136.py','private_sidecar_binding136.py','coarse_sidecar_master136.py','coarse_sidecar_seating136.py','shared_geometry137.py','shared_binding137.py','shared_producer137.py','coarse_sidecar_shared137.py','coarse_sidecar_group138.py','coarse_sidecar_rooted139.py','shared_gate140.py','rooted_bath139.py','seating_source142.py','seating_binding142.py','assemble142.py','coarse_sidecar_compact142.py','shared_gate142.py','local_routes142.py','nonseating144.py','private_branch_source146.py','private_branch_hall146.py','private_branch_binding146.py','world_record_schema147.json','assemble146.py','coarse_branch146.py','nonseating146.py','shared_gate146.py','coarse_branch_rooted149.py','assemble149.py','nonseating149.py','shared_gate149.py','circulation_frame148.py','shared_gate150.py','assemble144.py','public_witness144.py','coarse_sidecar_circulation144.py','shared_gate144.py','shared_gate145.py')
_CACHE={}
def verify(model,context):
 errors=[];rev=revision();mh=digest(model);trace=None
 try:
  if not isinstance(context,dict) or context.get('operation')!='generate_from_dimensions':raise ValueError('INTERNAL_DIMENSION_CONTEXT_REQUIRED')
  if context.get('baseline_model_hash')is not None or context.get('existing_plan_id')is not None:raise ValueError('REVISION_MISLABELED_NEW')
  trace=context['construction_trace']
  if trace['schema']!='CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1':raise ValueError('TRACE_SCHEMA')
  raw=trace['raw']
  if set(raw)!={'W','L','n','requested_count'}:raise ValueError('RAW_FIELD_INVENTORY')
  from contract114 import parse,S
  W,L,n=parse(raw)
  if n!=2 or type(raw['requested_count'])is not int or not 1<=raw['requested_count']<=12:raise ValueError('INTERNAL_RAW_SCOPE')
  if model['inputs']!=[S(W),S(L),n] or context['inputs']!=model['inputs']:raise ValueError('CANONICAL_INPUT_BINDING')
  if trace['source_revision']!=rev:raise ValueError('SOURCE_REVISION_CHANGED')
  if trace['model_hash']!=mh:raise ValueError('MODEL_HASH')
  sources=context['source_files']
  if not set(REQUIRED)<=set(sources):raise ValueError('SOURCE_INVENTORY')
  for name,sha in sources.items():
   p=(ROOT/name).resolve()
   if not p.is_relative_to(ROOT)or not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_HASH:'+name)
  p=trace['proposal']
  if p.get('status')!='PROPOSAL_ONLY'or p.get('bedrooms')!=3 or p.get('sleep_roles')!=(['twin','twin','double']if (p.get('ordered_macro')or{}).get('kind')=='L3_EXPERIMENTAL131'else['double','twin','twin']):raise ValueError('THREE_BED_SOURCE_PROGRAM_SCOPE')
  key=(rev,mh,digest(context))
  if key not in _CACHE:
   from constructor129 import build
   family=trace['family']
   if family not in ('FRONT_REAR','LEFT_RIGHT'):raise ValueError('OWNERSHIP_FAMILY')
   packet=build(copy.deepcopy(raw),family,copy.deepcopy(p))
   if digest(packet['world_model'])!=mh or digest(packet['local_model'])!=trace['local_model_hash'] or digest(packet['core'])!=trace['core_hash']:raise ValueError('WHOLE_CONSTRUCTION_REPLAY_MISMATCH')
   if packet.get('admission_claim')is not False:raise ValueError('CONSTRUCTOR_ADMISSION_CLAIM')
   if revision()!=rev:raise ValueError('SOURCE_CHANGED_DURING_REPLAY')
   _CACHE[key]=True
 except(KeyError,TypeError,ValueError,IndexError)as e:errors.append({'code':'HIERARCHICAL_CONSTRUCTION_BINDING','detail':str(e)})
 return {'verified':not errors,'errors':errors,'pending':[],'model_hash':mh,'source_revision':rev,'scope':'Exact current three-bedroom constructor replay, origin only; no solver, no transfer of macro or operation acceptance.','accepted':False}
