"""New engineering finite Q04 closure; no global optimum or live receipt.
Exact negative objectives refute dominance without converting unknown fields.
"""
from build_ledger import *
from comparison_metrics import route_metrics,rectangle_union_area
from fractions import Fraction as F
import eligibility_intrinsic359 as eligibility
from circulation_role359 import evaluate as role_review
from branch_registry359 import registry as branch_registry
H=ROOT/'semantic_rules357';HERE=Path(__file__).resolve().parent

def dimensions(m):
 values={};mm=measure_model(m)
 for u in m['units']:
  uid=u['id'];values[uid+'/circulation_m2']=F(mm['units'][uid]['declared_circulation_union_m2'])
  for k,p in u['routes'].items():
   if k not in u['route_targets']:continue
   if list(map(F,p[0]))!=list(map(F,u['entry_point'])) or list(map(F,p[-1]))!=list(map(F,u['route_targets'][k])):raise ValueError('SOURCE_ENTRY_TARGET_PATH')
   q=route_metrics(p);values[uid+'/'+k+'/length']=F(q['length']);values[uid+'/'+k+'/turns']=F(q['direction_changes'])
 return values

def negative(current,alternative):
 a,b=dimensions(current),dimensions(alternative)
 for k in sorted(set(a)&set(b)):
  if b[k]>a[k]:return {'dominance':'FALSE','witness':{'metric':k,'current':str(a[k]),'alternative':str(b[k]),'increase':str(b[k]-a[k])},'missing_other_metrics_not_promoted':True}
 return {'dominance':'UNKNOWN','reason':'NO_SINGLE_WORSE_OBJECTIVE_FOUND; POSITIVE_DOMINANCE_REQUIRES_COMPLETE_PROTECTED_VECTOR'}

def purpose_complete(role):
 return all(u['intrinsic_private_role_status']=='PASS_SCOPED_SOURCE_WHOLE_CONNECTOR_ROLE'and not u['untargeted_terminal_extensions']and u['source_connector_margin_proof']['all_residual_cells_source_bound']and all(c['verdict']=='PASS_EXACT_REQUIRED_PATH_USE_COMPONENT'for c in u['entry_circulation_components']) for u in role['units'])

