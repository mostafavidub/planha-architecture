"""Fixed ROW358 source dispatch; no translated357 or JSON-verdict authority."""
import sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'staging358_comparative'))
from row_adapter358 import replay,inventory,validate
from contract114 import digest

def protected(model):
 return {'inputs':model['inputs'],'program':model['program'],'ownership':{u['id']:u['ownership']for u in model['units']},'unit_ids':[u['id']for u in model['units']],'room_ids':{u['id']:sorted(u['rooms'])for u in model['units']},'common_spaces':model['common_spaces']}
def run(record):
 if type(record)is not dict or type(record.get('candidate'))is not dict or type(record.get('trace'))is not dict:raise ValueError('REGISTERED_INPUT_RECORD_REQUIRED')
 trace=record['trace'];candidate=record['candidate']
 if trace.get('schema')!='ROW_BODY358_SOURCE_TRACE_V1':raise ValueError('UNREGISTERED_SCHEMA')
 before=inventory();rebuilt=replay(trace)['candidate']
 if digest(rebuilt)!=digest(candidate):raise ValueError('ACTUAL_CANDIDATE_REPLAY_BINDING')
 model=candidate['model'];packet=candidate['packet']
 if digest(model)!=candidate['model_digest']or digest(packet['world_model'])!=digest(model):raise ValueError('MODEL_PACKET_BINDING')
 if digest(candidate['request'])!=candidate['request_digest']or digest(candidate['request'])!=digest(trace['raw']):raise ValueError('RAW_BINDING')
 core=validate(trace['raw'],trace['proposal'])
 if digest(core)!=digest(packet['core']):raise ValueError('SOURCE_CORE_BINDING')
 baseline=json.loads((BASE/'actual_run/actual_response.json').read_text())['selected'][0]
 if digest(baseline['request'])!=digest(candidate['request']):raise ValueError('PROTECTED_REQUEST_CHANGED')
 if digest(protected(baseline['model']))!=digest(protected(model)):raise ValueError('PROTECTED_PROGRAM_OWNERSHIP_OR_INPUT_CHANGED')
 if before!=inventory():raise ValueError('SOURCE_DRIFT_AFTER_REPLAY')
 return {'verified':True,'scope':'EXACT_ROW_REPLAY_AND_PROTECTED_PROGRAM_NOT_FUNCTIONAL_ADMISSION','input_record_digest':digest(record),'outer_trace_digest':digest(trace),'candidate_digest':digest(candidate),'model_hash':digest(model),'packet_digest':digest(packet),'source_inventory':before,'raw':trace['raw'],'protected_vector_digest':digest(protected(model)),'baseline_model_digest':digest(baseline['model']),'schema':trace['schema']}
if __name__=='__main__':
 try:print(json.dumps(run(json.load(sys.stdin))))
 except Exception as e:print(json.dumps({'verified':False,'error':type(e).__name__+':'+str(e)}));sys.exit(1)
