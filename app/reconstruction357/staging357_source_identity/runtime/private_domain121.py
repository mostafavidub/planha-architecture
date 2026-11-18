"""Independent multi-bedroom private-domain topology. Not a visibility certificate.
No source rule limits grouping to pairs. Missing physical domains remain pending.
"""
from fractions import Fraction as F
from core_wall_audit118 import q,hit,covered,sweep

def examine(m):
 errors=[];pending=[];rows=[];body=F(str(m['profile']['body_m']));h=body/2
 try:
  walls=list(map(q,m['walls'].values()));domains=m.get('private_domains',[])
  for u in m['units']:
   uid=u['id'];beds={uid+'.'+k for k in u['rooms']if k.startswith('bed')}
   if len(beds)<3:continue
   ds=[d for d in domains if d.get('unit')==uid]
   if len(ds)!=1:pending.append(uid+':UNSUPPORTED_DOMAIN_VERIFICATION:ONE_DECLARED_DOMAIN_METHOD');continue
   d=ds[0];parts=list(map(q,d['parts']));own=list(map(q,u['ownership']));fx=list(map(q,u['fixtures'].values()));floor=[q(r)for rs in u['rooms'].values()for r in rs]
   if set(d['bedrooms'])!=beds or len(d['bedrooms'])!=len(beds):errors.append(uid+':DOMAIN_BEDROOM_INVENTORY')
   if any(not covered(r,own)or not covered(r,floor)or any(hit(r,w)for w in walls+fx)for r in parts):errors.append(uid+':DOMAIN_NOT_ACTUAL_FREE_FLOOR')
   interface=q(d['public_interface']['rect']);side=d['public_interface']['open_side'];axis=1 if side in('top','bottom')else 0 if side in('left','right')else -1
   if axis<0:pending.append(uid+':UNSUPPORTED_DOMAIN_VERIFICATION:AXIS_ALIGNED_INTERFACE_METHOD');continue
   center=((interface[0]+interface[2])/2,(interface[1]+interface[3])/2)
   if axis>=0 and interface[axis+2]-interface[axis]!=body:pending.append(uid+':UNSUPPORTED_DOMAIN_VERIFICATION:BODY_STRIP_INTERFACE_METHOD')
   if axis>=0:
    inward=list(interface);outward=list(interface);mid=center[axis]
    if side in('top','right'):inward[axis+2]=mid;outward[axis]=mid
    else:inward[axis]=mid;outward[axis+2]=mid
    if not covered(tuple(inward),parts)or any(hit(tuple(outward),r)for r in parts):pending.append(uid+':UNSUPPORTED_DOMAIN_VERIFICATION:SINGLE_EDGE_INTERFACE_METHOD')
   cross=(center[0]-h,center[1]-h,center[0]+h,center[1]+h)
   if not covered(cross,floor)or any(hit(cross,w)for w in walls+fx):errors.append(uid+':PUBLIC_INTERFACE_NOT_BODY_FREE')
   doors=[o for o in m['openings']if any(b in o['connects']for b in beds)]
   if {b for o in doors for b in o['connects']if b in beds}!=beds or len(doors)!=len(beds):errors.append(uid+':DOMAIN_ACTUAL_DOOR_INVENTORY')
   # Every exposed domain edge must touch a physical solid, a bedroom
   # aperture, or the one declared public interface. Rectangular envelopes
   # cannot silently bridge holes or a second public opening.
   cover=walls+[q(o['rect'])for o in doors]+[interface];allr=parts+cover
   xs=sorted({v for r in allr for v in(r[0],r[2])});ys=sorted({v for r in allr for v in(r[1],r[3])})
   def member(x,y):return any(r[0]<x<r[2]and r[1]<y<r[3]for r in parts)
   gaps=[]
   for axis0,coords,other in [(0,xs,ys),(1,ys,xs)]:
    for j,v in enumerate(coords):
     lo=(coords[j-1]+v)/2 if j else v-1;hi=(v+coords[j+1])/2 if j+1<len(coords)else v+1
     for a,b in zip(other,other[1:]):
      mid=(a+b)/2;x,y=(v,mid)if axis0==0 else(mid,v)
      left=member(lo,mid)if axis0==0 else member(mid,lo);right=member(hi,mid)if axis0==0 else member(mid,hi)
      if left==right:continue
      isinterface=axis0==axis and v==center[axis]and interface[1-axis]<=mid<=interface[3-axis]
      if not isinterface and not any(r[0]<=x<=r[2]and r[1]<=y<=r[3]for r in walls+[q(o['rect'])for o in doors]):gaps.append([str(x),str(y)])
   if gaps:pending.append(uid+':UNSUPPORTED_DOMAIN_VERIFICATION:EXTRA_OR_UNPROVEN_DOMAIN_BOUNDARY')
   paths=d.get('paths',{})
   if set(paths)!=beds:pending.append(uid+':PRIVATE_DOMAIN_BODY_PATHS_REQUIRED')
   for bed,path in paths.items():
    if bed not in beds:errors.append(uid+':UNKNOWN_DOMAIN_TARGET');continue
    ports=[p for p in m.get('module_ports',[])if p.get('opening_id')in[o['id']for o in doors if bed in o['connects']]]
    if len(ports)!=1 or tuple(map(F,path[-1]))!=tuple(map(F,ports[0]['center'])):errors.append(uid+':DOMAIN_PATH_PORT_BINDING')
    if tuple(map(F,path[0]))!=center:errors.append(uid+':DOMAIN_PATH_INTERFACE_BINDING')
    for r in sweep(path,body):
     if not covered(r,parts+[interface])or any(hit(r,w)for w in walls+fx):errors.append(uid+':DOMAIN_BODY_ROUTE_INVALID')
   nonbed={k:p for k,p in u['routes'].items()if not k.startswith('bed')};nonbed.update(u.get('scenario_routes',{}))
   if any(hit(r,z)for p in nonbed.values()for r in sweep(p,body)for z in parts):errors.append(uid+':NONPRIVATE_FUNCTION_THROUGH_PRIVATE_DOMAIN')
   rows.append({'unit':uid,'bedrooms':sorted(beds),'domain_parts':d['parts'],'boundary_gaps':gaps,'visibility_status':'NOT_EVALUATED_BY_TOPOLOGY','all_private_targets_retained':True})
 except(KeyError,ValueError,TypeError,IndexError)as e:errors.append('PRIVATE_DOMAIN_SCHEMA:'+str(e))
 return {'errors':sorted(set(errors)),'pending':sorted(set(pending)),'domains':rows,'scope':'Conservative proof method for one declared connected domain with one axis-aligned public interface. These topology restrictions are NOT owner requirements and unsupported domains are NOT proven infeasible. Physical collision, actual access and inventory falsification remain errors. No all-scenario privacy, wardrobe capacity, minimal-corridor or whole-plan approval.'}
