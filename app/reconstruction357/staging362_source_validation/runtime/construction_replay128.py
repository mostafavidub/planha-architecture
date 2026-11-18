"""Exact hierarchical construction origin only; never operational admission."""
import copy
from construction_replay127 import digest,revision,ROOT
import hashlib
REQUIRED=('constructor128.py','assemble114.py','contract114.py','ordered_macro121.py','coarse_master128.py')
_CACHE={}
def verify(model,context):
 errors=[];rev=revision();mh=digest(model);trace=None
 try:
  if not isinstance(context,dict) or context.get('operation')!='generate_from_dimensions':raise ValueError('INTERNAL_DIMENSION_CONTEXT_REQUIRED')
  if context.get('baseline_model_hash')is not None or context.get('existing_plan_id')is not None:raise ValueError('REVISION_MISLABELED_NEW')
  trace=context['construction_trace']
  if trace['schema']!='CONSTRUCTION_TRACE128_HIERARCHICAL_V1':raise ValueError('TRACE_SCHEMA')
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
  if p.get('status')!='PROPOSAL_ONLY'or p.get('bedrooms')!=3 or p.get('sleep_roles')!=['double','twin','twin']:raise ValueError('THREE_BED_SOURCE_PROGRAM_SCOPE')
  key=(rev,mh,digest(context))
  if key not in _CACHE:
   from constructor128 import build
   packet=build(copy.deepcopy(raw),copy.deepcopy(p))
   if digest(packet['model'])!=mh or digest(packet['core'])!=trace['core_hash']:raise ValueError('WHOLE_CONSTRUCTION_REPLAY_MISMATCH')
   if packet.get('admission_claim')is not False:raise ValueError('CONSTRUCTOR_ADMISSION_CLAIM')
   if revision()!=rev:raise ValueError('SOURCE_CHANGED_DURING_REPLAY')
   _CACHE[key]=True
 except(KeyError,TypeError,ValueError,IndexError)as e:errors.append({'code':'HIERARCHICAL_CONSTRUCTION_BINDING','detail':str(e)})
 return {'verified':not errors,'errors':errors,'pending':[],'model_hash':mh,'source_revision':rev,'scope':'Exact current three-bedroom constructor replay, origin only; no solver, no transfer of macro or operation acceptance.','accepted':False}
