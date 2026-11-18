import hashlib,json,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from request_contract368 import parse_json,verify,digest

def bind(envelope,record,fresh,run_id,lineage=None):
 if type(run_id)is not str or str(uuid.UUID(run_id))!=run_id:raise ValueError('RUN_UUID')
 if type(fresh.get('review_id'))is not str or not fresh['review_id']:raise ValueError('REVIEW_ID')
 verify(envelope);c=record['candidate'];m=c['model'];t=record['trace'];p=fresh['provenance'];mh=digest(m)
 if record.get('test_only')is not True or fresh.get('test_only')is not True:raise ValueError('TEST_ONLY_REQUIRED')
 if t['schema']!='DERIVED_BALANCED_SOURCE369_TRACE_V1':raise ValueError('DERIVED_SOURCE_REQUIRED')
 if digest(c['request'])!=envelope['raw_digest']or c['request_digest']!=envelope['raw_digest']:raise ValueError('REQUEST_BINDING')
 if c['model_digest']!=mh or t['model_digest']!=mh or t['candidate_digest']!=digest(c)or digest(c['packet']['world_model'])!=mh:raise ValueError('MODEL_TRACE_BINDING')
 if (fresh['model_digest']!=mh or fresh['input_record_digest']!=digest(record)or fresh['outer_trace_digest']!=digest(t)
     or p['model_hash']!=mh or p['input_record_digest']!=digest(record)or p['candidate_digest']!=digest(c)or p['packet_digest']!=digest(c['packet'])or p['outer_trace_digest']!=digest(t)):
  raise ValueError('FRESH_PROVENANCE_BINDING')
 if not(p['verified']and fresh['fresh_checker_executed']and fresh['source_unchanged']and fresh['expected_method_registry']['built_before_evaluate']):raise ValueError('FRESH_AUTHORITY')
 if digest(p['raw'])!=digest(c['request'])or fresh['raw_report']['model_hash']!=mh:raise ValueError('RAW_MODEL_REQUEST_BINDING')
 candidate_id=digest({'run_id':run_id,'model_digest':mh,'kind':'CONTROLLED375_BALANCED'})
 if lineage is not None:
  if (lineage.get('run_id')!=run_id or lineage.get('model_digest')!=mh or lineage.get('record_digest')!=digest(record)
      or lineage.get('request_digest')!=envelope['raw_digest']or type(lineage.get('candidate_id'))is not str or not lineage['candidate_id']):raise ValueError('CHILD_LINEAGE_BINDING')
  candidate_id=lineage['candidate_id']
 return {'run_id':run_id,'candidate_id':candidate_id,'raw_digest':envelope['raw_digest'],'canonical_request_digest':envelope['canonical_request_digest'],'received_digest':envelope['received_digest'],'review_id':fresh['review_id'],'record_digest':digest(record),'model_digest':mh,'fresh_digest':digest(fresh)}

def decision(raw):
 if raw.get('status')=='PASS_CONCEPT_SCOPED_REVIEW'and not raw.get('errors')and not raw.get('pending'):return 'NO_REPAIR_CURRENT_PASS'
 if raw.get('status')!='FAIL'or raw.get('pending')!=[]:return 'STOP_NOT_UNAMBIGUOUS_FAIL'
 if not any(e.get('code')=='FIXTURE_COLLISION'for e in raw.get('errors',[])if isinstance(e,dict)):return 'STOP_NO_SUPPORTED_WITNESS'
 return 'REQUIRES_BOUND_OPERATOR_GATE'

def partial(state,run_id):
 return {'state':state,'transport_run_id':run_id,'test_only':True,'natural_generator_failure':False,'requested_count':2,'tested_branch_count':1,'request_fulfilled':False,'accepted':False,'delivery_allowed':False,'qualified_selected_set':False,'semantic_state':'UNKNOWN_NOT_EXECUTED_DUE_TO_COMPARATIVE_BLOCKER'}
