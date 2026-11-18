"""Mandatory functional circulation, distinct from comparative review preferences.
Source Q04/IR-P10 and explicit scope correction119. No global necessity claim.
"""
from fractions import Fraction as F
from core_wall_audit118 import q,sweep,covered,hit,core_concept,opening_hosts,safe,output
from core_circulation_scope118 import grammar,subtract,SOURCE
from circulation_named_audit118 import area,long_corridor_facts

def remainder(rects,uses):
 out=list(rects)
 for use in uses:out=[part for r in out for part in subtract(r,use)]
 return out

def safe_frame(fn):
 def run(m, *, frame_core=None,frame_local=None):
  try:return fn(m,frame_core=frame_core,frame_local=frame_local)
  except(KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as e:
   return output(fn.__name__,['NONPOSITIVE_RECTANGLE']if str(e)=='NONPOSITIVE_RECTANGLE'else[],[]if str(e)=='NONPOSITIVE_RECTANGLE'else['SCHEMA_OR_PROFILE_NOT_EVALUATED:'+str(e)],{})
 return run

@safe_frame
def evaluate(m, *, frame_core=None,frame_local=None):
 # These independent validators evaluate current geometry, never stored PASS.
 from named_checks118 import body_route_sweeps,public_named_scenarios
 from access_accounting118 import bath_nonprivate_access
 from checker114 import check_module_placements
 placement=check_module_placements(m)
 checks={'core':core_concept(m),'hosts':opening_hosts(m),'body':body_route_sweeps(m),'public_scenarios':public_named_scenarios(m),'bath_nonprivate':bath_nonprivate_access(m)}
 errors=[];pending=grammar(m,frame_core=frame_core,frame_local=frame_local);rows=[]
 if placement['errors']:errors.append('ACTUAL_SOURCE_MODULE_PLACEMENT_FAILED')
 pending.extend(placement['pending'])
 for k,r in checks.items():
  if r['status']=='FAIL':errors.append(k+':ACTUAL_FUNCTIONAL_CIRCULATION_FAILED')
  elif r['status']!='PASS_LIMITED':pending.append(k+':ACTUAL_FUNCTIONAL_CIRCULATION_NOT_EVALUATED')
 body=F(str(m['profile']['body_m']))
 for u in m['units']:
  paths=list(u['routes'].values())+list(u.get('scenario_routes',{}).values())
  sw=[r for p in paths for r in sweep(p,body)]
  dedicated=[q(r)for r in u['rooms'].get('entry_circulation',[])]
  # Room labels are not evidence of function. Classify uncovered material
  # explicitly rather than counting it as circulation/usable seating.
  residual=remainder(dedicated,sw)
  for r in dedicated:
   if not any(hit(r,s)for s in sw):errors.append(u['id']+':DECLARED_CIRCULATION_COMPONENT_WITHOUT_ACTUAL_ROUTE_USE')
  rows.append({'unit':u['id'],'route_body_union_m2':str(area(sw)),'declared_entry_union_m2':str(area(dedicated)), 'not_route_proven_floor_m2':str(area(residual)), 'not_route_proven_parts':[list(map(str,r))for r in residual], 'classification':'NOT_ROUTE_PROVEN; not automatically useful seating or necessary corridor. Door/other operation floor is assessed by separate mandatory operation gates.'})
 common=[q(r)for r in m['common_spaces']['lobby']];sw=[r for p in m['common_routes'].values()for r in sweep(p,body)]
 unused=[r for r in common if not any(hit(r,s)for s in sw)]
 return output('Q04',errors,pending,{'source':SOURCE,'module_placement':placement,'checks':checks,'units':rows,'common_unprogrammed_components':[{'rect':list(map(str,r)),'area_m2':str(area([r])),'classification':'COMMON_UNPROGRAMMED_NOT_PROVEN_FUNCTIONAL'}for r in unused], 'common_not_route_proven_area_m2':str(area(remainder(common,sw))), 'functional_claim_boundary':'Only actual required body-route swept union counted as route use. Unused floor is preserved and disclosed, never labelled necessary circulation or useful public area by this audit.', 'review_separation':'Layout alternative, preference tradeoffs and absolute necessity are REVIEW, not excused collisions or fake functional floor.', 'route_cost_facts':long_corridor_facts(m)['witness']})
