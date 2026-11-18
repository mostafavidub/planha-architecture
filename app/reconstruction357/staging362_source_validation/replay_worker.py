"""Fixed HALL_CLAMP359 dispatch. Real rebuild, never legacy129 authority."""
import sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'staging362_core_notch'))
from adapter362 import replay,inventory,lineage
from contract114 import digest

def protected(model):
 return {'inputs':model['inputs'],'program':model['program'],'profile':model['profile'],'fixtures':{u['id']:u['fixtures']for u in model['units']},'activities':{u['id']:u['activities']for u in model['units']},'bedroom_rooms':{u['id']:{k:v for k,v in u['rooms'].items()if k.startswith('bed')}for u in model['units']},'unit_ids':[u['id']for u in model['units']],'room_ids':{u['id']:sorted(u['rooms'])for u in model['units']},'core_assets':{k:model['common_spaces'][k]for k in ('stair','lift')},'entries':{u['id']:u['entry_point']for u in model['units']}}
def run(record):
 if type(record)is not dict or type(record.get('candidate'))is not dict or type(record.get('trace'))is not dict:raise ValueError('REGISTERED_INPUT_RECORD_REQUIRED')
 trace=record['trace'];candidate=record['candidate']
 if trace.get('schema')!='ROW_CORE_NOTCH362_SOURCE_TRACE_V1':raise ValueError('UNREGISTERED_SCHEMA')
 before=inventory();rebuilt=replay(trace)['candidate']
 if digest(rebuilt)!=digest(candidate):raise ValueError('ACTUAL_CANDIDATE_REPLAY_BINDING')
 model=candidate['model'];packet=candidate['packet']
 if digest(model)!=candidate['model_digest']or digest(packet['world_model'])!=digest(model):raise ValueError('MODEL_PACKET_BINDING')
 if digest(candidate['request'])!=candidate['request_digest']or digest(candidate['request'])!=digest(trace['raw']):raise ValueError('RAW_BINDING')
 old=lineage();baseline=old['candidate']
 if trace['parent_record_digest']!=digest(old)or trace['parent_model_digest']!=digest(baseline['model']):raise ValueError('FIXED_PARENT_BINDING')
 if digest(baseline['request'])!=digest(candidate['request']):raise ValueError('PROTECTED_REQUEST_CHANGED')
 from protected362 import check
 ownership_proof=check(baseline, candidate)
 if digest(protected(baseline['model']))!=digest(protected(model)):raise ValueError('PROTECTED_PROGRAM_OWNERSHIP_ASSETS_OR_INPUT_CHANGED')
 if before!=inventory():raise ValueError('SOURCE_DRIFT_AFTER_REPLAY')
 return {'verified':True,'scope':'EXACT_NOTCH_REPLAY_PROTECTED_ASSETS_AND_NONDECREASE_NOT_FUNCTIONAL_ADMISSION','input_record_digest':digest(record),'outer_trace_digest':digest(trace),'candidate_digest':digest(candidate),'model_hash':digest(model),'packet_digest':digest(packet),'source_inventory':before,'raw':trace['raw'],'protected_vector_digest':digest(protected(model)),'baseline_model_digest':digest(baseline['model']),'parent_record_digest':digest(old),'schema':trace['schema'],'ownership_nondecrease':ownership_proof}
if __name__=='__main__':
 try:print(json.dumps(run(json.load(sys.stdin))))
 except Exception as e:print(json.dumps({'verified':False,'error':type(e).__name__+':'+str(e)}));sys.exit(1)
