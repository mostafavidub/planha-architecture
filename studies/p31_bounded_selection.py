"""Isolated P31 selection mechanics; no producer, clock, quality or delivery authority.

Trusted input is an independently obtained expected manifest digest. This is
content binding, not a signature, request API, verifier, or product decision.
Real archived observations can show rejection only; positive mechanics require
explicit synthetic fixture receipts and the returned qualified_count is zero.
"""
import hashlib,json,re

AUTH={k:False for k in ('accepted','qualified','display_allowed','delivery_allowed','production_supported')}
FIXTURE='P31_SYNTHETIC_MECHANICS_V1'
ARCHIVE='P31_ARCHIVED_NONADMISSION_V1'
MAXIMUM=6
CAP=64
CONTEXT={'schema','mode','request_digest','source_digest','environment_digest','programme_digest','budget_account_digest',
         'opened_tick','cutoff_tick','finalized_tick','requested_count'}
CANDIDATE={'schema','id','model_digest','request_context_digest','programme_digest','attempt_id','parent_id',
           'start_tick','end_tick','state','evidence_digest',*AUTH}
PAIR={'schema','context_digest','left_id','right_id','left_model','right_model','left_candidate_digest','right_candidate_digest',
      'result','evidence_digest',*AUTH}
LINEAGE={'schema','context_digest','parent_id','child_id','parent_model','child_model','parent_candidate_digest','child_candidate_digest',
         'result','evidence_digest',*AUTH}
MANIFEST={'schema','context_digest','candidate_order','candidate_digests','pair_digests','lineage_digests'}

def require(ok,code):
 if not ok:raise ValueError(code)
def strict(v,depth=0):
 require(depth<=12,'P31_TREE_DEPTH')
 t=type(v)
 require(t in (dict,list,str,int,bool,type(None)),'P31_UNSUPPORTED_VALUE_TYPE')
 if t is str:require(len(v)<=512,'P31_TEXT_LIMIT')
 if t is dict:
  require(len(v)<=CAP*CAP and all(type(k)is str and len(k)<=128 for k in v),'P31_FIELD_LIMIT')
  for x in v.values():strict(x,depth+1)
 if t is list:
  require(len(v)<=CAP*CAP,'P31_LIST_LIMIT')
  for x in v:strict(x,depth+1)
def digest(v):
 strict(v)
 return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()).hexdigest()
def hexn(x):return type(x)is str and re.fullmatch('[a-f0-9]{64}',x)is not None
def idn(x):return type(x)is str and re.fullmatch('[a-z0-9][a-z0-9_-]{0,47}',x)is not None
def pair_key(a,b):return '|'.join(sorted((a,b)))
def is_exact_k(v,k):return type(v)is dict and set(v)==k
def authority(v):return all(v.get(k)is False for k in AUTH)
def timev(v):return type(v)is int and 0<=v<2**63
def context(v):
 require(is_exact_k(v,CONTEXT) and v['schema']=='P31_SELECTION_CONTEXT_V1'
   and v['mode'] in (FIXTURE,ARCHIVE),'P31_CONTEXT')
 require(all(hexn(v[k])for k in ('request_digest','source_digest','environment_digest','programme_digest','budget_account_digest')),'P31_CONTEXT_PINS')
 require(all(timev(v[k])for k in ('opened_tick','cutoff_tick','finalized_tick'))
   and v['opened_tick']<v['cutoff_tick'] and v['opened_tick']<=v['finalized_tick'],'P31_BUDGET_CLOCK')
 n=v['requested_count']
 require(type(n)is int and 1<=n<=MAXIMUM,'P31_REQUESTED_COUNT')
