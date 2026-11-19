"""Independent study contract fork: retains all frozen registry requirements;
stricter current 5..25 domain; no historical checker identity or attach waiver.
Historical registry is not a full current PRD implementation.
"""
"""Source-bound named obligation evaluator. No producer imports, no receipts trusted.
Integration API: evaluate_rule_contract(model, *, trusted_evaluators={},
context={}, applicability_evaluators={}, evidence_by_rule=None).
Callbacks are internal independently reviewed executable tests, not HTTP data.
They receive a deep copy and must return status, nonempty witness and scope.
Missing tests remain named NOT_EVALUATED. This module grants no delivery approval.
"""
import copy,hashlib,inspect,json,types
from fractions import Fraction
from pathlib import Path
CONTRACT_SHA256='b286c31d09fd58b962e0af1a81ee0e5c79c43c17271c40580ff6ee5b7ce3a1ac'
from open_front_kitchen_study import ENGINE
PATH=ENGINE/'rule_contract118.json'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def load_contract():
 raw=PATH.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=CONTRACT_SHA256:raise ValueError('RULE_CONTRACT_SOURCE_CHANGED')
 c=json.loads(raw)
 expected={f'H{i:02}'for i in range(1,23)}|{f'Q{i:02}'for i in range(1,15)}|{f'IR-P{i:02}'for i in range(1,48)}|{f'IR-L{i:02}'for i in range(1,7)}
 if len(c['registry'])!=89 or {r['id']for r in c['registry']}!=expected:raise ValueError('RULE_REGISTRY_INCOMPLETE')
 return c

def result(status,witness,scope):return {'status':status,'witness':witness,'scope':scope}
def _input(m):
 try:
  vals=m.get('inputs');raw=vals if isinstance(vals,list)else[m['input_exact'][k]for k in ('W','L','n')];w,l,n=[Fraction(str(v))for v in raw]
  good=5<=w<=25 and 5<=l<=25 and n.denominator==1 and n in (1,2)
  return result('PASS_LIMITED'if good else'FAIL',{'exact':[str(w),str(l),str(n)]},'Exact model input-domain only; request parser/raw formatting tested separately.')
 except (KeyError,ValueError,TypeError,ZeroDivisionError):return result('FAIL',{'reason':'INVALID_OR_MISSING_EXACT_INPUT'},'Exact numeric input domain')
def _regions(m):
 found=[]
 try:
  if not isinstance(m.get('units'),list)or not m['units']:raise ValueError('MISSING_UNITS')
  found += [('wall:'+str(k),q)for k,q in m['walls'].items()]
  for u in m['units']:
   found += [(u['id']+'.ownership',q)for q in u['ownership']]
   for k,rs in u['rooms'].items():found +=[(u['id']+'.'+k,q)for q in rs]
   found +=[(u['id']+'.fixture.'+k,q)for k,q in u['fixtures'].items()]
  for k,q in found:
   if len(q)!=4:raise ValueError('UNSUPPORTED_NON_RECTANGLE_REGION:'+k)
   a,b,c,d=map(lambda v:Fraction(str(v)),q)
   if not(a<c and b<d):raise ValueError('NONPOSITIVE_RECTANGLE:'+k)
  return result('PASS_LIMITED',{'positive_rectangles':len(found),'representation':'Exact unions of positive rectangles; holes are not replaced by a bbox'},'Rectangle-union well-formedness only; coverage/disjointness/containment are separate obligations.')
 except (KeyError,TypeError,ValueError,ZeroDivisionError)as e:return result('FAIL',{'reason':str(e)},'Supported exact rectangle-union profile')
