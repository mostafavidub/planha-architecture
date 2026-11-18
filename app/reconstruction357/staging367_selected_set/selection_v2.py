"""Draft qualification diagnostics. No membership issuer until final evaluators bind.
The pure reducer is test-only data validation, never authority or a signed receipt.
"""
import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent
REQUIRED=('SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY')
MEMBERS=('8013a1328a6104be58d9de22834dce16b1754277f450fa0ba8475253c26fc783','b1256726013116ef5f1cbcd784380a80861fa485c372909d52bf8bce0d398759')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def _hex64(x):return type(x)is str and len(x)==64 and all(c in '0123456789abcdef'for c in x)
def diagnose_test_only(members,pair,request_count):
 reasons=[]
 def fail(code):
  return {'valid_shape':False,'missing':[code],'membership_authority':False,'scope':'TEST_ONLY_DIAGNOSTIC_NO_ISSUANCE'}
 if type(request_count)is not int or request_count!=2:reasons.append('REQUEST_COUNT_EXACT_TWO')
 if type(members)is not list or len(members)!=2 or any(type(m)is not dict for m in members):return fail('TWO_TYPED_MEMBERS_REQUIRED')
 if type(pair)is not dict:return fail('PAIR_MAPPING_REQUIRED')
 ids=[m.get('model_digest')for m in members]
 if not all(_hex64(h)for h in ids):return fail('MODEL_HEX64_REQUIRED')
 if len(set(ids))!=2 or set(ids)!=set(MEMBERS):reasons.append('FIXED_UNIQUE_MEMBER_MODELS')
 for m in members:
  h=m['model_digest'];quality=m.get('quality')
  if type(quality)is not list or any(type(q)is not dict for q in quality):return fail('QUALITY_LIST_OF_MAPPINGS')
  qids=[q.get('rule_id')for q in quality]
  if any(type(i)is not str for i in qids) or len(qids)!=11 or len(set(qids))!=11 or set(qids)!=set(REQUIRED):reasons.append('ELEVEN_UNIQUE_NONCYCLIC_PARENTS_REQUIRED')
  for q in quality:
   if q.get('verdict')!='PASS' or type(q.get('missing'))is not list or q['missing']:reasons.append('PARTIAL_MEMBER_QUALITY')
   if q.get('model_hash')!=h:reasons.append('STALE_QUALITY_MODEL')
  # Diagnostic convention only; final adapter obtains IDs from fixed model.
  unitids=m.get('unit_ids')
  if type(unitids)is not list or any(type(u)is not str for u in unitids) or len(unitids)!=2 or len(set(unitids))!=2:return fail('EXACT_TWO_MODEL_UNIT_IDS')
  q12=m.get('q12')
  if type(q12)is not dict or set(q12)!=set(unitids):return fail('INDEPENDENT_PER_UNIT_Q12_REQUIRED')
  for q in q12.values():
   if type(q)is not dict:return fail('Q12_MAPPING_REQUIRED')
   if q.get('verdict')!='PASS_SCOPED_PER_UNIT_Q12' or q.get('model_hash')!=h or type(q.get('missing'))is not list or q['missing']:reasons.append('INDEPENDENT_PER_UNIT_Q12_REQUIRED')
  if not all(_hex64(m.get(k))for k in ('record_digest','fresh_digest','semantic_digest','program_digest','profile_digest','request_digest')):reasons.append('COMPLETE_CURRENT_BINDING_REQUIRED')
 if any(members[0].get(k)!=members[1].get(k)for k in ('program_digest','profile_digest','request_digest')):reasons.append('SHARED_REQUEST_PROGRAM_PROFILE')
 pids=pair.get('model_digests')
 if type(pids)is not list or len(pids)!=2 or not all(_hex64(h)for h in pids):return fail('EXACT_PAIR_MEMBERS_REQUIRED')
 if type(pair.get('pair_count'))is not int or pair['pair_count']!=1 or pair.get('source_organization_distinct')is not True or len(set(pids))!=2 or set(pids)!=set(ids):reasons.append('EXACT_CURRENT_PAIR_REQUIRED')
 return {'valid_shape':not reasons,'missing':sorted(set(reasons)),'membership_authority':False,'scope':'TEST_ONLY_DIAGNOSTIC_NO_ISSUANCE'}

def evaluate_registered_set():
 # No evaluator is imported from a caller path and no caller PASS is accepted.
 # This function is intentionally incomplete until separately audited final
 # balanced-expanded-Q04 and joint engines plus per-unit Q12 APIs are pinned.
 registry=json.loads((P/'registry_draft.json').read_text())
 for n,h in registry['sources'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('REGISTERED_SOURCE_CHANGED:'+n)
 if registry['quality_bindings']!={'balanced365':None,'joint367':None}:raise ValueError('UNREVIEWED_QUALITY_BINDING')
 return {'status':'UNKNOWN_FINAL_MEMBER_EVALUATORS_NOT_BOUND','requested_count':2,'qualified_selected_count':0,'selected_members':[],'membership_authority':False,'request_fulfilled':False,'accepted':False,'delivery_allowed':False,'missing':['BALANCED365_EXPANDED_Q04_AND_ELEVEN_PARENT_EVALUATOR','JOINT367_ELEVEN_PARENT_EVALUATOR','INDEPENDENT_PER_UNIT_Q12_BOTH_MEMBERS','AUDITED_TRANSITIVE_FINAL_QUALITY_FREEZE'],'scope':'DRAFT_ONLY_NOT_SELECTED_SET'}
