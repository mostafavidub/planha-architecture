"""Two actual ownership grammars; independently supplied same-program unit proposals."""
from contract114 import parse,core_first,full_band_core_first,digest
from frame_contract125 import local_core
from assemble114 import assemble
from world_transform125 import to_world
FAMILIES=('FRONT_REAR','LEFT_RIGHT')
def frame(raw,family,*,core_choice=None):
 W,L,n=parse(raw)
 if n!=2:raise ValueError('N2_ONLY')
 if core_choice is not None and (family!='FRONT_REAR' or core_choice not in ('COMPACT','FULL_BAND')):
  raise ValueError('UNKNOWN_CORE_CHOICE')
 if family=='LEFT_RIGHT':return local_core(W,L),(L,W)
 if family=='FRONT_REAR':
  c=(full_band_core_first if core_choice=='FULL_BAND' else core_first)(W,L)
  if c is None:raise ValueError('FRONT_REAR_SCOPE_NO_CORE')
  return c,(W,L)
 raise ValueError('UNKNOWN_OWNERSHIP_FAMILY')
def build(raw,family,proposal_a,proposal_b,*,core_choice=None):
 core,(w,l)=frame(raw,family,core_choice=core_choice)
 local=assemble(w,l,core,proposal_a,unit_proposals={'A':proposal_a,'B':proposal_b})
 world=to_world(local,core) if family=='LEFT_RIGHT' else local
 return {'family':family,'local_model':local,'world_model':world,'core':core,'unit_proposal_hashes':{'A':digest(proposal_a),'B':digest(proposal_b)},'admission_claim':False}
def context(raw,packet,proposals,*,core_choice=None):
 from engine114 import revision
 import hashlib
 from pathlib import Path
 root=Path(__file__).parent
 sources={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['constructor127.py','assemble114.py','contract114.py','frame_contract125.py','common_core125.py','world_transform125.py']}
 return {'operation':'generate_from_dimensions','inputs':packet['world_model']['inputs'],'baseline_model_hash':None,'existing_plan_id':None,'source_files':sources,'construction_trace':{'schema':'CONSTRUCTION_TRACE127_PAIR_V2' if core_choice is not None else 'CONSTRUCTION_TRACE127_PAIR_V1',**({'core_choice':core_choice} if core_choice is not None else {}),'raw':raw,'family':packet['family'],'proposals':proposals,'unit_proposal_hashes':packet['unit_proposal_hashes'],'local_model_hash':digest(packet['local_model']),'model_hash':digest(packet['world_model']),'core_hash':digest(packet['core']),'source_revision':revision()}}