def _laundry(m):
 # Exact semantic inventory only; no inference from a picture or area label.
 if not m.get('units'):return result('NOT_EVALUATED',{'reason':'MISSING_ENTITY_INVENTORY'},'Zero laundry')
 names=[]
 for u in m['units']:
  for key in ('rooms','fixtures','activities','fixture_metadata'):
   if key not in u:return result('NOT_EVALUATED',{'reason':'INCOMPLETE_ENTITY_INVENTORY'},'Zero laundry')
   names += [(u['id']+'.'+str(k),str(v)if key=='fixture_metadata'else'')for k,v in u[key].items()]
 for key in ('reserved_spaces','reservations','space_metadata','room_metadata'):
  names +=[(str(k),str(v))for k,v in m.get(key,{}).items()]
 bad=[k for k,v in names if any(x in (k+' '+v).lower()for x in ('laundry','washing_machine','washer','رختشویی','لباسشویی'))]
 return result('FAIL'if bad else'PASS_LIMITED',{'entity_count':len(names),'forbidden_entities':bad},'Declared structured entity inventory; identity/role provenance is separately required, not recognition of disguised labels.')
BUILTINS={'input_exact_domain':_input,'valid_exact_regions':_regions,'zero_laundry':_laundry}
def _method(fn):
 try:src=inspect.getsource(fn).encode()
 except (OSError,TypeError):src=repr(getattr(fn,'__code__',type(fn))).encode()
 return {'name':getattr(fn,'__module__','')+'.'+getattr(fn,'__qualname__',type(fn).__name__),'code_sha256':hashlib.sha256(src).hexdigest()}
def _call(fn,m):
 if not callable(fn):return result('NOT_EVALUATED',{'reason':'EVALUATOR_NOT_CALLABLE'},'No computed evidence')
 view=copy.deepcopy(m);before=digest(view)
 try:r=fn(view)
 except Exception as e:return result('NOT_EVALUATED',{'reason':'EVALUATOR_EXCEPTION','type':type(e).__name__,'detail':str(e)},'No successful evaluator result')
 if digest(view)!=before:return result('FAIL',{'reason':'EVALUATOR_MUTATED_MODEL'},'Immutable audit input')
 if not isinstance(r,dict)or r.get('status')not in ('PASS_LIMITED','FAIL','NOT_EVALUATED')or not r.get('witness')or not r.get('scope'):
  return result('NOT_EVALUATED',{'reason':'INCOMPLETE_COMPUTED_EVIDENCE'},'Status alone is not evidence')
 return r

