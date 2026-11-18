"""Registered source-family construction and independent deterministic replay.
No controlled perturbation, no prior failure inputs, no inherited semantic PASS.
"""
import copy,hashlib,json,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from family378 import load_parent,validate_request,enumerate_family,actual_selection
from contract114 import digest
from constructor378 import build
SCHEMA='FINITE_PORTALS378_SOURCE_TRACE_V1'
def inventory():
 parent=load_parent();paths={ROOT/n for n in parent['trace']['source_inventory']}
 paths.add(ROOT/'staging362_core_notch/actual362.json')
 paths.update(ROOT/n for n in ('semantic_rules357/modules_spatial.py','semantic_rules357/common.py'))
 paths.update(p for p in HERE.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.suffix not in('.pyc','.pyo'))
 # Include entire assembly/helper source trees and ALL non-code references.
 for folder in ('staging362_core_notch','staging365_balanced_portals','staging359_hall_clamp','planha_general150_runtime_work'):
  paths.update(p for p in (ROOT/folder).rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.suffix not in('.pyc','.pyo'))
 for n,want in parent['trace']['source_inventory'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=want:raise ValueError('PARENT_SOURCE_DRIFT:'+n)
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(paths)}
def require_protected(parent,model):
 prior=parent['candidate']['model']
 for k in ('inputs','profile','program'):
  if digest(model[k])!=digest(prior[k]):raise ValueError('PROTECTED_MODEL:'+k)
 for k in ('stair','lift'):
  if model['common_spaces'][k]!=prior['common_spaces'][k]:raise ValueError('PROTECTED_CORE_ASSET:'+k)
 if [u['id']for u in model['units']]!=[u['id']for u in prior['units']]:raise ValueError('PROTECTED_UNIT_IDS')
 for u in model['units']:
  old=next(v for v in prior['units']if v['id']==u['id'])
  for k in ('fixtures','activities','ownership'):
   if digest(u[k])!=digest(old[k]):raise ValueError('PROTECTED_UNIT_ASSET:'+u['id']+':'+k)
  for name in old['rooms']:
   if name.startswith('bed')and u['rooms'].get(name)!=old['rooms'][name]:raise ValueError('PROTECTED_BEDROOM')

def construct(raw,run_id):
 validate_request(raw)
 if str(uuid.UUID(run_id))!=run_id:raise ValueError('RUN_ID')
 parent=load_parent();before=inventory();choices=enumerate_family(parent);selection=choices[1]
 proposal=copy.deepcopy(parent['trace']['proposal'])
 # Existing room/seating proposal is fixed; only explicit core parameters vary.
 packet=build(raw,'FRONT_REAR',proposal,selection);model=packet['world_model']
 require_protected(parent,model)
 c={'request':copy.deepcopy(raw),'request_digest':digest(raw),'packet':packet,'model':model,'model_digest':digest(model),
    'generation_context':{'schema':'FINITE_PORTALS378_CONTEXT','run_id':run_id,'parent_record_digest':digest(parent),'selection':selection,'constraints_complete':False,'solver_used':False,'legacy_context_used':False}}
 trace={'schema':SCHEMA,'raw':copy.deepcopy(raw),'run_id':run_id,'source_inventory':before,'parent_record_digest':digest(parent),'parent_model_digest':parent['candidate']['model_digest'],
        'enumeration':choices,'selection_rank':1,'proposal':proposal,'proposal_digest':digest(proposal),'candidate_digest':digest(c),'model_digest':digest(model),'packet_digest':digest(packet),'solver_used':False}
 identity=digest({'run_id':run_id,'request_digest':digest(raw),'model_digest':digest(model),'trace_digest':digest(trace)})
 r={'candidate':c,'trace':trace,'candidate_id':identity,'test_only':False,'experimental':True,'accepted':False,'delivery_allowed':False,'request_fulfilled':False,'branch_count':1,'requested_count':2,'semantic_qualification':'UNKNOWN_NOT_EXECUTED'}
 if inventory()!=before:raise ValueError('SOURCE_DRIFT')
 return r