def manifest(m,wanted,ctx):
 require(is_exact_k(m,MANIFEST) and m['schema']=='P31_EXTERNAL_MANIFEST_V1' and hexn(wanted) and digest(m)==wanted
  and m['context_digest']==digest(ctx),'P31_UNTRUSTED_MANIFEST')
 orders=m['candidate_order'];require(type(orders)is list and len(orders)<=CAP and all(idn(x)for x in orders)
  and len(set(orders))==len(orders),'P31_CANDIDATE_ORDER')
 for k,limit in (('candidate_digests',CAP),('lineage_digests',CAP),('pair_digests',CAP*(CAP-1)//2)):
  q=m[k];require(type(q)is dict and len(q)<=limit and all(hexn(x)for x in q.values()),'P31_PIN_INDEX')
 require(set(m['candidate_digests'])<=set(orders) and set(m['lineage_digests'])<=set(orders),'P31_PIN_ID_SET')
 for k in m['pair_digests']:
  z=k.split('|')
  require(len(z)==2 and z==sorted(z) and z[0]!=z[1] and set(z)<=set(orders),'P31_PAIR_PIN_KEY')
def find_candidate(ctx,m,k,v):
 if not is_exact_k(v,CANDIDATE) or v.get('schema')!='P31_CANDIDATE_RECEIPT_V1' or v.get('id')!=k or not authority(v):
  return 'CANDIDATE_MISSING_OR_INVALID',False
 if m['candidate_digests'].get(k)!=digest(v):return 'CANDIDATE_UNPINNED_OR_CHANGED',False
 if v['request_context_digest']!=m['context_digest'] or not (hexn(v['model_digest']) and hexn(v['evidence_digest']) and idn(v['attempt_id'])):
  return 'CANDIDATE_CONTEXT_OR_ID_MISMATCH',False
 if v['parent_id'] is not None and (not idn(v['parent_id']) or v['parent_id']==k):return 'INVALID_LINEAGE_REFERENCE',False
 if v['programme_digest']!=ctx['programme_digest']:return 'DIFFERENT_PROGRAMME',False
 a,b=v['start_tick'],v['end_tick']
 if not (timev(a) and timev(b) and ctx['opened_tick']<=a<=b<=ctx['finalized_tick']):
  return 'UNBOUND_ATTEMPT_CLOCK',False
 if b>=ctx['cutoff_tick'] or v['state']=='TIMEOUT':return 'ATTEMPT_TIMEOUT',False
 if v['state'] in ('REJECTED','UNKNOWN','EVALUATOR_ERROR','NOT_EVALUATED'):
  return 'CANDIDATE_'+v['state'],True
 if v['state']!='HYPOTHETICAL_VALIDATED':return 'CANDIDATE_UNKNOWN_STATE',False
 if ctx['mode']!=FIXTURE:return 'POSITIVE_AUTHORITY_UNWIRED_FOR_ARCHIVES',False
 if ctx['finalized_tick']>=ctx['cutoff_tick']:return 'SELECTION_WINDOW_EXPIRED',True
 return 'FIXTURE_CANDIDATE',True
def relationship(cid,v,records,decisions,linked,ctx,m):
 pid=v['parent_id']
 a=records.get(pid)
 if pid is None:return True
 if not a or not decisions.get(pid,(None,False))[1] or a['parent_id'] is not None or a['model_digest']==v['model_digest']:
  return False
 r=linked.get(cid)
 if not is_exact_k(r,LINEAGE) or not authority(r) or m['lineage_digests'].get(cid)!=digest(r):return False
 return (r['schema']=='P31_FIXTURE_LINEAGE_PROOF_V1' and r['context_digest']==m['context_digest'] and
   r['parent_id']==pid and r['child_id']==cid and r['parent_model']==a['model_digest'] and r['child_model']==v['model_digest'] and
   r['parent_candidate_digest']==digest(a) and r['child_candidate_digest']==digest(v) and
   r['result']=='VERIFIED_FIXTURE_REPLACEMENT' and hexn(r['evidence_digest']) and
   a['end_tick']<=v['start_tick']<ctx['cutoff_tick'])
def pair_outcome(a,b,pairs,m):
 if a['model_digest']==b['model_digest']:return 'DUPLICATE_MODEL'
 left,right=sorted((a,b),key=lambda x:x['id']);key=pair_key(left['id'],right['id']);r=pairs.get(key)
 if r is None:return 'PAIR_MISSING'
 if not is_exact_k(r,PAIR) or not authority(r) or m['pair_digests'].get(key)!=digest(r):
  return 'PAIR_UNTRUSTED_OR_CHANGED'
 if not (r['schema']=='P31_FIXTURE_PAIR_PROOF_V1' and r['context_digest']==m['context_digest'] and
    r['left_id']==left['id'] and r['right_id']==right['id'] and
    r['left_model']==left['model_digest'] and r['right_model']==right['model_digest'] and
    r['left_candidate_digest']==digest(left) and r['right_candidate_digest']==digest(right) and
    hexn(r['evidence_digest'])):
  return 'PAIR_STALE_OR_WRONG_BINDING'
 if type(r['result'])is not str:return 'PAIR_UNKNOWN_STATE'
 return {'VERIFIED_FIXTURE_DISTINCT':'FIXTURE_DISTINCT','VERIFIED_FIXTURE_DUPLICATE':'PAIR_VERIFIED_DUPLICATE',
         'UNKNOWN':'PAIR_UNRESOLVED'}.get(r['result'],'PAIR_UNKNOWN_STATE')
def select(ctx,candidates,pairs,lineage,*,trusted_manifest,expected_manifest_digest):
 context(ctx);m=trusted_manifest
 manifest(m,expected_manifest_digest,ctx)
 order=m['candidate_order']
 require(type(candidates)is dict and len(candidates)<=CAP and set(candidates)<=set(order),'P31_CANDIDATE_INPUT_SET')
 require(type(pairs)is dict and len(pairs)<=CAP*(CAP-1)//2 and all(type(k)is str for k in pairs)
  and type(lineage)is dict and len(lineage)<=CAP and set(lineage)<=set(order),'P31_LINK_INPUT_SET')
 # Hash validation/size guards are shared by the input/output consistency check.
 initial=digest([ctx,candidates,pairs,lineage,m])
 verdicts={k:find_candidate(ctx,m,k,candidates.get(k)) for k in order}
 reasons={k:x[0]for k,x in verdicts.items()}
 # Multiple purported receipts for one attempt never create separate candidates.
 seen={}
 for k in order:
  v=candidates.get(k)
  if (is_exact_k(v,CANDIDATE) and v['schema']=='P31_CANDIDATE_RECEIPT_V1' and v['id']==k and authority(v)
   and m['candidate_digests'].get(k)==digest(v) and v['request_context_digest']==m['context_digest']
   and v['programme_digest']==ctx['programme_digest'] and idn(v['attempt_id'])):
   seen.setdefault(v['attempt_id'],[]).append(k)
 for group in seen.values():
  if len(group)>1:
   for k in group:reasons[k]='REUSED_ATTEMPT_ID';verdicts[k]=(reasons[k],False)
 roots=[k for k in order if verdicts[k][1] and candidates[k]['parent_id'] is None]
 alts={k:[]for k in roots}
 for k in order:
  if reasons[k]!='FIXTURE_CANDIDATE':continue
  v=candidates[k]
  if v['parent_id'] is not None:
   if relationship(k,v,candidates,verdicts,lineage,ctx,m):alts[v['parent_id']].append(k)
   else:reasons[k]='CHILD_RELATION_NOT_VERIFIED'
 chosen=[];checks=[];short=[];selected_proof_keys=[]
 for root in roots:
  options=alts[root]+([root]if reasons[root]=='FIXTURE_CANDIDATE'else [])
  for ix,k in enumerate(options):
   if len(chosen)==ctx['requested_count']:
    reasons[k]='LIMIT_REACHED'
    continue
   tested=[(j,pair_outcome(candidates[j],candidates[k],pairs,m))for j in chosen]
   checks.extend({'candidate':k,'against':j,'state':v}for j,v in tested)
   broken=[v for _,v in tested if v!='FIXTURE_DISTINCT']
   if broken:
    reasons[k]=broken[0]
    continue
   selected_proof_keys.extend(pair_key(j,k)for j,_ in tested)
   chosen.append(k);reasons[k]='FIXTURE_SELECTED'
   for skip in options[ix+1:]:
    reasons[skip]='PARENT_REPLACED_BY_VERIFIED_CHILD'if skip==root and k!=root else'SAME_LINEAGE_NOT_COUNTED'
   break
 if len(chosen)<ctx['requested_count']:
  short=list(dict.fromkeys(reasons[k]for k in order if reasons[k]!='FIXTURE_SELECTED'))
  if not short or len(order)<ctx['requested_count']:short.append('INSUFFICIENT_RECORDED_CANDIDATES')
 require(len(chosen)<=MAXIMUM and len(selected_proof_keys)==len(chosen)*(len(chosen)-1)//2
  and len(set(selected_proof_keys))==len(selected_proof_keys),'P31_SELECTED_PAIR_COVERAGE')
 require(digest([ctx,candidates,pairs,lineage,m])==initial,'P31_INPUT_MUTATION')
 return {'schema':'P31_ISOLATED_SELECTION_OBSERVATION_V1','mode':ctx['mode'],'request_context_digest':m['context_digest'],
  'budget_account_digest':ctx['budget_account_digest'],'cutoff_tick_unchanged':ctx['cutoff_tick'],'budget_reset':False,
  'selected_hypothetical':chosen,'synthetic_count':len(chosen),'qualified_count':0,
  'requested_count':ctx['requested_count'],'unfilled_fixture_slots':ctx['requested_count']-len(chosen),
  'candidate_reasons':[{'id':k,'reason':reasons[k]}for k in order],'shortfall_codes':short,
  'pair_checks':checks,'selected_pair_proof_keys':selected_proof_keys,'selected_pair_count':len(selected_proof_keys),
  'producer_order_greedy_not_global_optimum':True,'live_verifier_or_api_wired':False,**AUTH}
