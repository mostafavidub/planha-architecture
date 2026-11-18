"""Deterministic raw/proposal construction; no solver and no inherited receipts."""
from contract114 import parse,digest
from frame_contract125 import local_core
from assemble114 import assemble
from world_transform125 import to_world

def build(raw,proposal):
 W,L,n=parse(raw)
 core=local_core(W,L)
 local=assemble(L,W,core,proposal)
 world=to_world(local,core)
 return {'local_model':local,'world_model':world,'core':core}

def context(raw,proposal,packet):
 from pathlib import Path
 import hashlib
 from engine114 import revision
 root=Path(__file__).resolve().parent
 names=['engine114.py','assemble114.py','constructor125.py','frame_contract125.py','common_core125.py','world_transform125.py']
 return {'operation':'generate_from_dimensions','inputs':packet['world_model']['inputs'],'baseline_model_hash':None,'existing_plan_id':None,
  'source_files':{n:hashlib.sha256((root/n).read_bytes()).hexdigest()for n in names},
  'construction_trace':{'schema':'CONSTRUCTION_TRACE125_WORLD_V1','raw':raw,'proposal':proposal,'local_model_hash':digest(packet['local_model']),'model_hash':digest(packet['world_model']),'core_hash':digest(packet['core']),'source_revision':revision()}}
