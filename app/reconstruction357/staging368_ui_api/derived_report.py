"""Transport projection of a trusted private bridge invocation, never an issuer."""
import copy
from state_machine import digest,final_view

def derive(raw,semantic,envelope,run_id):
 if raw.get('generation_run_id')!=run_id or semantic.get('generation_run_id')!=run_id:raise ValueError('DERIVED_RUN_BINDING')
 for k in ('canonical_request_digest','raw_digest','received_digest'):
  if raw.get(k)!=envelope[k]:raise ValueError('DERIVED_RAW_REQUEST:'+k)
 status=semantic.get('status')
 states={'QUALIFIED_FIXED_CURRENT_RUN':'QUALIFIED_CONCEPTUAL_SET','UNKNOWN':'UNKNOWN','REJECTED_UNSUPPORTED_REDESIGN':'REJECTED_UNSUPPORTED_REDESIGN'}
 if status not in states:raise ValueError('UNREGISTERED_BRIDGE_STATUS')
 out={'schema':'UI368_CURRENT_DERIVED_REPORT','state':states[status],'generation_run_id':run_id,**{k:envelope[k]for k in ('canonical_request_digest','raw_digest','received_digest')},'raw_pipeline_receipt_digest':digest(raw),'semantic_receipt_digest':digest(semantic),'raw_pipeline_status':raw['status'],'semantic_receipt':copy.deepcopy(semantic),'accepted':False,'delivery_allowed':False,'global_domain_complete':False,'supported_repair_reasons':[],'repair_attempted':False}
 if status=='QUALIFIED_FIXED_CURRENT_RUN':
  for k in ('canonical_request_digest','raw_digest','received_digest'):
   if semantic.get(k)!=envelope[k]:raise ValueError('DERIVED_SEMANTIC_REQUEST:'+k)
  out.update(members=copy.deepcopy(semantic['members']),qualified_set=copy.deepcopy(semantic['qualified_set']))
 elif status=='REJECTED_UNSUPPORTED_REDESIGN':
  rejection=semantic['current_rejection'];b=rejection['binding']
  if rejection.get('status')!=status or semantic.get('supported_repair_operators')!=[] or rejection.get('supported_repair_operators')!=[]:raise ValueError('REJECTION_OPERATOR_BINDING')
  if b.get('run_id')!=run_id or any(b.get(k)!=envelope[k]for k in ('canonical_request_digest','raw_digest','received_digest')):raise ValueError('REJECTION_REQUEST_BINDING')
  rows=[m for m in raw['members']if m.get('kind')==rejection.get('kind')]
  if len(rows)!=1:raise ValueError('REJECTION_MEMBER_BINDING')
  review=rows[0]['review'];original=review['binding']
  if review.get('review_id')!=b['review_id']or original.get('candidate_id')!=b['candidate_id']or original.get('model_digest')!=b['model_digest']or review.get('fresh_result_digest')!=b['fresh_digest']:raise ValueError('REJECTION_CURRENT_REVIEW_BINDING')
  if rejection.get('model_digest')!=b['model_digest']or rejection.get('fresh_digest')!=b['fresh_digest']:raise ValueError('REJECTION_CURRENT_MODEL_BINDING')
  if not rejection.get('reasons')or any(type(x)is not dict or type(x.get('code'))is not str or not x['code']for x in rejection['reasons']):raise ValueError('REJECTION_REASON_SCHEMA')
  out.update(members=[],current_rejection=copy.deepcopy(rejection),missing=copy.deepcopy(rejection['reasons']),supported_repair_operators=[])
 else:
  out.update(members=[],missing=copy.deepcopy(semantic.get('missing',[])))
 final_view(out,envelope,run_id)
 return out

def unwrap_bridge(final,receipt,supervision,raw,envelope,run_id):
 if final.get('schema')!='DERIVED_FINAL_REPORT368'or final.get('generation_run_id')!=run_id or final.get('raw_pipeline_digest')!=digest(raw):raise ValueError('BRIDGE_FINAL_RAW_BINDING')
 if final.get('bridge_receipt_digest')!=digest(receipt)or final.get('supervision_digest')!=digest(supervision):raise ValueError('BRIDGE_FINAL_RECEIPT_BINDING')
 if supervision.get('reason')!='COMPLETED'or type(supervision.get('worker_returncode'))is not int or supervision['worker_returncode']!=0 or supervision.get('cleanup_verified')is not True or supervision.get('worker_reaped')is not True or supervision.get('unresolved')!=[]:raise ValueError('BRIDGE_SUPERVISION_NOT_COMPLETED')
 if receipt.get('generation_run_id')!=run_id or receipt.get('raw_pipeline_digest')!=digest(raw)or receipt.get('request_digest')!=digest({'run_id':run_id,'envelope':envelope})or receipt.get('source_unchanged')is not True:raise ValueError('BRIDGE_RECEIPT_CURRENT_INPUTS')
 if final['qualified_set']!=receipt['bridge_result']:raise ValueError('BRIDGE_SEMANTIC_RECEIPT_BINDING')
 return copy.deepcopy(receipt['bridge_result'])
