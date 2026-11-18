"""Transport/progress defense, not a geometry/semantic acceptance issuer."""
import copy,re,uuid,json,hashlib
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
TERMINAL={'QUALIFIED_CONCEPTUAL_SET','REVIEWED_NOT_QUALIFIED','REJECTED_UNSUPPORTED_REDESIGN','UNKNOWN','CAPABILITY_UNAVAILABLE','FAILED'}
def valid_run_id(value):
 try:return type(value)is str and str(uuid.UUID(value))==value
 except (ValueError,AttributeError):return False

def event_view(event,run_id):
 if type(event)is not dict or event.get('generation_run_id')!=run_id:raise ValueError('EVENT_RUN_BINDING')
 if type(event.get('phase'))is not str or not 0<len(event['phase'])<=160:raise ValueError('EVENT_PHASE')
 if event.get('status')not in {'STARTED','COMPLETED','FAIL','UNKNOWN','STOPPED'}:raise ValueError('EVENT_STATUS')
 out={k:copy.deepcopy(event[k])for k in ('generation_run_id','phase','status','kind','candidate_id','review_id')if k in event}
 for k in ('candidate_id','review_id'):
  if k in out and out[k] is not None and(type(out[k])is not str or not out[k]or len(out[k])>200):raise ValueError('EVENT_ID')
 if 'kind'in out and out['kind']not in ('balanced','joint'):raise ValueError('EVENT_KIND')
 return out

def final_view(result,envelope,run_id):
 if type(result)is not dict or result.get('generation_run_id')!=run_id:raise ValueError('RESULT_RUN_BINDING')
 for k in ('canonical_request_digest','raw_digest'):
  if result.get(k)!=envelope[k]:raise ValueError('RESULT_REQUEST_BINDING:'+k)
 state=result.get('state')
 if state not in TERMINAL:raise ValueError('UNRECOGNIZED_PIPELINE_TERMINAL_STATE')
 # Only pipeline issuer may qualify the conceptual set; transport never grants delivery.
 if state=='QUALIFIED_CONCEPTUAL_SET':
  q=result.get('qualified_set')
  if type(q)is not dict or q.get('membership_authority')is not True or q.get('qualified_selected_count')!=envelope['normalized_raw']['requested_count']:raise ValueError('QUALIFIED_SET_WITNESS_REQUIRED')
  verify_qualified_binding(result,envelope,run_id)
 return {'state':state,'generation_run_id':run_id,'canonical_request_digest':envelope['canonical_request_digest'],'raw_digest':envelope['raw_digest'],'result':copy.deepcopy(result),'delivery_allowed':False,'transport_is_acceptance_authority':False}

def redesign_decision(fresh,registered_operator_codes):
 """Pure routing diagnostic only. Runtime must validate source receipts before this.
 No API accepts this object from the browser. UNKNOWN is not a rejection.
 """
 if fresh.get('verdict')!='FAIL':return 'STOP_NOT_PROVEN_FAIL'
 if not fresh.get('candidate_id')or not fresh.get('model_digest')or not fresh.get('review_id'):return 'STOP_UNBOUND_REJECTION'
 errors=fresh.get('errors')
 if type(errors)is not list or not errors or any(type(x)is not dict or x.get('code')not in registered_operator_codes for x in errors):return 'STOP_UNSUPPORTED_REJECTION'
 return 'SUPPORTED_FAIL_REQUIRES_SOURCE_BOUND_OPERATOR'


def verify_qualified_binding(result,envelope,run_id):
 q=result['qualified_set']
 if type(q.get('requested_count'))is not int or q['requested_count']!=envelope['normalized_raw']['requested_count']:raise ValueError('CURRENT_SET_REQUESTED_COUNT')
 if any(q.get(k)!=envelope[k]for k in ('canonical_request_digest','raw_digest','received_digest'))or q.get('normalized_raw_digest')!=envelope['raw_digest']:raise ValueError('CURRENT_SET_REQUEST_BINDING')
 unsigned={k:v for k,v in q.items()if k!='set_digest'}
 if q.get('generation_run_id')!=run_id or q.get('set_digest')!=digest(unsigned):raise ValueError('CURRENT_SET_DIGEST_OR_RUN')
 members=result.get('members');selected=q.get('members')
 if type(members)is not list or type(selected)is not list or len(members)!=2 or len(selected)!=2:raise ValueError('CURRENT_MEMBER_INVENTORY')
 if {m.get('kind')for m in members}!={'balanced','joint'}:raise ValueError('CURRENT_MEMBER_KIND')
 pairset=q.get('pair',{})
 if type(pairset.get('pair_count'))is not int or pairset.get('pair_count')!=1 or pairset.get('source_organization_distinct')is not True or len(pairset.get('members',[]))!=2 or {x.get('kind')for x in pairset['members']}!={'balanced','joint'}:raise ValueError('CURRENT_PAIR_INVENTORY')
 seen=set();reviews=set()
 for m in members:
  b=m['binding'];cid=b['candidate_id'];rid=b['review_id']
  if cid in seen or rid in reviews or not valid_run_id(rid):raise ValueError('CURRENT_MEMBER_IDENTITIES')
  seen.add(cid);reviews.add(rid)
  if b.get('run_id')!=run_id or any(b.get(k)!=envelope[k]for k in ('canonical_request_digest','raw_digest','received_digest')):raise ValueError('CURRENT_MEMBER_REQUEST')
  match=[x for x in selected if x.get('binding')==b]
  if len(match)!=1:raise ValueError('CURRENT_SET_MEMBER_BINDING')
  quality=m['quality'];q12=m['current_roles']['q12']
  if type(q12)is not list or len(q12)!=2 or {x.get('unit')for x in q12}!={'A','B'}:raise ValueError('CURRENT_UNIT_INVENTORY')
  if len(quality)!=12 or len({x['rule_id']for x in quality})!=12:raise ValueError('CURRENT_TWELVE_RULES')
  if match[0].get('eleven_attestations_digest')!=digest([x for x in quality if x['rule_id']!='DISTINCTNESS_AND_FAIRNESS'])or match[0].get('q12_digest')!=digest(q12):raise ValueError('CURRENT_SET_PROOF_DIGEST')
  for row in quality:
   if row.get('verdict')!='PASS'or row.get('missing')!=[]or any(row.get(k)!=v for k,v in {'run_id':run_id,'candidate_id':cid,'review_id':rid,'model_hash':b['model_digest'],'current_fresh_digest':b['fresh_digest']}.items()):raise ValueError('CURRENT_RULE_BINDING')
  q14=[x for x in quality if x['rule_id']=='DISTINCTNESS_AND_FAIRNESS']
  if len(q14)!=1 or q14[0].get('source_closure')!={'current_set_digest':q['set_digest'],'current_pair_digest':digest(pairset),'independent_current_q12_digest':digest(q12)}:raise ValueError('CURRENT_Q14_SET_BINDING')
  for row in q12:
   if any(row.get(k)!=v for k,v in {'run_id':run_id,'candidate_id':cid,'review_id':rid,'model_digest':b['model_digest'],'fresh_digest':b['fresh_digest']}.items())or row.get('missing')!=[]:raise ValueError('CURRENT_UNIT_BINDING')
  pair=[x for x in q['pair']['members']if x.get('candidate_id')==cid]
  if len(pair)!=1 or any(pair[0].get(k)!=v for k,v in {'generation_run_id':run_id,'review_id':rid,'model_digest':b['model_digest'],'current_fresh_digest':b['fresh_digest']}.items()):raise ValueError('CURRENT_PAIR_BINDING')
 return True
