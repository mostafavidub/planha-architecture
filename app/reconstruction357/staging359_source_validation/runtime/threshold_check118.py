"""Independent reference-line aperture allocation, not installed-frame certification."""
from fractions import Fraction as F
from space_accounting118 import rect,merge

def examine(m):
 errors=[]; expected=[]
 try:
  t=m['threshold_ownership'];rows=t['allocations']
  if t['schema']!='PORTAL_REFERENCE_HALF_OWNERSHIP118':raise ValueError('SCHEMA')
  openings={o['id']:o for o in m['openings']};owners={'unit:'+u['id']:[rect(r)for r in u['ownership']]for u in m['units']}
  owners.update({'common:'+k:[rect(r)for r in (v if isinstance(v[0],list)else[v])]for k,v in m['common_spaces'].items()})
  ids=['A.entry','B.entry','stair.entry','lift.entry']
  for oid in ids:
   o=openings[oid];q=rect(o['rect']);h=rect(m['wall_hosts'][o['host_wall_id']]);ax=0 if h[2]-h[0]<h[3]-h[1]else 1;ta=1-ax;mid=(h[ax]+h[ax+2])/2
   if q[ax]!=h[ax]or q[ax+2]!=h[ax+2]or not(h[ta]<=q[ta]<q[ta+2]<=h[ta+2]):raise ValueError('APERTURE_HOST:'+oid)
   if any(max(q[0],w[0])<min(q[2],w[2])and max(q[1],w[1])<min(q[3],w[3])for w in map(rect,m['walls'].values())):errors.append('THRESHOLD_SOLID_COLLISION:'+oid)
   allowed={'unit:'+oid[0],'common:lobby'}if oid[0]in'AB'else{'common:'+oid.split('.')[0],'common:lobby'}
   connects={('unit:'+v.split('.')[0])if'.'in v else'common:'+v for v in o['connects']}
   if connects!=allowed:errors.append('THRESHOLD_CONNECTS:'+oid)
   for side in ('minus','plus'):
    face=q[ax]if side=='minus'else q[ax+2];matched=[]
    for owner,regions in owners.items():
     spans=[]
     for r in regions:
      adjacent=(r[ax]<face<=r[ax+2])if side=='minus'else(r[ax]<=face<r[ax+2])
      if adjacent and max(q[ta],r[ta])<min(q[ta+2],r[ta+2]):spans.append((max(q[ta],r[ta]),min(q[ta+2],r[ta+2])))
     if merge(spans)==[(q[ta],q[ta+2])]:matched.append(owner)
    if len(matched)!=1 or matched[0]not in allowed:raise ValueError('ACTUAL_ADJACENCY:'+oid+':'+side+':'+str(matched))
    owner=matched[0];r=list(q);r[ax+2 if side=='minus'else ax]=mid
    found=[a for a in rows if a['opening_id']==oid and a['side']==side]
    if len(found)!=1:raise ValueError('ALLOCATION_INVENTORY')
    a=found[0]
    if a['owner']!=owner or rect(a['rect'])!=tuple(r)or a['host_wall_id']!=o['host_wall_id']or F(a['area_m2'])!=(r[2]-r[0])*(r[3]-r[1])or a['reference_axis']['orientation']!=('vertical'if ax==0 else'horizontal')or F(a['reference_axis']['coordinate'])!=mid:errors.append('ALLOCATION_NOT_ACTUAL:'+oid+':'+side)
    expected.append(('threshold_'+oid+'_'+side+'_'+owner,[tuple(r)]))
  if len(rows)!=len(expected):errors.append('EXTRA_THRESHOLD_ALLOCATION')
 except (KeyError,ValueError,TypeError,IndexError)as ex:errors.append('THRESHOLD_BINDING:'+str(ex))
 return {'errors':errors,'expected':expected,'scope':'Actual clear aperture halves, host reference midline, exact adjacent physical ownership; no installed frame or useful-area claim.'}
