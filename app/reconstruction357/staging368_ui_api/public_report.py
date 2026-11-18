"""User-facing allowlist; full source proofs remain unchanged in run artifacts."""
import copy
BINDING=('run_id','candidate_id','review_id','model_digest','record_digest','fresh_digest','packet_digest','canonical_request_digest','raw_digest','received_digest')
def select(v,keys):return {k:copy.deepcopy(v[k])for k in keys if k in v}
def public_result(result):
 out=select(result,('schema','state','generation_run_id','canonical_request_digest','raw_digest','received_digest','raw_pipeline_receipt_digest','semantic_receipt_digest','raw_pipeline_status','accepted','delivery_allowed','global_domain_complete','repair_attempted','supported_repair_operators','supported_repair_reasons'))
 out['members']=[]
 for m in result.get('members',[]):
  out['members'].append({'kind':m['kind'],'binding':select(m['binding'],BINDING),'quality':[select(q,('rule_id','verdict','missing','model_hash','run_id','candidate_id','review_id','current_fresh_digest','scope'))for q in m.get('quality',[])]})
 if 'qualified_set'in result:
  q=result['qualified_set'];out['qualified_set']=select(q,('schema','generation_run_id','set_digest','requested_count','qualified_selected_count','membership_authority','membership_scope','accepted','delivery_allowed','global_domain_complete'))
 if 'current_rejection'in result:
  r=result['current_rejection'];out['current_rejection']={'kind':r['kind'],'binding':select(r['binding'],BINDING),'status':r['status'],'reasons':[select(x,('code','requirement_id'))for x in r['reasons']],'pending_count':len(r.get('pending',[])),'supported_repair_operators':[]}
 if result.get('state')=='UNKNOWN':out['verification_note']='تأیید کامل نشد؛ مدرک کامل و علت فنی در پروندهٔ همین اجرا حفظ شده است.'
 out['evidence_note']='شناسه‌ها و خلاصهٔ قواعد مربوط به همین اجرا هستند. بستهٔ کامل شواهد بدون تغییر جداگانه حفظ شده است؛ این JSON جایگزین اثبات منبعی نیست.'
 return out
