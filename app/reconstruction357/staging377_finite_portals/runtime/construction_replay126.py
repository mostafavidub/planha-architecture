"""Independent multi-proposal origin verifier, not a layout/operation checker.
A and B are ordered source assignments, not interchangeable receipt labels.
Only deterministic constructor replay is used; no solver is imported here.
"""
import copy,hashlib,json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
REQUIRED_SOURCES=('constructor126.py','assemble114.py','contract114.py','frame_contract125.py','common_core125.py','world_transform125.py')
_CACHE={}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def revision():
 files=[*ROOT.glob('*.py'),*ROOT.glob('*.json'),*(p for p in(ROOT/'references').rglob('*')if p.is_file())]
 return digest({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)})
def program(p):
 if not isinstance(p,dict)or p.get('status')!='PROPOSAL_ONLY':raise ValueError('NOT_ACTUAL_PROPOSAL')
 n=p.get('bedrooms');roles=p.get('sleep_roles')
 if type(n)is not int or not 1<=n<=4 or not isinstance(roles,list)or len(roles)!=n or any(r not in('double','twin')for r in roles):raise ValueError('PROPOSAL_PROGRAM_SCHEMA')
 return n,tuple(roles)
def verify(model,context):
 errors=[];trace=None;rev=revision();mh=digest(model)
 try:
  if not isinstance(context,dict)or context.get('operation')!='generate_from_dimensions':raise ValueError('NOT_INTERNAL_NEW_DIMENSION_CONTEXT')
  if context.get('baseline_model_hash')is not None or context.get('existing_plan_id')is not None:raise ValueError('REVISION_MISLABELED_NEW')
  trace=context['construction_trace']
  if trace['schema']!='CONSTRUCTION_TRACE126_PAIR_V1':raise ValueError('TRACE_SCHEMA')
  raw=trace['raw']
  if not isinstance(raw,dict)or set(raw)!={'W','L','n','requested_count'}:raise ValueError('DIMENSIONS_PROTOCOL_FIELDS_ONLY')
  from contract114 import parse,S
  W,L,n=parse(raw)
  if model['inputs']!=[S(W),S(L),n]or context['inputs']!=model['inputs']:raise ValueError('CANONICAL_RAW_INPUT_BINDING')
  if trace['family']not in('FRONT_REAR','LEFT_RIGHT'):raise ValueError('OWNERSHIP_FAMILY')
  if trace['source_revision']!=rev:raise ValueError('SOURCE_REVISION_CHANGED')
  if trace['model_hash']!=mh:raise ValueError('WORLD_MODEL_HASH')
  sources=context['source_files']
  if not set(REQUIRED_SOURCES)<=set(sources):raise ValueError('SOURCE_INVENTORY')
  for name,value in sources.items():
   path=(ROOT/name).resolve()
   if not path.is_relative_to(ROOT)or not path.is_file()or hashlib.sha256(path.read_bytes()).hexdigest()!=value:raise ValueError('SOURCE_HASH:'+name)
  proposals=trace['proposals']
  if set(proposals)!={'A','B'}:raise ValueError('UNIT_ASSIGNMENT_INVENTORY')
  pa,pb=program(proposals['A']),program(proposals['B'])
  if pa!=pb:raise ValueError('DIFFERENT_UNIT_PROGRAMS')
  hashes={u:digest(proposals[u])for u in('A','B')}
  if trace['unit_proposal_hashes']!=hashes:raise ValueError('ORDERED_UNIT_PROPOSAL_HASHES')
  key=(rev,mh,digest(context))
  if key not in _CACHE:
   from constructor126 import build
   packet=build(copy.deepcopy(raw),trace['family'],copy.deepcopy(proposals['A']),copy.deepcopy(proposals['B']))
   if packet['family']!=trace['family']or packet['unit_proposal_hashes']!=hashes:raise ValueError('CONSTRUCTOR_ASSIGNMENT_BINDING')
   if digest(packet['world_model'])!=mh or digest(packet['local_model'])!=trace['local_model_hash']or digest(packet['core'])!=trace['core_hash']:raise ValueError('WHOLE_PAIR_REPLAY_MISMATCH')
   if packet.get('admission_claim')is not False:raise ValueError('CONSTRUCTOR_MUST_NOT_ADMIT')
   if revision()!=rev:raise ValueError('SOURCE_CHANGED_DURING_REPLAY')
   _CACHE[key]=True
 except (KeyError,ValueError,TypeError,IndexError)as ex:errors.append({'code':'MULTIPROPOSAL_CONSTRUCTION_BINDING','detail':str(ex)})
 return {'verified':not errors,'errors':errors,'pending':[],'model_hash':mh,'trace_hash':digest(trace),'source_revision':rev,'scope':'Ordered A/B same-program deterministic whole-construction provenance only. No geometry, operation, privacy, diversity or admission receipt transferred. Separate fresh whole gate remains required.','accepted':False}