def replay(record):
 if type(record)is not dict or record.get('trace',{}).get('schema')!=SCHEMA:raise ValueError('UNREGISTERED_SOURCE')
 t=record['trace']
 if t.get('source_inventory')!=inventory():raise ValueError('SOURCE_INVENTORY_CHANGED')
 built=construct(t['raw'],t['run_id'])
 if digest(built)!=digest(record):raise ValueError('EXACT_REPLAY_MISMATCH')
 return built

def proof(record):
 replay(record);c=record['candidate'];t=record['trace']
 return {'verified':True,'schema':SCHEMA,'input_record_digest':digest(record),'outer_trace_digest':digest(t),'candidate_digest':digest(c),'model_hash':digest(c['model']),
         'packet_digest':digest(c['packet']),'raw':c['request'],'run_id':t['run_id'],'candidate_id':record['candidate_id'],'parent_record_digest':t['parent_record_digest'],'test_only':False,
         'scope':'FINITE_SOURCE_RECONSTRUCTION_ONLY_NOT_QUALITY'}

def repair_dispatch(record,fresh):
 # This is an internal same-run receipt validator, not a caller-proof API.
 from evaluate378 import registry_for
 from source_registry365 import payload_for
 c=record['candidate'];t=record['trace'];raw=fresh.get('raw_report',{});proof=fresh.get('provenance',{})
 bound={'input_record_digest':digest(record),'outer_trace_digest':digest(t),'candidate_digest':digest(c),'model_hash':digest(c['model']),
        'packet_digest':digest(c['packet']),'raw':c['request'],'run_id':t['run_id'],'candidate_id':record['candidate_id'],'parent_record_digest':t['parent_record_digest']}
 if proof.get('verified')is not True or proof.get('schema')!=SCHEMA or any(proof.get(k)!=v for k,v in bound.items()):raise ValueError('CURRENT_PROVENANCE_BINDING')
 if fresh.get('schema')!='FINITE378_CURRENT_SOURCE_VALIDATION' or fresh.get('input_record_digest')!=digest(record)or fresh.get('model_digest')!=digest(c['model'])or fresh.get('outer_trace_digest')!=digest(t)or raw.get('model_hash')!=digest(c['model']):raise ValueError('CURRENT_REVIEW_BINDING')
 if fresh.get('fresh_checker_executed')is not True or fresh.get('source_unchanged')is not True or fresh.get('prior_quality_certificates_reused')is not False:raise ValueError('CURRENT_FRESH_REQUIRED')
 if str(uuid.UUID(fresh['review_id']))!=fresh['review_id']:raise ValueError('FRESH_REVIEW_ID')
 if fresh.get('expected_method_registry')!=registry_for(payload_for(record,proof)):raise ValueError('CURRENT_METHOD_REGISTRY')
 if type(raw.get('errors'))is not list or type(raw.get('pending'))is not list:raise ValueError('CURRENT_REPORT_SHAPE')
 if raw['errors']:reason='UNSUPPORTED_REPAIR_REASON'
 elif raw['pending']:reason='UNKNOWN_PENDING_REVIEW'
 elif raw.get('status')=='PASS_CONCEPT_SCOPED_REVIEW':reason='NO_CURRENT_REJECTION_SCOPED_PHYSICAL_ONLY'
 else:reason='UNKNOWN_REVIEW_STATUS'
 return {'repair_attempted':False,'reason':reason,'errors':copy.deepcopy(raw['errors']),'pending':copy.deepcopy(raw['pending']),
         'original_pending':copy.deepcopy(raw.get('original_pending',[])),'semantic_qualification':'UNKNOWN_NOT_EXECUTED','accepted':False}
if __name__=='__main__':
 try:print(json.dumps(proof(json.load(sys.stdin))))
 except Exception as e:print(json.dumps({'verified':False,'error':type(e).__name__+':'+str(e)}));sys.exit(1)
