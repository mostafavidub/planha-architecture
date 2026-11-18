"""Explicit359 source reconstruction, fixed358 proposal lineage, no solver.
Only construct/replay may generate. context129 is never reused as authority.
"""
import sys,json,copy,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;ROOT=BASE/'planha_general150_runtime_work'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from contract114 import digest
from constructor359 import build
LINEAGE=BASE/'staging358_comparative/row_candidate358.json'
LINEAGE_SHA='5780193d5256cece965966222a1d9654748aa5d5b1543bce0b80c6b9fcb11387'
FILES=('adapter359.py','constructor359.py','assemble359.py','private_hall_producer359.py','clamp_geometry359.py','operation_reservations359.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory():
 files=[*ROOT.glob('*.py'),*ROOT.glob('*.json'),*(p for p in(ROOT/'references').rglob('*')if p.is_file()),*(HERE/n for n in FILES),LINEAGE,BASE/'staging358_comparative/row_adapter358.py',BASE/'staging358_comparative/row_body358.py']
 return {str(p.relative_to(BASE)):sha(p)for p in sorted(set(files))}
def lineage():
 if sha(LINEAGE)!=LINEAGE_SHA:raise ValueError('FIXED358_LINEAGE_FILE')
 r=json.loads(LINEAGE.read_text());t=r['trace'];c=r['candidate']
 if t['schema']!='ROW_BODY358_SOURCE_TRACE_V1'or digest(c)!=t['candidate_digest']or digest(c['model'])!=t['model_digest']:raise ValueError('LINEAGE_BINDING')
 for name,h in t['source_inventory'].items():
  if sha(BASE/name)!=h:raise ValueError('LINEAGE_SOURCE_DRIFT:'+name)
 return r

def construct():
 old=lineage();sources=inventory();raw=copy.deepcopy(old['trace']['raw']);proposal=copy.deepcopy(old['trace']['proposal'])
 packet=build(raw,'FRONT_REAR',proposal)
 context={'schema':'EXPLICIT359_HALL_CLAMP_GENERATION_CONTEXT','producer':'constructor359.build','private_source':'private_hall_producer359.install','parent_record_digest':digest(old),'parent_model_digest':old['candidate']['model_digest'],'fixed_proposal_digest':digest(proposal),'source_inventory':sources,'transformation':'SOURCE121_HALL_BOUNDS_FROM_REQUIRED_PORT_PATH_BODY_AND_OPERATION_ENVELOPES; REBUILD_ALL_DOWNSTREAM_ASSEMBLY','excluded_authority':'constructor129.context legacy source receipt','released_floor_function':'UNKNOWN_UNTIL_INDEPENDENT_ROLE_REVIEW','accepted':False}
 candidate={'request':raw,'request_digest':digest(raw),'packet':packet,'model':packet['world_model'],'model_digest':digest(packet['world_model']),'generation_context':context}
 if inventory()!=sources:raise ValueError('SOURCE_CHANGED_DURING_BUILD')
 trace={'schema':'ROW_HALL_CLAMP359_SOURCE_TRACE_V1','raw':raw,'proposal':proposal,'parent_record_digest':digest(old),'parent_model_digest':old['candidate']['model_digest'],'source_inventory':sources,'candidate_digest':digest(candidate),'model_digest':candidate['model_digest'],'max_distinct_candidate_attempts':1,'solver_used':False,'accepted':False}
 return {'candidate':candidate,'trace':trace,'accepted':False}
def replay(trace):
 if trace['schema']!='ROW_HALL_CLAMP359_SOURCE_TRACE_V1'or trace['source_inventory']!=inventory():raise ValueError('TRACE_SOURCE_BINDING')
 old=lineage()
 if trace['parent_record_digest']!=digest(old)or trace['proposal']!=old['trace']['proposal']or trace['raw']!=old['trace']['raw']:raise ValueError('FIXED_LINEAGE_PARAMETERS')
 x=construct()
 if x['trace']!=trace:raise ValueError('EXACT_REPLAY_MISMATCH')
 return x
