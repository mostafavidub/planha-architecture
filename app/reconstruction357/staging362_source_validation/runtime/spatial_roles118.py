"""Honest geometry-bound accounting labels. Does not invent useful rooms.
Existing open-public geometry is retained for paths/windows, not sold as useful
living area. Functional groups refer only to actual fixtures/activities/routes.
"""
from fractions import Fraction as F
from geometry114 import cells,Q,hit
from contract114 import digest,S
from space_accounting118 import ledger

def area(rs):return sum((F(q[2])-F(q[0]))*(F(q[3])-F(q[1]))for q in rs)
def attach(m):
 physical={'inputs':m['inputs'],'walls':m['walls'],'common_spaces':m['common_spaces'],'units':[{k:u[k]for k in('id','ownership','rooms','fixtures','activities','routes','scenario_routes')}for u in m['units']]}
 audit=ledger(m);binding=digest(physical)
 for u in m['units']:
  uid=u['id'];fxids=[k for k in u['fixtures']if k.startswith(('sofa','armchair'))];actids=[k+'_front'for k in fxids if k+'_front'in u['activities']]
  group=cells([u['fixtures'][k]for k in fxids]+[u['activities'][k]for k in actids],[])
  u['spatial_role_bindings']={'open_public_envelope':{'source_room_key':'living','regions':u['rooms'].get('living',[]),'display_name_fa':'پهنه باز عمومی؛ کارکرد کامل تأیید نشده','counts_as_verified_useful_living':False,'reason':'Retained exact floor domain for access/window checks, not a residual-to-capacity conversion.'},'living_activity_group':{'regions':group,'fixture_ids':fxids,'activity_ids':actids,'access_route_ids':[k for k in actids if k in u['routes']],'guest_route_id':'guest_living'if'guest_living'in u['scenario_routes']else None,'declared_footprint_area_m2':S(area(group)),'functional_status':'REQUIRES_SCENARIO_CAPACITY_GATE','scope':'Actual furniture and declared activity footprints only, not a claimed enclosing useful room.'}}
  m['room_metadata'][uid+'.living']={'role':'open_public_envelope','display_name_fa':'پهنه باز عمومی؛ کارکرد کامل تأیید نشده','private':False,'verified_useful_area':False,'physical_room_key_preserved':'living'}
 W,L=map(lambda x:F(str(x)),m['inputs'][:2]);plot=[[F(0),F(0),W,L]];assigned=[];groups=[];errors=[]
 units=m['units']
 for i,a in enumerate(units):
  for b in units[i+1:]:
   if any(hit(Q(x),Q(y))for x in a['ownership']for y in b['ownership']):errors.append('UNIT_OWNERSHIP_OVERLAP:'+a['id']+':'+b['id'])
 raw=[('actual_wall_union',list(m['walls'].values()))]+[('threshold_'+a['opening_id']+'_'+a['side']+'_'+a['owner'],[a['rect']])for a in m.get('threshold_ownership',{}).get('allocations',[])]+[('unit_'+u['id']+'_floor',u['ownership'])for u in units]
 for k,v in m['common_spaces'].items():raw.append(('common_'+k,v if isinstance(v[0],list)else[v]))
 for name,rs in raw:
  clipped=[]
  for r in rs:
   a,b,c,d=Q(r);a=max(a,F(0));b=max(b,F(0));c=min(c,W);d=min(d,L)
   if a<c and b<d:clipped.append([a,b,c,d])
  region=cells(clipped,assigned);groups.append({'role':name,'regions':region,'area_m2':S(area(region))});assigned+=region
 remainder=cells(plot,assigned);groups.append({'role':'UNASSIGNED_PLOT_FLOOR','regions':remainder,'area_m2':S(area(remainder)),'not_inferred_as_outdoor_or_storage':True})
 total=sum(F(g['area_m2'])for g in groups)
 if total!=W*L:errors.append('PLOT_AREA_NOT_CONSERVED')
 m['spatial_accounting']={'schema':'DECLARED_SPACE_ACCOUNTING118','physical_geometry_hash':binding,'unit_ledger':audit,'plot_partition':groups,'plot_area_m2':S(W*L),'partition_sum_m2':S(total),'errors':errors,'classification_precedence':'physical wall union; unit floor; common clear regions; unassigned plot. Exact intersections, not extra physical boundaries.','remainder_label':'UNACCOUNTED_DECLARED_FLOOR','limitations':['Unit remainder excludes only declared fixture/activity/body-route footprints; full swept operations are not complete.','Not proof of unusable floor or useful living capacity.','Necessary circulation is declared, not proved shortest or minimal.','No new room, store, courtyard or private partition is generated.'],'accepted':False}
 m['quality_unverified']=['Open-public envelope is retained for access/window geometry, not verified useful living area.','Actual living activity group is separately bound to furniture, activities and routes; capacity/comfort remain scenario-gated.','Remainder is UNACCOUNTED_DECLARED_FLOOR, not automatically useful, unusable, storage or courtyard.','Service ventilation/daylight remain unverified; open-edge contact is only geometric evidence.']
 return m
