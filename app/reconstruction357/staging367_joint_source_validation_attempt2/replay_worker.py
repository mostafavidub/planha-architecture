"""JOINT367 exact ordered source reconstruction; not a donor-profile receipt."""
import sys,json
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent
sys.path.insert(0,str(ROOT/'staging367_service_joint_attempt2'))
from joint367 import replay,inventory,original,protect,SCHEMA
from contract114 import digest

def run(record):
 if type(record)is not dict or type(record.get('trace'))is not dict or record['trace'].get('schema')!=SCHEMA:raise ValueError('JOINT367_SCHEMA_REQUIRED')
 c=record['candidate'];t=record['trace'];before=inventory();rebuilt=replay(t)
 if digest(rebuilt['trace'])!=digest(t)or digest(rebuilt['candidate'])!=digest(c):raise ValueError('JOINT367_FULL_REPLAY_MISMATCH')
 parent=original();raw=c['request']
 if type(raw)is not dict or set(raw)!={'W','L','n','requested_count'}or any(type(raw[k])is not type(v)or raw[k]!=v for k,v in {'W':'26','L':'28','n':2,'requested_count':2}.items()):raise ValueError('EXACT_REGISTERED_RAW')
 if digest(raw)!=c['request_digest']or digest(raw)!=digest(parent['candidate']['request']):raise ValueError('SOURCE_RAW_PARENT_BINDING')
 m=c['model'];packet=c['packet']
 if digest(m)!=c['model_digest']or digest(packet['world_model'])!=digest(m)or digest(packet['local_model'])!=digest(m):raise ValueError('FRONT_REAR_EXACT_FRAME')
 if t['parent_record_digest']!=digest(parent):raise ValueError('PARENT_RECORD')
 protection=protect(parent['candidate']['model'],m,ownership_equal=False)
 if before!=inventory():raise ValueError('PRODUCER_DRIFT')
 return {'verified':True,'schema':SCHEMA,'scope':'EXACT_ORDERED_JOINT367_SOURCE_REPLAY_AND_PROTECTED_PROGRAM_NOT_ADMISSION','input_record_digest':digest(record),'outer_trace_digest':digest(t),'candidate_digest':digest(c),'model_hash':digest(m),'packet_digest':digest(packet),'local_model_digest':digest(packet['local_model']),'core_digest':digest(packet['core']),'raw':raw,'source_inventory':before,'parent_record_digest':digest(parent),'ordered_stages':t['stages'],'protected':protection}
if __name__=='__main__':
 try:print(json.dumps(run(json.load(sys.stdin))))
 except Exception as e:print(json.dumps({'verified':False,'error':type(e).__name__+':'+str(e)}));sys.exit(1)
