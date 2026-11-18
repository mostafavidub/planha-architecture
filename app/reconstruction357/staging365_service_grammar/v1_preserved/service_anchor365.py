"""Finite source-host anchors, identity orientation only. No admission claim."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
SIDES=('left','right')
def q(v):
 if not isinstance(v,(list,tuple))or len(v)!=4:raise ValueError('RECTANGLE')
 r=tuple(F(str(a))for a in v)
 if r[0]>=r[2]or r[1]>=r[3]:raise ValueError('POSITIVE_RECTANGLE')
 return r

def anchors(module,approach,box):
 """Host contact + declared source reservation containment, not full operations."""
 x0,y0,x1,y1=q(box);w=F(module['input_program']['width']);h=F(module['input_program']['depth'])
 if w<=0 or h<=0:raise ValueError('SOURCE_DIMENSIONS')
 shapes=[q(r)for field in ('walls','wall_hosts')for r in module[field].values()]
 shapes +=[q(r)for field in ('fixtures','activities')for r in module['unit'][field].values()]
 shapes +=[q(r)for rs in module['unit']['rooms'].values()for r in rs]
 shapes +=[q(r)for r in approach['parts']]
 shapes +=[(F(0),F(0),w,h)]
 for op in module.get('operations',{}).get('doors',[]):
  shapes +=[q(op[k])for k in ('closed_panel','open_panel','pocket')]
  shapes +=[q(st[k])for st in op['states']for k in ('panel_rect','actor_rect')]
  shapes +=[q(seg[k])for seg in op['continuous_actor_segments']for k in ('actor_start','actor_end')]
 for op in module.get('operations',{}).get('kitchen',[]):
  if op['profile']!='REFERENCE113_ESSENTIAL_KITCHEN_V1' or op['fridge']['angle_range_degrees']!=[0,90] or op['canonical_isometry']['matrix']!=[[-1,0],[0,1]]:raise ValueError('UNSUPPORTED_KITCHEN_MOTION_EXTENT')
  fr=op['fridge'];body=F(fr['body_m']);half=body/2
  def swept_actor(a,b):
   a=list(map(F,a));b=list(map(F,b));return (min(a[0],b[0])-half,min(a[1],b[1])-half,max(a[0],b[0])+half,max(a[1],b[1])+half)
  # This exact source quarter-turn is coordinate-monotonic. Bind endpoints
  # to its hinge/radius/offset rather than trusting arbitrary caller endpoints.
  hx,hy=map(F,fr['hinge']);dx,dy=map(F,fr['actor_offset_m']);gr=F(fr['grip_radius_m'])
  if list(map(F,fr['closed_actor']))!=[hx+dx,hy+dy-gr]or list(map(F,fr['open_actor']))!=[hx+dx+gr,hy+dy]:raise ValueError('SOURCE_FRIDGE_ACTOR_BINDING')
  shapes.append(swept_actor(fr['closed_actor'],fr['open_actor']))
  radius=F(fr['leaf_radius_m']);thick=F(fr['leaf_half_thickness_m']);shapes.append((hx-thick,hy-radius-thick,hx+radius+thick,hy+thick))
  for drawer in op['drawers'].values():
   shapes.append(swept_actor(drawer['closed_actor'],drawer['open_actor']))
   a=q(drawer['closed_tray']);b=q(drawer['open_tray']);shapes.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
  shapes +=[q(st['actor_rect'])for st in op['workstations']]
 lo=min(r[0]for r in shapes);hi=max(r[2]for r in shapes);low=min(r[1]for r in shapes);high=max(r[3]for r in shapes)
 out={}
 for side in SIDES:
  edge=lo if side=='left'else hi;contact=[]
  for key,v in module['wall_hosts'].items():
   r=q(v)
   if (r[0]if side=='left'else r[2])!=edge:continue
   solids=[k for k,z in module['walls'].items()if (q(z)[0]if side=='left'else q(z)[2])==edge and min(q(z)[3],r[3])>max(q(z)[1],r[1])]
   if solids:contact.append({'host':key,'source_rect':list(map(str,r)),'physical_solids':solids})
  if not contact:continue
  x=(x0 if side=='left'else x1)-edge;yl=y0-low;yh=y1-high
  if yl>yh or x+lo<x0 or x+hi>x1:continue
  out[side]={'x':str(x),'y_min':str(yl),'y_max':str(yh),'width':str(w),'height':str(h),'contact':contact,'source_extent':list(map(str,[lo,low,hi,high])),'scope':'DECLARED_SOURCE_RESERVATIONS_ONLY; all source operations/private deletion/full wall connectivity remain mandatory fresh checks'}
 return out

def choose(bath,kitchen,approaches,box,case):
 if case not in ('BATH_RIGHT_KITCHEN_LEFT','BATH_LEFT_KITCHEN_RIGHT'):raise ValueError('UNREGISTERED_FINITE_SIDECASE')
 bs,ks=('right','left')if case=='BATH_RIGHT_KITCHEN_LEFT'else('left','right')
 a=anchors(bath,approaches['bath'],box);b=anchors(kitchen,approaches['kitchen'],box)
 if bs not in a or ks not in b:raise ValueError('SOURCE_HOST_ANCHOR_UNAVAILABLE')
 return {'case':case,'bath':a[bs],'kitchen':b[ks],'orientation':'identity_A_and_source_reflectY_B','not_admission':True}

def validate_rectangles(rectangles,contract):
 for name in ('bath','kitchen'):
  x,y,X,Y=q(rectangles[name]);a=contract[name]
  if x!=F(a['x'])or not F(a['y_min'])<=y<=F(a['y_max'])or X-x!=F(a['width'])or Y-y!=F(a['height']):raise ValueError('SOURCE_ANCHOR_OR_ASSET_DRIFT:'+name)
 return True
