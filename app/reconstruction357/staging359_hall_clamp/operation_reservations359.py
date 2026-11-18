"""Conservative continuous enclosures for explicitly supported source schemas.
Union bounding boxes over continuous endpoints include intervening sweep.
Kitchen rotation uses full hinge-radius enclosure, not endpoint interpolation.
"""
from fractions import Fraction as F
from clamp_geometry359 import rect

def bbox(rects):
 rs=[rect(r)for r in rects]
 if not rs:raise ValueError('EMPTY_SWEEP')
 return [min(r[0]for r in rs),min(r[1]for r in rs),max(r[2]for r in rs),max(r[3]for r in rs)]
def pointbox(p,pad):
 if len(p)!=2:raise ValueError('POINT')
 x,y=map(F,p);h=F(pad)
 if h<=0:raise ValueError('POSITIVE_ENCLOSURE_PAD')
 return [x-h,y-h,x+h,y+h]
def linear_panel(o,body):
 a=rect(o['closed_panel']);b=rect(o['open_panel']);dx,dy=map(F,o['translation'])
 if (a[0]+dx,a[1]+dy,a[2]+dx,a[3]+dy)!=b:raise ValueError('PANEL_TRANSLATION_BINDING')
 rs=[bbox([a,b]),rect(o['pocket'] if o.get('kind')=='pocket_source113'else o['rail_envelope'])]
 if 'open_transfer_points'in o:rs.append(bbox([pointbox(p,body/2)for p in o['open_transfer_points']]))
 if not o['states']or not o['continuous_actor_segments']:raise ValueError('MISSING_CONTINUOUS_STATES')
 for s in o['states']:rs.extend([rect(s['panel_rect']),rect(s['actor_rect']),pointbox(s['hand_point'],body/2)])
 for s in o['continuous_actor_segments']:
  if F(s['t0'])>=F(s['t1']):raise ValueError('MOTION_INTERVAL')
  rs += [bbox([s['actor_start'],s['actor_end']]),bbox([pointbox(s['hand_start'],body/2),pointbox(s['hand_end'],body/2)])]
 return rs

def extract(ops,body):
 body=F(body);out={}
 if set(ops)-{'doors','closets','kitchen','dining_chairs'}:raise ValueError('UNSUPPORTED_OPERATION_GROUP')
 if not ops.get('doors')or not ops.get('closets')or not ops.get('kitchen'):raise ValueError('REQUIRED_OPERATION_GROUP_MISSING')
 for group,items in ops.items():
  for i,o in enumerate(items):
   if group=='doors':
    if o['kind']not in('sliding_linear','pocket_source113'):raise ValueError('UNSUPPORTED_DOOR_MOTION')
    rs=linear_panel(o,body)
   elif group=='closets':
    if not o['panels']:raise ValueError('EMPTY_CLOSET_PANELS')
    rs=[rect(r)for r in o['shell_rects']]
    for p in o['panels']:rs+=linear_panel(p,body)
   elif group=='dining_chairs':
    rs=[bbox([o['closed_rect'],o['open_rect']]),rect(o['occupied_body'])]
    rs += [bbox([pointbox(a,body/2),pointbox(b,body/2)])for a,b in zip(o['egress_route'],o['egress_route'][1:])]
   elif group=='kitchen':
    if o['profile']!='REFERENCE113_ESSENTIAL_KITCHEN_V1':raise ValueError('UNSUPPORTED_KITCHEN_PROFILE')
    f=o['fridge']
    if f['angle_range_degrees']!=[0,90]or f['interval_count']!=360:raise ValueError('UNSUPPORTED_ROTATION')
    # Full disc box encloses leaf, grip, source actor offset and held object.
    radius=max(F(f['leaf_radius_m'])+F(f['leaf_half_thickness_m']),F(f['grip_radius_m'])+sum(abs(F(v))for v in f['actor_offset_m'])+body/2+F(f['object_half_size_m']))
    rs=[pointbox(f['hinge'],radius),bbox([pointbox(f[k],body/2)for k in ('closed_actor','open_actor','open_access','shelf_target','held_target')])]
    for d in o['drawers'].values():
     rs += [bbox([d['closed_tray'],d['open_tray']]),bbox([pointbox(d[k],body/2+F(d['object_half_size_m']))for k in('closed_actor','open_actor','grip_closed','grip_open','storage_target','held_target')])]
    for s in o['workstations']:rs += [rect(s['actor_rect']),pointbox(s['hand_point'],body/2)]
   for j,r in enumerate(rs):out[group+'/'+str(i)+'/'+str(j)]=list(map(str,rect(r)))
 return out
