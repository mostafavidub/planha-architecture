"""Geometric proof of a doorless private approach shared by two bedrooms.
No added wall/door or role rename. Existing solids, openings, floor and real
non-bedroom activity paths must prove the pocket is not public through-flow.
"""
from fractions import Fraction as F
from core_wall_audit118 import q,hit,covered,sweep

def examine(m):
 body=F(str(m['profile']['body_m']));h=body/2;W,L=map(F,m['inputs'][:2]);walls=[q(r)for r in m['walls'].values()];opall=[q(o['rect'])for o in m['openings']];regions=[]
 for u in m['units']:
  beds={u['id']+'.'+k:[q(r)for r in rs]for k,rs in u['rooms'].items()if k.startswith('bed')};entries=[];floor=[q(r)for rs in u['rooms'].values()for r in rs];fixtures=[q(r)for r in u['fixtures'].values()]
  for o in m['openings']:
   linked=[k for k in o['connects']if k in beds]
   if len(linked)==1:
    r=q(o['rect']);host=m['wall_hosts'].get(o.get('host_wall_id'))
    if host and r[3]-r[1]>r[2]-r[0]:entries.append((linked[0],o,r,q(host)))
  for i,a in enumerate(entries):
   for b in entries[i+1:]:
    if a[0]==b[0]:continue
    left,right=sorted((a,b),key=lambda z:z[2][0]);ln,lo,lr,lh=left;rn,ro,rr,rh=right;x,X=lr[2],rr[0]
    if X-x<body:continue
    if not all(z[2]<=lr[0]for z in beds[ln])or not all(z[0]>=rr[2]for z in beds[rn]):continue
    # Method scope: a real closed horizontal end, not necessarily a facade.
    # Host names/labels alone prove nothing: full cap material must exist.
    loY=max(lh[1],rh[1]);hiY=min(lh[3],rh[3]);candidates=[]
    for host_id,raw_host in m['wall_hosts'].items():
     cap=q(raw_host)
     if cap[2]-cap[0]<=cap[3]-cap[1] or not cap[0]<=x<X<=cap[2]:continue
     strip=(x,cap[1],X,cap[3])
     if not covered(strip,walls):continue
     if any(hit(strip,q(o['rect'])) for o in m['openings']):continue
     if loY<=cap[3]<hiY:candidates.append(((x,cap[3],X,hiY),'top',host_id,strip))
     if loY<cap[1]<=hiY:candidates.append(((x,loY,X,cap[1]),'bottom',host_id,strip))
    seen_candidates=set()
    for zone,entrance,cap_id,cap_strip in candidates:
     key=(zone,entrance)
     if key in seen_candidates:continue
     seen_candidates.add(key)
     y,Y=zone[1],zone[3];reasons=[]
     if not covered(zone,floor):reasons.append('ACTUAL_FLOOR_UNCOVERED')
     if any(hit(zone,r)for r in walls+fixtures):reasons.append('ZONE_PHYSICAL_OBSTRUCTION')
     leftstrip=(lr[0],y,lr[2],Y);rightstrip=(rr[0],y,rr[2],Y)
     if not covered(leftstrip,walls+opall)or not covered(rightstrip,walls+opall):reasons.append('SIDE_BOUNDARY_GAP')
     if not y<=lr[1]<lr[3]<=Y or not y<=rr[1]<rr[3]<=Y:reasons.append('BEDROOM_DOOR_OUTSIDE_ZONE')
     extra=[o['id']for o in m['openings']if o['id']not in(lo['id'],ro['id'])and(hit(q(o['rect']),leftstrip)or hit(q(o['rect']),rightstrip))]
     if extra:reasons.append('ADDITIONAL_SIDE_OPENING')
     center=(x+X)/2;boundary=Y if entrance=='top'else y;cross=(center-h,boundary-h,center+h,boundary+h)
     if not covered(cross,floor)or any(hit(cross,r)for r in walls+fixtures):reasons.append('PUBLIC_INTERFACE_BODY_NOT_FREE')
     paths={k:p for k,p in u['routes'].items()if not k.startswith('bed')};paths.update({'scenario:'+k:p for k,p in u.get('scenario_routes',{}).items()})
     through=[k for k,p in paths.items()if any(hit(zone,r)for r in sweep(p,body))]
     if through:reasons.append('NONBEDROOM_ACTIVITY_USES_PRIVATE_APPROACH')
     missing=[k for k in('guest_living','guest_dining','kitchen_to_dining_floor')if not u.get('scenario_routes',{}).get(k)]
     regions.append({'closed_end_host_id':cap_id,'closed_end_solid_strip':list(map(str,cap_strip)),'source_binding_scope':'Actual host/solid geometry here; full source-module/isometry and network checks remain separate mandatory checks','unit':u['id'],'bedrooms':[ln,rn],'zone':list(map(str,zone)),'public_open_side':entrance,'clear_width_m':str(X-x),'door_ids':[lo['id'],ro['id']],'extra_side_openings':extra,'nonbedroom_routes_intersecting':through,'errors':reasons,'pending_scenario_inventory':missing,'geometric_enclosure_proven':not reasons,'status':'PASS_TWO_BEDROOM_PRIVATE_APPROACH_TOPOLOGY'if not reasons and not missing else'NOT_EVALUATED_APPROACH_USE'if not reasons else'NOT_A_PROVEN_PRIVATE_APPROACH','not_added_wall_or_door':True,'compactness_or_necessity_globally_proven':False})
 return {'zones':regions,'scope':'Existing floor and enclosing real side/end solids; end may be existing service/core/envelope host, two actual bedroom portals, single open public entrance and no supplied guest/service activity crossing; not automatic compactness of all bedrooms or global route optimality.'}
