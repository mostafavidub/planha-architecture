"""Explicit independent source lineage. Reconstruction only, never admission."""
import json,hashlib
from pathlib import Path
from constructor366 import build,inputs
from contract114 import digest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;RUNTIME=ROOT/'planha_general150_runtime_work'
SCHEMA='SOURCE_SERVICE_BALANCED366_TRACE_V1'
def inventory():
 files=list(RUNTIME.glob('*.py'))+list(RUNTIME.glob('*.json'))+[p for p in (RUNTIME/'references').rglob('*')if p.is_file()]
 files += [HERE/n for n in ('constructor366.py','assemble366.py','entry366.py','selector366.py','selector_input_pins.json','actual_selection366.json','actual_domain366.json','union_domain.py','operation_domain366.py','adapter366.py')]
 files += [ROOT/'staging365_service_grammar/candidate365.json']
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)}
def construct():
 sources=inventory();r,s=inputs();packet=build();model=packet['world_model'];raw=r['candidate']['request']
 candidate={'request':raw,'request_digest':digest(raw),'packet':packet,'model':model,'model_digest':digest(model)}
 trace={'schema':SCHEMA,'parent_record_digest':digest(r),'source_inventory':sources,'raw':raw,'selection':s,'candidate_digest':digest(candidate),'model_digest':digest(model),'packet_digest':digest(packet),'preserved_core_assets':True,'tail_and_branch_role':'UNRESOLVED_ORIGINAL_GEOMETRY_RETAINED','admission_claim':False}
 if inventory()!=sources:raise ValueError('SOURCE_CHANGED_DURING_BUILD')
 return {'candidate':candidate,'trace':trace,'accepted':False,'delivery_allowed':False}
def replay(trace):
 if trace.get('schema')!=SCHEMA or trace.get('source_inventory')!=inventory():raise ValueError('UNREGISTERED_SOURCE_OR_DRIFT')
 result=construct()
 if digest(result['trace'])!=digest(trace):raise ValueError('FULL_TRACE_REPLAY_MISMATCH')
 return result
