"""Service grammar only. Reconstruct source365; never borrow balanced/legacy authority."""
import sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'staging365_service_grammar'))
from adapter365 import replay,inventory,validate_raw
from contract114 import digest

def run(record):
 if type(record)is not dict or type(record.get('candidate'))is not dict or type(record.get('trace'))is not dict:raise ValueError('REGISTERED_RECORD_REQUIRED')
 t=record['trace'];c=record['candidate']
 if t.get('schema')!='SOURCE_SERVICE_ANCHOR365_TRACE_V1':raise ValueError('UNREGISTERED_SERVICE_SCHEMA')
 validate_raw(t['raw']);before=inventory();r=replay(t)
 if digest(r['candidate'])!=digest(c)or digest(r['trace'])!=digest(t):raise ValueError('EXACT_SERVICE_REPLAY_BINDING')
 m=c['model'];p=c['packet']
 if digest(m)!=c['model_digest']or digest(p['world_model'])!=digest(m):raise ValueError('CURRENT_MODEL_PACKET_BINDING')
 if digest(c['request'])!=c['request_digest']or digest(c['request'])!=digest(t['raw']):raise ValueError('CURRENT_RAW_BINDING')
 if m['program']['bedrooms_per_unit']!=3 or m['program']['sleep_roles']!=['double','twin','twin']or m['profile']['body_m']!='.7':raise ValueError('SOURCE_PROGRAM_PROFILE')
 if before!=inventory():raise ValueError('SOURCE_DRIFT')
 return {'verified':True,'scope':'EXACT_SERVICE365_RECONSTRUCTION_SOURCE_ASSETS_AND_CONSTRAINTS_NOT_ADMISSION','schema':t['schema'],'input_record_digest':digest(record),'outer_trace_digest':digest(t),'candidate_digest':digest(c),'model_hash':digest(m),'packet_digest':digest(p),'local_model_digest':digest(p['local_model']),'core_digest':digest(p['core']),'source_inventory':before,'raw':t['raw'],'source_anchor_digest':digest(t['anchor_contract'])}
if __name__=='__main__':
 try:print(json.dumps(run(json.load(sys.stdin))))
 except Exception as e:print(json.dumps({'verified':False,'error':type(e).__name__+':'+str(e)}));sys.exit(1)