def evaluate_rule_contract(model,*,trusted_evaluators=None,context=None,applicability_evaluators=None,evidence_by_rule=None):
 c=load_contract();gid=digest(model);context=context or {};stage=context.get('stage','product');adapters=trusted_evaluators or {};app=applicability_evaluators or {};errors=[];pending=[];findings=[];reviews=[]
 if stage not in ('concept_internal','product'):raise ValueError('UNKNOWN_CONTRACT_STAGE')
 if evidence_by_rule:errors.append({'code':'UNTRUSTED_RECEIPTS_NOT_ACCEPTED','reason':'Supply internal executable evaluators, never caller PASS records'})
 for r in c['requirements']:
  rid=r['id'];required=r.get('mandatory',True);cond=r['condition'];applies=True;why={'condition':cond}
  if cond=='owner_excluded_light_vent121':
   findings.append({'requirement_id':rid,'source_rule_ids':r['source_rule_ids'],'status':'EXCLUDED_BY_OWNER_SCOPE','mandatory':False,'scope_authority':c['light_vent_authority121']});continue
  if cond=='product_stage':applies=stage=='product';why['stage']=stage
  elif cond=='multi_bedroom':
   units=model.get('units',[])
   if not units:applies=None
   else:applies=any(sum(k.startswith('bed')for k in u.get('rooms',{}))>1 for u in units)
  elif cond=='multiple_candidates':
   batch=context.get('batch_models')
   if not isinstance(batch,list)or not batch or not all(isinstance(x,dict)for x in batch)or gid not in [digest(x)for x in batch]:applies=None
   else:applies=len(batch)>1;why['batch_model_hashes']=[digest(x)for x in batch]
  elif cond=='corridor_issue_requires_applicability':
   fn=app.get(rid)
   if fn:
    ar=_call(fn,model);why['computed_applicability']=ar
    if ar['status']=='PASS_LIMITED'and isinstance(ar['witness'].get('applies'),bool):applies=ar['witness']['applies']
    else:applies=None
   else:applies=None
  if applies is False:
   row={'requirement_id':rid,'source_rule_ids':r['source_rule_ids'],'status':'NOT_APPLICABLE_TO_STAGE_OR_MODEL','applicability':why}
  elif applies is None:
   row={'requirement_id':rid,'source_rule_ids':r['source_rule_ids'],'status':'NOT_EVALUATED','applicability':why,'reason':'APPLICABILITY_NOT_ESTABLISHED'}
   if required:pending.append('RULE_APPLICABILITY_NOT_EVALUATED:'+rid)
  else:
   fn=BUILTINS.get(rid)or adapters.get(rid)
   if fn is None:
    row={'requirement_id':rid,'source_rule_ids':r['source_rule_ids'],'status':'NOT_EVALUATED','reason':'INDEPENDENT_NAMED_EVALUATOR_MISSING','applicability':why}
    if required:pending.append('RULE_NOT_EVALUATED:'+rid)
   else:
    ev=_call(fn,model);row={'requirement_id':rid,'source_rule_ids':r['source_rule_ids'],'status':ev['status'],'applicability':why,'evidence':ev,'method':_method(fn),'model_hash':gid,'contract_hash':CONTRACT_SHA256}
    if required and ev['status']=='FAIL':errors.append({'code':'RULE_FAILED','requirement_id':rid,'witness':ev['witness']})
    elif required and ev['status']=='NOT_EVALUATED':pending.append('RULE_NOT_EVALUATED:'+rid)
  row['mandatory']=required
  if not required:
   row['review_disposition']='REVIEW_DOCUMENTED'if row['status']=='PASS_LIMITED'else'REVIEW_NOT_APPLICABLE'if row['status']=='NOT_APPLICABLE_TO_STAGE_OR_MODEL'else'REVIEW_REQUIRED'
   reviews.append(row)
  findings.append(row)
 lookup={x['requirement_id']:x for x in findings};registry=[]
 for r in c['registry']:
  if r.get('classification')=='excluded_by_latest_owner_scope':
   registry.append({'rule_id':r['id'],'source':r['source'],'classification':r['classification'],'status':'EXCLUDED_BY_OWNER_SCOPE','requirement_ids':r['requirement_ids'],'full_rule_approved':False,'remaining_review':None,'scope_authority':c['light_vent_authority121']});continue
  subs=[lookup[k]for k in r['requirement_ids']if lookup[k]['mandatory']];statuses={x['status']for x in subs}
  status='FAIL_REQUIRED_SUBCONDITION'if 'FAIL'in statuses else'NOT_EVALUATED_REQUIRED_SUBCONDITION'if 'NOT_EVALUATED'in statuses else'REQUIRED_SUBCONDITIONS_ONLY_CHECKED'if subs else'REVIEW_OR_OUTSIDE_SCOPE_NOT_APPROVED'
  registry.append({'rule_id':r['id'],'source':r['source'],'classification':r['classification'],'status':status,'requirement_ids':r['requirement_ids'],'full_rule_approved':False,'remaining_review':r['implemented_evidence_mapping']['known_gap']})
 if digest(model)!=gid:errors.append({'code':'AUDIT_MUTATED_MODEL'})
 return {'contract_schema':'OPEN_FRONT_NAMED_CONTRACT_STUDY_V1','historical_registry_schema':c['schema'],'contract_hash':CONTRACT_SHA256,'model_hash':gid,'stage':stage,'errors':errors,'pending':sorted(set(pending)),'requirements':findings,'review_findings':reviews,'authority_reconciliation':c.get('circulation_authority119'),'light_vent_scope':c.get('light_vent_authority121'),'rows':registry,'status':'FAIL_REQUIRED'if errors else'NOT_EVALUATED_REQUIRED'if pending else'PASS_NAMED_REQUIRED_SCOPED','all_rules_approved':False,'accepted':False,'release':False,'eligible_for_draft_export':False,'integration_note':'This result is a source-obligation audit, not delivery permission. Existing independent physical gate remains separately mandatory. Internal evaluator registration must be reviewed; no untrusted receipts or HTTP callbacks.'}
