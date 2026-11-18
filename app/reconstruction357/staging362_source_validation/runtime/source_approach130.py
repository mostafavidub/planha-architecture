"""Source-derived external access reservations for the restricted coarse master.
Construction policy, not an owner rule forbidding sequential shared circulation.
Whole checks remain mandatory; the bounding box is deliberately conservative.
"""
from fractions import Fraction as F
from contract114 import digest,S

def module_approach(module):
 unit=module['unit'];role=unit['id']+'.public_access';parts=list(unit['rooms']['public_access'])
 for p in module['external_ports']:
  if p['role_id']!=role:raise ValueError('EXTERNAL_PORT_ROLE_MISMATCH')
  parts.append(p['rect']);x,y=map(F,p['center']);h=F(p['body_width'])/2
  parts.append([x-h,y-h,x+h,y+h])
 for op in module.get('operations',{}).get('doors',[]):
  for state in op['states']:
   if state['role_id']==role:parts.append(state['actor_rect'])
  for seg in op['continuous_actor_segments']:
   if seg['role_id']==role:
    a=list(map(F,seg['actor_start']));b=list(map(F,seg['actor_end']))
    parts.append([min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])])
 rects=[list(map(F,r))for r in parts]
 if not rects:raise ValueError('MISSING_EXTERNAL_APPROACH')
 bbox=[min(r[0]for r in rects),min(r[1]for r in rects),max(r[2]for r in rects),max(r[3]for r in rects)]
 return {'source_module_hash':digest(module),'role':role,'parts':[[S(v)for v in r]for r in rects],'bbox':[S(v)for v in bbox],'policy':'Reserve source public apron, port body, external door actor sweeps against other room/use envelopes. Shared circulation reservations may overlap; no new simultaneous-use law.'}