def evaluate(record,review):
 before=digest([record,review]);gate=eligibility.evaluate(record,review,seconds=30)
 if gate['verdict']!='PASS'or not gate['eligible']:return {'schema':'Q04_FINITE359_CLOSURE','verdict':'UNKNOWN','reason':'UNCHANGED_CURRENT_INTRINSIC_GATE_NOT_PASS','gate':gate,'accepted':False}
 role=role_review(record,review);m=record['candidate']['model'];mh=digest(m)
 if role['model_hash']!=mh or role['review_digest']!=digest(review):raise ValueError('PURPOSE_SOURCE_BINDING')
 purpose=purpose_complete(role)
 ledger=json.loads((HERE/'bound_comparison_actual358.json').read_text());pairs=[]
 for member in ledger['members']:
  p=ROOT/member['artifact'];assert hashlib.sha256(p.read_bytes()).hexdigest()==member['artifact_sha256'];r=json.loads(p.read_text());c=r['selected'][0]if member['id']=='baseline351'else r['candidate'];other=c['model'];assert digest(other)==member['model_digest']
  if c['request']!=record['candidate']['request']or other['program']!=m['program']or other['profile']!=m['profile']:raise ValueError('FINITE_DOMAIN_SHARED_BRIEF')
  n=negative(m,other);pairs.append({'alternative':member['id'],'model_digest':digest(other),'negative_comparison':n,'retained_eligibility_evidence':member['eligibility'],'alternative_not_deleted':True})
 core=json.loads((HERE/'core_branch_bound358.json').read_text());src=json.loads((ROOT/core['artifact']).read_text())
 if hashlib.sha256((ROOT/core['artifact']).read_bytes()).hexdigest()!=core['artifact_sha256']:raise ValueError('CORE_BRANCH_CHANGED')
 # Current359 retained precisely the same core/ownership as its row358 parent.
 if digest(record['candidate']['packet']['core'])!=src['current_core_digest']:raise ValueError('CORE_CONTEXT_CHANGED')
 for r in src['ownership_rows']:
  u=next(u for u in m['units']if u['id']==r['unit']);assert digest(u['ownership'])==digest(r['before_regions'])
  if rectangle_union_area(r['after_regions'])>=rectangle_union_area(r['before_regions']):raise ValueError('CORE_COUNTEREXAMPLE_NOT_STRICT')
 # Strict counterfactual comparison against preserved358, not all candidates.
 old=next(p for p in ledger['members']if p['id']=='row358');oldrecord=json.loads((ROOT/old['artifact']).read_text());a=oldrecord['candidate']['model'];av,bv=dimensions(a),dimensions(m)
 preserved=a['program']==m['program']and a['profile']==m['profile']and oldrecord['candidate']['packet']['core']==record['candidate']['packet']['core']
 for u in a['units']:
  v=next(v for v in m['units']if v['id']==u['id']);preserved &= all(u[k]==v[k]for k in ('fixtures','activities','ownership','route_targets'))and {k:r for k,r in u['rooms'].items()if k.startswith('bed')}=={k:r for k,r in v['rooms'].items()if k.startswith('bed')}
 comparable=set(av)==set(bv);worse=[k for k in av if bv.get(k,av[k])>av[k]];better=[k for k in av if bv.get(k,av[k])<av[k]]
 branches=branch_registry();scoped=purpose and all(p['negative_comparison']['dominance']=='FALSE'for p in pairs) and branches['scope_closed']
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return {'schema':'Q04_FINITE359_CLOSURE','verdict':'PASS_SCOPED_FINITE_Q04'if scoped else'UNKNOWN','finite_branch_registry':branches,'unknown_reasons':branches['unknown_or_stopped_branch_ids'],'model_digest':mh,'record_digest':digest(record),'fresh_result_digest':digest(review),'current_gate':gate,'current_gate_evaluator_sha256':hashlib.sha256((H/'eligibility_intrinsic359.py').read_bytes()).hexdigest(),'purpose':role,'alternatives':pairs,'full_band_branch':{'proof':core,'current_core_and_ownership_binding':True,'state':'EXCLUDED_ONLY_FROM_NONDECREASING_OWNERSHIP_DOMAIN_NOT_INTRINSIC_INVALIDITY'},'current_self_comparison':'EXACT_TIE_NOT_STRICT_DOMINANCE','counterfactual_358_to359':{'preserved_exact_geometry_inventory':preserved,'same_metric_inventory':comparable,'improved':better,'worsened':worse,'strict_objective_improvement':bool(better)and not worse,'scope':'B18_CURRENT_PASS_PLUS_PRIOR_FIXED_B18_358; REQUIRED_OBJECT_USE_AND_ROUTE_GEOMETRY_PRESERVED; NOT_GLOBAL_SUPERIORITY'},'bottleneck_scope':{'below_source_body_blocked_required_routes':0,'basis':'Current intrinsic B06 source-profile body-sweep gate PASS; no invented preferred-clearance threshold','scope':'SOURCE_REQUIRED_ACTUAL_ROUTE_FEASIBILITY_ONLY; NO_ALTERNATIVE_ROUTE_OPTIMUM'},'finite_scope':'Three named constructed alternatives plus current self tie and explicit source114 full-band protected-ownership branch; no exhaustive global topology enumeration','source233':'Q04 [447999,464629], sourceSHA046cb8490a0865b74a9f844fa7db513490c50393e21923d1aa458f846fa89108','engineering_assumption':'Exact componentwise nondeterioration over named per-unit actual-target route lengths/turns and circulation area. One strictly worse objective refutes dominance regardless of other unknown dimensions. Source-role margins are accepted only through separately audited source connector proof.','all12_accepted':False,'delivery_allowed':False,'new_fresh_execution':False,'live_authority':False,'audit_status':'PENDING_INDEPENDENT_CLOSURE_AUDIT'}
if __name__=='__main__':
 r=json.loads((ROOT/'staging359_hall_clamp/actual359.json').read_text());f=json.loads((ROOT/'review359_source_validation/result.json').read_text());out=evaluate(r,f);(HERE/'q04_closure_actual359.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(out['verdict'])
