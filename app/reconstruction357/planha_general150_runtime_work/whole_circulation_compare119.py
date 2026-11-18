"""Independent bounded whole-plan Q04 comparison. No producer receipts trusted.
Evaluator is an internal executable dependency; HTTP payloads cannot supply it.
Excluding Q04 here breaks recursion only, and NEVER grants Q04 acceptance.
"""
import copy, hashlib, json
from fractions import Fraction as F
from circulation_named_audit118 import long_corridor_facts, area, measures
from core_wall_audit118 import q
from core_circulation_scope118 import SOURCE

def digest(m):
 return hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def signature(m):
 def dims(r):
  x,y,X,Y=q(r);return sorted([str(X-x),str(Y-y)])
 return {'inputs':m['inputs'],'program':m['program'],'body':m['profile'],
 'cores':{k:dims(m['common_spaces'][k]) for k in ('stair','lift')},
 'units':{u['id']:{'rooms':sorted(u['rooms']),'fixtures':{k:dims(v)for k,v in u['fixtures'].items()},'fixture_roles':{k:{a:b for a,b in v.items()if a!='rotation_deg'}for k,v in u['fixture_metadata'].items()}}for u in m['units']}}
def metrics(m):
 units=long_corridor_facts(m)['witness']['units'];out={}
 for u in units:
  uid=u['unit'];rs=u['routes']
  for key,v in rs.items():
   out[uid+':'+key+':length']=F(v['length_m']);out[uid+':'+key+':turns']=F(v['direction_changes'])
  out[uid+':circulation_union']=F(u['all_route_body_union_m2'])
  out[uid+':circulation_public_overlap']=F(u['route_inside_living_or_dining_m2'])
  out[uid+':worst_route_length']=max(F(v['length_m'])for v in rs.values())
 for k,p in m['common_routes'].items():
  v=measures(p);out['common:'+k+':length']=F(v['length_m']);out['common:'+k+':turns']=F(v['direction_changes'])
 out['common:floor_union']=area([q(r)for r in m['common_spaces']['lobby']])
 out['worst_unit_total_length']=max(sum(F(v['length_m'])for v in u['routes'].values())for u in units)
 return out

def compare(current,alternative,physical_evaluator):
 """Both models fully rechecked, except precisely the recursive comparison.
 No arbitrary weights: componentwise improvement is a conservative sufficient
 selection certificate, not a new architectural optimum or required threshold.
 Tradeoffs are retained as pending until an explicit functional reason is bound.
 """
 errors=[];pending=[];w={'source':SOURCE,'scope':'Whole same-program alternatives; scoped concept evidence only, no global optimality or technical approval.'}
 before=[digest(current),digest(alternative)];w['model_hashes']=before
 if before[0]==before[1]:pending.append('ALTERNATIVE_IDENTICAL_TO_CURRENT')
 if signature(current)!=signature(alternative):errors.append('ALTERNATIVE_INPUT_PROGRAM_CORE_OR_FURNITURE_MISMATCH')
 reports=[]
 for tag,m in [('current',current),('alternative',alternative)]:
  view=copy.deepcopy(m);r=physical_evaluator(view)
  if digest(view)!=digest(m):errors.append(tag+':PHYSICAL_EVALUATOR_MUTATED_MODEL')
  reports.append(r)
  if r.get('model_hash')!=digest(m):errors.append(tag+':PHYSICAL_REPORT_NOT_BOUND')
  if r.get('excluded_requirements')!=['long_corridor_necessity']:errors.append(tag+':WRONG_NONCIRCULAR_EXCLUSION')
  if r.get('errors'):errors.append(tag+':PHYSICAL_OR_NAMED_FAILURE')
  if r.get('noncomparison_pending', r.get('pending')):pending.append(tag+':OTHER_NAMED_REQUIREMENTS_UNRESOLVED')
  if r.get('status')!='PASS_NONCIRCULAR_PHYSICAL_SCOPED':pending.append(tag+':FULL_NONCIRCULAR_CHECK_NOT_PASSED')
 w['fresh_physical_reports']=reports
 a,b=metrics(current),metrics(alternative)
 if set(a)!=set(b):errors.append('ALTERNATIVE_ROUTE_TARGET_INVENTORY_MISMATCH')
 else:
  delta={k:a[k]-b[k]for k in a};better=[k for k,v in delta.items()if v<0];worse=[k for k,v in delta.items()if v>0]
  w.update(current_metrics={k:str(v)for k,v in a.items()},alternative_metrics={k:str(v)for k,v in b.items()},current_minus_alternative={k:str(v)for k,v in delta.items()},current_better=better,current_worse=worse)
  if worse:pending.append('CURRENT_HAS_CIRCULATION_TRADEOFF_REQUIRING_FUNCTIONAL_SELECTION_REASON')
  if not better:pending.append('NO_MEASURED_CIRCULATION_ADVANTAGE_OVER_ACTUAL_ALTERNATIVE')
 # Document review reasoning from measured evidence, not a new mandatory
 # dominance policy. Any retained disadvantages remain visible and unapproved.
 if 'current_better' in w:
  selected=[k for k in w['current_better'] if k.endswith(':scenario:kitchen_to_dining_floor:length') or k.endswith(':worst_route_length') or k.endswith(':circulation_union')]
  w['review_selection_reason']={'policy':'REVIEW_PREFERENCE_NOT_MANDATORY_DOMINANCE_OR_GLOBAL_NECESSITY','measured_benefits':selected,'retained_disadvantages':w['current_worse'],'reason':'Candidate may be retained for shorter serving/worst functional routes and less actual swept circulation where listed. Longer private/other routes and extra turns remain explicit tradeoffs, not claimed improvements.','decision':'DOCUMENTED_REVIEW_CANDIDATE' if selected else 'NO_POSITIVE_SELECTION_REASON_ESTABLISHED','all_metrics_dominance_is_owner_requirement':False}
 w['bottleneck_scope']='Both candidates must independently pass the identical actual body-clearance and operation profile. No unmeasured wider-clearance superiority is claimed.'
 w['endpoint_scope']='Targets preserve functional roles but positions may change; lengths compare complete layouts, not fixed-endpoint detour ratios.'
 w['necessity_scope']='A measured selection among two feasible whole layouts is not proof that every path is globally shortest. Unknown tradeoffs remain unresolved, not accepted.'
 if before!=[digest(current),digest(alternative)]:errors.append('MODEL_MUTATED')
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','errors':errors,'pending':pending,'witness':w,'scope':w['scope']}

def adapter_for_alternative(alternative, *, current_workflow_context=None, alternative_workflow_context=None):
 """Internal binding only; alternative geometry is freshly rechecked, not receipt.
 The checker integration supplies workflow contexts, never caller PASS records.
 """
 from checker114 import evaluate_for_circulation_comparison
 alternative=copy.deepcopy(alternative)
 alt_hash=digest(alternative)
 def callback(current):
  def physical(m):
   context=alternative_workflow_context if digest(m)==alt_hash else current_workflow_context
   return evaluate_for_circulation_comparison(m,workflow_context=context)
  return compare(current,alternative,physical)
 return callback
