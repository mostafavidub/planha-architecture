"""Measured tradeoffs, not mandatory ratios or optimality certification."""
from fractions import Fraction as F
from circulation_named_audit118 import area,measures

def facts(m):
 def rs(v):return [] if not v else [tuple(map(F,r))for r in (v if isinstance(v[0],list)else[v])]
 common=area([r for v in m['common_spaces'].values()for r in rs(v)])
 units=[]
 for u in m['units']:
  paths={**u['routes'],**u.get('scenario_routes',{})}
  beds=[F(measures(p)['length_m'])for k,p in paths.items()if k.startswith('bed')]
  service=[F(measures(p)['length_m'])for k,p in paths.items()if k in('kitchen_to_dining_floor','kitchen_work')]
  circulation=area([r for name in('entry_circulation','private_circulation','private_corridor')for r in rs(u['rooms'].get(name,[]))]if any(u['rooms'].get(n)for n in('entry_circulation','private_circulation','private_corridor'))else[])
  public=area(rs(u['rooms']['living']))
  units.append({'unit':u['id'],'designated_circulation_union_m2':str(circulation),'public_residual_floor_not_certified_useful_living_m2':str(public),'longest_bed_route_m':str(max(beds,default=F(0))),'longest_service_route_m':str(max(service,default=F(0)))})
 return {'common_floor_union_m2':str(common),'units':units,'quality_optimality_claim':False}
def rank(f):
 return (max(F(u['longest_service_route_m'])for u in f['units']),max(F(u['longest_bed_route_m'])for u in f['units']),F(f['common_floor_union_m2']),max(F(u['designated_circulation_union_m2'])for u in f['units']))
