"""Deterministic decomposition of a coarse-master proposal; never admits it."""
from pathlib import Path
import hashlib
from contract114 import parse,core_first,S,digest
from assemble114 import assemble

def build(raw,proposal):
 if not isinstance(raw,dict)or set(raw)!={'W','L','n','requested_count'}:raise ValueError('RAW_DIMENSION_FIELDS')
 W,L,n=parse(raw)
 if n!=2 or type(raw['requested_count'])is not int or not 1<=raw['requested_count']<=12:raise ValueError('SUPPORTED_INPUT_SCOPE')
 if proposal.get('bedrooms')!=3 or proposal.get('sleep_roles')!=['double','twin','twin']or proposal.get('capacity_profile')!='SIX_PERSON_INTERNAL_PROGRAM121':raise ValueError('HIERARCHICAL_STUDY_PROGRAM')
 core=core_first(W,L)
 if core is None:raise ValueError('FRONT_REAR_CORE_UNSUPPORTED')
 model=assemble(W,L,core,proposal)
 return {'model':model,'core':core,'admission_claim':False,'generation_method':'COARSE_BUNDLE_MASTER_WITH_FULL_OPERATIONAL_DECOMPOSITION'}
def context(raw,proposal,packet):
 from engine114 import revision
 root=Path(__file__).parent;names=['constructor128.py','coarse_master128.py','assemble114.py','contract114.py','private_hall_producer121.py','ordered_macro121.py']
 return {'operation':'generate_from_dimensions','inputs':packet['model']['inputs'],'baseline_model_hash':None,'existing_plan_id':None,'source_files':{n:hashlib.sha256((root/n).read_bytes()).hexdigest()for n in names},'construction_trace':{'schema':'CONSTRUCTION_TRACE128_HIERARCHICAL_V1','raw':raw,'proposal':proposal,'model_hash':digest(packet['model']),'core_hash':digest(packet['core']),'source_revision':revision()}}
