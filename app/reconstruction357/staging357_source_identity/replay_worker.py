"""Fixed producer dispatch in a separate interpreter; no receipt import."""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'staging357_comparative'))
from translated_adapter import replay,sources
from translated_validator import verify
from contract114 import digest

def run(record):
 if type(record)is not dict or type(record.get('candidate'))is not dict or type(record.get('trace'))is not dict:raise ValueError('REGISTERED_INPUT_RECORD_REQUIRED')
 trace=record['trace'];candidate=record['candidate']
 if trace.get('schema')!='TRANSLATED_PRIVATE357_SOURCE_TRACE_V1':raise ValueError('UNREGISTERED_SCHEMA')
 before=sources();rebuilt=replay(trace)['candidate']
 if digest(rebuilt)!=digest(candidate):raise ValueError('ACTUAL_CANDIDATE_REPLAY_BINDING')
 model=candidate['model'];packet=candidate['packet']
 if digest(model)!=candidate['model_digest'] or digest(packet['world_model'])!=digest(model):raise ValueError('MODEL_PACKET_BINDING')
 if digest(candidate['request'])!=candidate['request_digest'] or digest(candidate['request'])!=digest(trace['raw']):raise ValueError('RAW_BINDING')
 v=verify(model,trace)
 if v['errors']:raise ValueError('SOURCE_PRIMITIVE_BINDING:'+str(v['errors']))
 if before!=sources():raise ValueError('SOURCE_DRIFT_AFTER_REPLAY')
 return {'verified':True,'scope':'EXACT_REPLAY_AND_SOURCE_PRIMITIVE_NOT_FUNCTIONAL_ADMISSION','input_record_digest':digest(record),'outer_trace_digest':digest(trace),'candidate_digest':digest(candidate),'model_hash':digest(model),'packet_digest':digest(packet),'source_inventory':before,'raw':trace['raw'],'primitive':v,'schema':trace['schema']}
if __name__=='__main__':
 try:print(json.dumps(run(json.load(sys.stdin))))
 except Exception as e:print(json.dumps({'verified':False,'error':type(e).__name__+':'+str(e)}));sys.exit(1)
