# Independent experimental fork of frozen search114; upstream blob 65e0f278c9f9ef480388d3ea8056161c0a938a36.
# Adds four-seat protected envelope and shared-body constraints only; no source guard or historical marker change.
"""Bounded rectangle-variable proposal. A solver incumbent is NEVER admission.
Core and real entry apron are fixed first. Room dimensions and locations are
variables; no historical plan file is loaded or selected by requested dimensions.
"""
import math,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
from contract114 import GRID,BODY

def bath_apron_dining_separated(rectangles):
 from fractions import Fraction as F
 from bathroom_module117 import build
 bath=list(map(lambda v:F(str(v)),rectangles['bath']));dining=list(map(lambda v:F(str(v)),rectangles['dining']))
 module=build(str(bath[2]-bath[0]),str(bath[3]-bath[1]))
 gross=module['reserved_approach_gross']
 if gross!=[['7/10','-19/20','23/10','0']]:raise ValueError('SOURCE_BATH_APRON_CHANGED')
 q=list(map(F,gross[0]));a=[q[0]+bath[0],q[1]+bath[1],q[2]+bath[0],q[3]+bath[1]]
 return a[2]<=dining[0] or dining[2]<=a[0] or a[3]<=dining[1] or dining[3]<=a[1]

def propose(core,bedrooms,time_limit=3,variant=0,fixed_witness=None,diagnostic_capture=None,sleep_roles=None,ordered_macro=False,topology="SIDE_ROOTED_SERVICES",organization_profile="UNRESTRICTED"):
 box=list(map(lambda x:float(__import__('fractions').Fraction(str(x))),core['units']['A']));x0,y0,x1,y1=box;ar=(x1-x0)*(y1-y0);scale=float(GRID)
 # No exterior-facade or daylight condition constrains bedroom placement.
 from fractions import Fraction as F
 sleep_roles=sleep_roles or ['double']*bedrooms
 if bedrooms!=2 or sleep_roles!=['double','twin']:raise ValueError('EXPLICIT_TWO_BEDROOM_SHARED_GROUP_ONLY')
 if len(sleep_roles)!=bedrooms or any(r not in('double','twin')for r in sleep_roles):raise ValueError('SLEEP_ROLE_PROGRAM')
 specs=[]
 six_person=bedrooms==3 and sleep_roles==['double','twin','twin']
 for i in range(bedrooms):
  target=max(19.62,min(35,ar*.24/bedrooms));tw=max(5.45,min(7.0,math.sqrt(target*5.45/3.6)));th=max(3.6,min(5.0,target/tw))
  minh=4.5 if sleep_roles[i]=='twin'else 3.6;th=max(minh,th)
  specs.append((f'bed{i+1}',5.45,7.0,minh,5.0,tw,th,'private_room'))
 for name,w,h,wm,hm,ratio in [('bath',3.15,2.25,4.3,3.1,.045),('kitchen',2.35,3.05,3.6,4.2,.05),(('dining',5.4,4.4,6.0,5.0,.04)if six_person else('dining',3.1,3.5,4.2,4.5,.04))]:
  target=max(w*h,min(wm*hm,ar*ratio));tw=max(w,min(wm,math.sqrt(target*w/h)));th=max(h,min(hm,target/tw));specs.append((name,w,wm,h,hm,tw,th,'service'if name=='bath'else'open_room'))
 horizontal=variant%2==0
 for name,w,h in [('sofa1_use',2.2 if horizontal else 1.6,1.6 if horizontal else 2.2),('sofa2_use',2.2,1.6),('chair1_use',.8,1.5),('chair2_use',.8,1.5)]+([('chair3_use',.8,1.5),('chair4_use',.8,1.5)]if six_person else[]):specs.append((name,w,w,h,h,w,h,'furniture_use'))
 ex=float(__import__('fractions').Fraction(core['entry_centers']['A'][0]));specs.append(('entry_apron',2.65,2.65,.9,.9,2.65,.9,'reserved_entry'))
 n=len(specs);nv=4*n;lower=[];upper=[];objective=[];integer=[];rows=[];lbs=[];ubs=[];row_meta=[];group="room_bounds"
 def var(lo,hi,c=0,integ=1):
  j=len(lower);lower.append(lo);upper.append(hi);objective.append(c);integer.append(integ);return j
 for i,(name,w,wm,h,hm,tw,th,role)in enumerate(specs):
  for lo,hi,c in [(math.ceil(x0/scale),math.floor((x1-w)/scale),0),(math.ceil(y0/scale),math.floor((y1-h)/scale),0),(math.ceil(w/scale),math.floor(wm/scale),0),(math.ceil(h/scale),math.floor(hm/scale),0)]:var(lo,hi,c)
 def row(d,lo=-np.inf,hi=np.inf):
  import inspect
  frame=inspect.currentframe().f_back
  while frame.f_code.co_name!='propose':frame=frame.f_back
  row_meta.append({'group':group,'source_line':frame.f_lineno})
  rows.append(d);lbs.append(lo);ubs.append(hi)
 for i,s in enumerate(specs):
  name,w,wm,h,hm,tw,th,role=s;k=4*i
  row({k:1,k+2:1},hi=x1/scale);row({k+1:1,k+3:1},hi=y1/scale)
  if role=='reserved_door_approach':
   bed_idx=next(j for j,z in enumerate(specs)if z[0]==name.replace('_approach',''));bk=4*bed_idx
   row({k:1,bk:-1},lo=-.85/scale,hi=-.85/scale);row({k+1:1,bk+1:-1},lo=0,hi=0)
  # Furniture Y is a spatial decision; fixed-front was not a source rule.
  if name=='sofa1_use':objective[k+1]+=.001
  if name=='entry_apron':
   lower[k]=upper[k]=round((ex-.7)/scale);lower[k+1]=upper[k+1]=math.floor((y1-.9)/scale)
  # Absolute target sizes keep dimensions a decision, not maximal empty rooms.
  for axis,target in ((2,tw),(3,th)):
   e=var(0,10000,1,0);row({k+axis:1,e:-1},hi=target/scale);row({k+axis:-1,e:-1},hi=-target/scale)
  # Soft architectural hints, not mandatory coordinate copies.
  if name=='bath':
   if topology=='FRAME125_SERVICE_SIDE':
    # Actual bathroom right side wall shares the existing unit side boundary.
    # Back/core contact is not retained where it contradicts the real entry.
    row({k:1,k+2:1},lo=x1/scale,hi=x1/scale)
   else:
    row({k+1:1,k+3:1},lo=y1/scale,hi=y1/scale)
    host_left,host_right=map(lambda v:float(F(str(v))),core.get('core_extent_x',[x0,x1]))
    row({k:1},lo=host_left/scale)
    row({k:1,k+2:1},hi=host_right/scale)
   objective[k]+=.008;objective[k+1]-=.015
  elif name=='kitchen':objective[k]+=.008;objective[k+1]+=.006*(1 if variant<2 else -1)
  elif name=='dining':objective[k]+=.003*(-1 if variant%3==2 else 1);objective[k+1]+=.004*(-1 if variant%3==1 else 1)
  elif name.startswith('bed'):objective[k]+=.002*(-1 if variant%2==0 else 1)
 # Explicit bounded functional ordering; not a universal owner rule.
 # Entry is at high local Y: CORE_SIDE places private rooms beyond both
 # service blocks toward entry; OUTER_SIDE places them before the blocks.
 if organization_profile not in ('UNRESTRICTED','PRIVATE_CORE_SIDE','PRIVATE_OUTER_SIDE','COMPACT_FUNCTIONAL_CLUSTER'):raise ValueError('ORGANIZATION_PROFILE')
 group="functional_private_service_order"
 if organization_profile in ('PRIVATE_CORE_SIDE','PRIVATE_OUTER_SIDE'):
  for i,z in enumerate(specs):
   if not z[0].startswith('bed'):continue
   bk=4*i
   for service in ('bath','kitchen'):
    sk=4*next(j for j,t in enumerate(specs)if t[0]==service)
    if organization_profile=='PRIVATE_CORE_SIDE':row({bk+1:1,sk+1:-1,sk+3:-1},lo=.15/scale)
    else:row({sk+1:1,bk+1:-1,bk+3:-1},lo=.15/scale)
 # Engineering objective only: reduce actual program/entry envelope perimeter.
 # All fixed furniture, activities and room constraints remain unchanged.
 if organization_profile=='COMPACT_FUNCTIONAL_CLUSTER':
  group='compact_functional_envelope'
  bx=var(x0/scale,x1/scale,-.1,0);by=var(y0/scale,y1/scale,-.1,0)
  bX=var(x0/scale,x1/scale,.1,0);bY=var(y0/scale,y1/scale,.1,0)
  for i,z in enumerate(specs):
   k=4*i;row({bx:1,k:-1},hi=0);row({by:1,k+1:-1},hi=0)
   row({k:1,k+2:1,bX:-1},hi=0);row({k+1:1,k+3:1,bY:-1},hi=0)
 # No all-bedroom X ordering: it would silently retain the removed front row.
 # Facing pairs below are a limited physical approach topology, not a facade rule.
 M=max(x1-x0,y1-y0)/scale+2000
 group="independent_four_seat_group_envelope"
 seat_indices=[i for i,z in enumerate(specs) if z[7]=='furniture_use']
 if len(seat_indices)!=4:raise ValueError('FOUR_SOURCE_SEAT_USES_REQUIRED')
 gl=var(math.ceil(x0/scale),math.floor(x1/scale),-.01)
 gb=var(math.ceil(y0/scale),math.floor(y1/scale),-.01)
 gr=var(math.ceil(x0/scale),math.floor(x1/scale),.01)
 gt=var(math.ceil(y0/scale),math.floor(y1/scale),.01)
 for i in seat_indices:
  k=4*i;row({gl:1,k:-1},hi=0);row({gb:1,k+1:-1},hi=0)
  row({k:1,k+2:1,gr:-1},hi=0);row({k+1:1,k+3:1,gt:-1},hi=0)
 # Every envelope edge is an actual use edge, never an artificially inflated bbox.
 for edge,axis,far in ((gl,0,False),(gb,1,False),(gr,0,True),(gt,1,True)):
  zs=[]
  for i in seat_indices:
   k=4*i;z=var(0,1);zs.append(z)
   d={edge:1,k+axis:-1}
   if far:d[k+axis+2]=-1
   row(d|{z:-M},hi=0);row({j:-v for j,v in d.items()}|{z:-M},hi=0)
  row({z:1 for z in zs},hi=len(zs)-1)
 for i,sp in enumerate(specs):
  if i in seat_indices:continue
  k=4*i;margin=.15/scale if sp[7] in ('private_room','service','open_room') else 0
  zs=[var(0,1) for _ in range(4)];row({z:1 for z in zs},hi=3)
  row({gr:1,k:-1,zs[0]:-M},hi=-margin)
  row({k:1,k+2:1,gl:-1,zs[1]:-M},hi=-margin)
  row({gt:1,k+1:-1,zs[2]:-M},hi=-margin)
  row({k+1:1,k+3:1,gb:-1,zs[3]:-M},hi=-margin)
 group="independent_four_seat_shared_body"
 bs=float(BODY)/scale
 wx=var(math.ceil(x0/scale),math.floor(x1/scale-bs));wy=var(math.ceil(y0/scale),math.floor(y1/scale-bs))
 row({gl:1,wx:-1},hi=0);row({gb:1,wy:-1},hi=0)
 row({wx:1,gr:-1},hi=-bs);row({wy:1,gt:-1},hi=-bs)
 for i in seat_indices:
  k=4*i;zs=[var(0,1) for _ in range(4)];row({z:1 for z in zs},hi=3)
  row({wx:1,k:-1,zs[0]:-M},hi=-bs)
  row({k:1,k+2:1,wx:-1,zs[1]:-M},hi=0)
  row({wy:1,k+1:-1,zs[2]:-M},hi=-bs)
  row({k+1:1,k+3:1,wy:-1,zs[3]:-M},hi=0)
 group="kitchen_functional_boundary_attachment"
 # Attach an actual kitchen side boundary to an existing plot side wall.
 # This is a bounded topology choice, not an arbitrary connecting wall or a
 # claim that every feasible kitchen must touch a perimeter wall.
 ki=next(i for i,z in enumerate(specs)if z[0]=='kitchen');kk=4*ki
 if topology=='CORE_ROOTED_SERVICES':
  # Alternative actual organization: kitchen and bath both share the existing
  # central unit/core boundary. Source kitchen back wall is physical, not a
  # decorative connector. All room separation and operations remain mandatory.
  cl,cr=map(lambda v:float(F(str(v))),core['core_extent_x'])
  row({kk+1:1,kk+3:1},lo=y1/scale,hi=y1/scale)
  row({kk:1},lo=cl/scale);row({kk:1,kk+2:1},hi=cr/scale)
 elif topology in ('KITCHEN_BATH_SHARED_SIDE','FRAME125_SERVICE_SIDE'):
  # Two real service-room boundaries coincide in the .15m shared wall;
  # bathroom retains its actual core attachment. No artificial wall bridge.
  bk=4*next(i for i,z in enumerate(specs)if z[0]=='bath')
  row({kk:1,kk+2:1,bk:-1},lo=-.15/scale,hi=-.15/scale)
  row({kk+1:1,kk+3:1,bk+1:-1,bk+3:-1},lo=0,hi=0)
 elif topology=='SIDE_ROOTED_SERVICES':
  side=var(0,1)
  row({kk:1,side:-M},hi=x0/scale)
  row({kk:1,kk+2:1,side:-M},lo=x1/scale-M)
 else:raise ValueError('UNSUPPORTED_ORGANIZATION_TOPOLOGY')
 group="bedroom_actual_wall_attachment"
 # Each bedroom host must physically meet an already rooted wall. These are
 # wall-network choices, including closed side/core walls, not opening/light rules.
 # No connector wall is created and the room remains a variable rectangle.
 def contact_option(constraints):
  z=var(0,1)
  for d,lo,hi in constraints:
   if lo is not None:row({**d,z:d.get(z,0)+M},lo=lo)
   if hi is not None:row({**d,z:d.get(z,0)-M},hi=hi)
  return z
 for bi in range(bedrooms):
  k=4*bi;options=[]
  for d,value in (({k:1},x0/scale),({k:1,k+2:1},x1/scale),({k+1:1},y0/scale)):
   options.append(contact_option([(d,value,value)]))
  cl,cr=map(lambda v:float(F(str(v))),core.get('core_extent_x',[x0,x1]))
  options.append(contact_option([({k+1:1,k+3:1},y1/scale,y1/scale),({k:1},None,(cr-.15)/scale),({k:1,k+2:1},(cl+.15)/scale,None)]))
  # Positive overlap with a source service wall; .15 gap is occupied by the
  # actual source wall skins/hosts, not an empty bridge. All actor gates remain.
  for service in ('bath','kitchen'):
   sk=4*next(i for i,z in enumerate(specs)if z[0]==service)
   for axis in (0,1):
    other=1-axis
    overlap=[({k+other:1,sk+other:-1,sk+other+2:-1},None,-.15/scale),({k+other:1,k+other+2:1,sk+other:-1},.15/scale,None)]
    for d in ({k+axis:1,k+axis+2:1,sk+axis:-1},{sk+axis:1,sk+axis+2:1,k+axis:-1}):
     options.append(contact_option([(d,-.15/scale,-.15/scale)]+overlap))
  row({z:1 for z in options},hi=len(options)-1)
 group="physical_rectangle_separation"
 for i in range(n):
  for j in range(i+1,n):
   ai,aj=4*i,4*j;ri,rj=specs[i][7],specs[j][7];sep=.15 if ri in('private_room','service','open_room')or rj in('private_room','service','open_room')else 0
   b=[var(0,1,0,1)for _ in range(4)];row({k:1 for k in b},hi=3)
   row({ai:1,ai+2:1,aj:-1,b[0]:-M},hi=-sep/scale)
   row({aj:1,aj+2:1,ai:-1,b[1]:-M},hi=-sep/scale)
   row({ai+1:1,ai+3:1,aj+1:-1,b[2]:-M},hi=-sep/scale)
   row({aj+1:1,aj+3:1,ai+1:-1,b[3]:-M},hi=-sep/scale)
 # Connected route skeleton: each terminal joins the actual entry by a
 # variable three-segment orthogonal path. No fixed corridor coordinates.
 # This bounded topology is not a universal routing completeness claim.
 rootx=ex/scale;rooty=(y1-.4)/scale;half=.35/scale
 def aff(j,c=1):return ({j:c},0.)
 def plus(*terms):
  d={};c=0.
  for dd,cc in terms:
   c+=cc
   for j,v in dd.items():d[j]=d.get(j,0)+v
  return d,c
 def const(x):return ({},x/scale)
 def neg(a):return ({j:-v for j,v in a[0].items()},-a[1])
 def lin(a,lo=-np.inf,hi=np.inf):row(a[0],lo-a[1],hi-a[1])
 def bind(j,a):lin(plus(aff(j),neg(a)),0,0)
 def either_eq(j,a,b,z):
  # z=0 ->a; z=1 ->b.
  d=plus(aff(j),neg(a));lin(plus(d,aff(z,-M)),hi=0);lin(plus(d,aff(z,M)),lo=0)
  d=plus(aff(j),neg(b));lin(plus(d,aff(z,M)),hi=M);lin(plus(d,aff(z,-M)),lo=-M)
 obstacles=[];terminaldefs=[];bedroom_motion_reservations=[]
 for i,sp in enumerate(specs):
  name=sp[0];k=4*i;X=aff(k);Y=aff(k+1);XX=plus(X,aff(k+2));YY=plus(Y,aff(k+3));role=sp[7]
  if role in('private_room','service','open_room') and name!='dining':
   margin=.15 if role in('private_room','service')or name=='kitchen'else 0
   obstacles.append((name,[plus(X,const(-margin)),plus(Y,const(-margin)),plus(XX,const(margin)),plus(YY,const(margin))]))
  elif name.startswith('sofa'):
   vertical=name=='sofa1_use'and not horizontal
   obstacles.append((name,[plus(X,const(.7))if vertical else X,Y,XX,YY if vertical else plus(Y,const(.9))]))
  elif name.startswith('chair'):
   obstacles.append((name,[X,plus(Y,const(.7)),XX,YY]))
  if name.startswith('bed'):
   px=var((x0+.35)/scale,(x1-.35)/scale);py=var((y0+.35)/scale,(y1-.35)/scale);side=var(0,1)
   either_eq(px,plus(X,const(-.55)),plus(XX,const(.55)),side);bind(py,plus(Y,const(.7)));terminaldefs.append((name,px,py,side))
  elif name in('bath','kitchen'):
   px=var((x0+.35)/scale,(x1-.35)/scale);py=var((y0+.35)/scale,(y1-.35)/scale)
   bind(px,plus(X,const(1.525 if name=='bath'else 1.1)));bind(py,plus(Y,const(-.55 if name=='kitchen'else-.5)));terminaldefs.append((name,px,py,None))
  elif name=='dining':
   # Derive all four actual standing endpoints and rigid obstacles from the
   # unchanged source module. Room width/depth translate its centered furniture;
   # no guessed center-port or replacement two-chair program is used.
   if six_person:
    from dining_module121 import build as dining_geometry
   else:
    from dining_module118 import build as dining_geometry
   dm=dining_geometry('4','4');cx=plus(X,aff(k+2,.5));cy=plus(Y,aff(k+3,.5))
   def dq(q):
    return [plus(cx,const(float(F(str(q[0])))-2)),plus(cy,const(float(F(str(q[1])))-2)),plus(cx,const(float(F(str(q[2])))-2)),plus(cy,const(float(F(str(q[3])))-2))]
   # Closed chair rectangles are already contained in their exact pull
   # envelopes below; avoid duplicate disjunctions without changing obstacles.
   for fid,q in dm['fixtures'].items():
    if fid=='table':obstacles.append(('dining.fixture.'+fid,dq(q)))
   from approach_contract123 import dining_actor_sweeps
   bedroom_motion_reservations.extend(('dining.actor.'+sid,dq(q)) for sid,q in dining_actor_sweeps(dm))
   for seat in dm['seating']['instances']:
    q=list(map(F,seat['rise_transfer']['standing_body']));tx=(q[0]+q[2])/2-F(2);ty=(q[1]+q[3])/2-F(2)
    px=var((x0+.35)/scale,(x1-.35)/scale,integ=0);py=var((y0+.35)/scale,(y1-.35)/scale,integ=0)
    bind(px,plus(cx,const(float(tx))));bind(py,plus(cy,const(float(ty))))
    terminaldefs.append(('dining_'+(seat['id']if six_person else seat['id'][5:]),px,py,None))
    a=list(map(F,seat['closed_rect']));b=list(map(F,seat['pulled_rect']))
    swept=[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])]
    obstacles.append(('dining.pull.'+seat['id'],dq(swept)))
    obstacles.append(('dining.occupied.'+seat['id'],dq(seat['occupied_body'])))
  elif name.startswith(('sofa','chair')):
   px=var((x0+.35)/scale,(x1-.35)/scale);py=var((y0+.35)/scale,(y1-.35)/scale)
   if name.startswith('sofa'):
    bind(px,plus(X,const(.35 if name=='sofa1_use'and not horizontal else 1.1)))
    bind(py,plus(Y,const(1.1 if name=='sofa1_use'and not horizontal else 1.25)))
   else:bind(px,plus(X,const(.4)));bind(py,plus(Y,const(.35)))
   terminaldefs.append((name,px,py,None))
 group="independent_four_seat_local_body_routes"
 # Additional restricted local network from the shared body to actual source
 # seat ports. These constraints add to, never replace, the entry network.
 def group_span(a,b,low,high):
  lo=var(low,high,-.0001,0);hi=var(low,high,.0001,0)
  lin(plus(aff(lo),neg(a)),hi=0);lin(plus(aff(lo),neg(b)),hi=0)
  lin(plus(aff(hi),neg(a)),lo=0);lin(plus(aff(hi),neg(b)),lo=0)
  return aff(lo),aff(hi)
 group_routes=[];group_startx=plus(aff(wx),({},bs/2));group_starty=plus(aff(wy),({},bs/2))
 seat_names={specs[i][0] for i in seat_indices}
 for name,px,py,_side in terminaldefs:
  if name not in seat_names:continue
  jx=var(x0/scale,x1/scale)
  xa,xb=group_span(group_startx,aff(jx),x0/scale,x1/scale)
  ya,yb=group_span(group_starty,aff(py),y0/scale,y1/scale)
  xc,xd=group_span(aff(jx),aff(px),x0/scale,x1/scale)
  segments=[[plus(xa,({},-bs/2)),plus(group_starty,({},-bs/2)),plus(xb,({},bs/2)),plus(group_starty,({},bs/2))],
            [plus(aff(jx),({},-bs/2)),plus(ya,({},-bs/2)),plus(aff(jx),({},bs/2)),plus(yb,({},bs/2))],
            [plus(xc,({},-bs/2)),plus(aff(py),({},-bs/2)),plus(xd,({},bs/2)),plus(aff(py),({},bs/2))]]
  for seg in segments:
   lin(plus(seg[0],neg(aff(gl))),lo=0);lin(plus(seg[1],neg(aff(gb))),lo=0)
   lin(plus(seg[2],neg(aff(gr))),hi=0);lin(plus(seg[3],neg(aff(gt))),hi=0)
   for oname,ob in obstacles:
    zz=[var(0,1) for _ in range(4)];row({j:1 for j in zz},hi=3)
    for expr,z in zip([plus(seg[2],neg(ob[0])),plus(ob[2],neg(seg[0])),plus(seg[3],neg(ob[1])),plus(ob[3],neg(seg[1]))],zz):lin(plus(expr,aff(z,-M)),hi=0)
  group_routes.append((name,px,py,jx))
 group="paired_private_apron"
 # Adjacent private modules face one actual 1.0m clear common approach:
 # 0.15m side wall + 1.0m clear floor + 0.15m side wall.
 for bi in range(0,bedrooms-1,2):
  left=next(t for t in terminaldefs if t[0]=='bed'+str(bi+1));right=next(t for t in terminaldefs if t[0]=='bed'+str(bi+2))
  lower[left[3]]=upper[left[3]]=1;lower[right[3]]=upper[right[3]]=0
  row({4*(bi+1):1,4*bi:-1,4*bi+2:-1},lo=1.3/scale,hi=1.3/scale)
  row({4*(bi+1)+1:1,4*bi+1:-1},lo=0,hi=0) # actual shared approach, not facade alignment
 # A facing pair needs a physically closed end, not a facade requirement.
 # The existing exterior front OR an actual wet/kitchen back host may close
 # the clear approach. This topology creates no extra partition.
 group="paired_approach_existing_end_host"
 for bi in range(0,bedrooms-1,2):
  bk=4*bi;rk=4*(bi+1);options=[]
  options.append(contact_option([({bk+1:1},y0/scale,y0/scale)]))
  for service in ('bath','kitchen'):
   sk=4*next(i for i,z in enumerate(specs)if z[0]==service)
   options.append(contact_option([
    ({bk+1:1,sk+1:-1,sk+3:-1},.15/scale,.15/scale),
    ({sk:1,bk:-1,bk+2:-1},None,.15/scale),
    ({sk:1,sk+2:1,rk:-1},-.15/scale,None)]))
  row({z:1 for z in options},hi=len(options)-1)
 if ordered_macro:
  from ordered_macro121 import build as build_macro
  macro=build_macro(core,variant)
  if not six_person or macro is None:return {'status':'NO_PROPOSAL_IN_THIS_TOPOLOGY','reason':'ORDERED_SIX_PERSON_MACRO_NOT_APPLICABLE','bedrooms':bedrooms,'variant':variant,'no_global_infeasibility_claim':True}
  group="ordered_macro_restricted_topology"
  for i,sp in enumerate(specs):
   if sp[0]not in macro['rectangles']:continue
   q=list(map(F,macro['rectangles'][sp[0]]))
   for axis,v in enumerate((q[0],q[1],q[2]-q[0],q[3]-q[1])):lower[4*i+axis]=upper[4*i+axis]=float(v/F(str(scale)))
  for name,px,py,side in terminaldefs:
   if side is not None:lower[side]=upper[side]=int(macro['bed_door_sides'][name]=='right')
 network=[]
 junction=var((x0+.35)/scale,(x1-.35)/scale)
 def minmax(a,b,low,high):
  lo=var(low,high,-.0001);hi=var(low,high,.0001)
  lin(plus(aff(lo),neg(a)),hi=0);lin(plus(aff(lo),neg(b)),hi=0)
  lin(plus(aff(hi),neg(a)),lo=0);lin(plus(aff(hi),neg(b)),lo=0)
  return aff(lo),aff(hi)
 group="shared_root_body_segment"
 # The root-to-junction body sweep is literally common to every route.
 # Constrain it once against every unchanged obstacle, not once per terminal.
 jlo,jhi=minmax(({},rootx),aff(junction),x0/scale,x1/scale)
 # Preserve the old repeated root min/max objective weight exactly after
 # hard-constraint factoring. The explicit L1 compactness term below is a
 # separate, disclosed objective change, not part of the equivalence claim.
 for j in jlo[0]:objective[j]-=.0001*(len(terminaldefs)-1)
 for j in jhi[0]:objective[j]+=.0001*(len(terminaldefs)-1)
 sharedseg=[plus(jlo,({},-half)),({},rooty-half),plus(jhi,({},half)),({},rooty+half)]
 for idx,lo,hi in ((0,x0/scale,np.inf),(1,y0/scale,np.inf),(2,-np.inf,x1/scale),(3,-np.inf,y1/scale)):lin(sharedseg[idx],lo=lo,hi=hi)
 for oname,ob in obstacles:
  zz=[var(0,1)for _ in range(4)];row({j:1 for j in zz},hi=3)
  for expr,z in zip([plus(sharedseg[2],neg(ob[0])),plus(ob[2],neg(sharedseg[0])),plus(sharedseg[3],neg(ob[1])),plus(ob[3],neg(sharedseg[1]))],zz):lin(plus(expr,aff(z,-M)),hi=0)
 group="rooted_body_network"
 for name,px,py,side in terminaldefs:
  # Explicit engineering preference for compact functional placement, not a
  # mandated maximum distance or evidence of global architectural optimality.
  for node,rootcoord in ((px,rootx),(py,rooty)):
   deviation=var(0,M,.01,0);row({node:1,deviation:-1},hi=rootcoord);row({node:-1,deviation:-1},hi=-rootcoord)
  bend=var((y0+.35)/scale,(y1-.35)/scale)
  ylo,yhi=minmax(({},rooty),aff(bend),y0/scale,y1/scale)
  xlo,xhi=minmax(aff(junction),aff(px),x0/scale,x1/scale)
  plo,phi=minmax(aff(py),aff(bend),y0/scale,y1/scale)
  segments=[ [plus(aff(junction),({},-half)),plus(ylo,({},-half)),plus(aff(junction),({},half)),plus(yhi,({},half))],
   [plus(xlo,({},-half)),plus(aff(bend),({},-half)),plus(xhi,({},half)),plus(aff(bend),({},half))],
   [plus(aff(px),({},-half)),plus(plo,({},-half)),plus(aff(px),({},half)),plus(phi,({},half))] ]
  for seg in segments:
   lin(seg[0],lo=x0/scale);lin(seg[1],lo=y0/scale);lin(seg[2],hi=x1/scale);lin(seg[3],hi=y1/scale)
   for oname,ob in obstacles:
    zz=[var(0,1)for _ in range(4)];row({j:1 for j in zz},hi=3)
    for expr,z in zip([plus(seg[2],neg(ob[0])),plus(ob[2],neg(seg[0])),plus(seg[3],neg(ob[1])),plus(ob[3],neg(seg[1]))],zz):lin(plus(expr,aff(z,-M)),hi=0)
  network.append((name,px,py,bend,side))
 group="bedroom_actual_approach"
 # Module exterior apron is real reserved floor, not a discarded bbox.
 for name,px,py,side in terminaldefs:
  if side is None:continue
  i=next(j for j,z in enumerate(specs)if z[0]==name);k=4*i;X=aff(k);Y=aff(k+1);XX=plus(X,aff(k+2))
  apronx=var(x0/scale,x1/scale);either_eq(apronx,plus(X,const(-1)),XX,side)
  apron=[aff(apronx),Y,plus(aff(apronx),const(1)),plus(Y,const(2.4))]
  lin(apron[0],lo=x0/scale);lin(apron[2],hi=x1/scale);lin(apron[3],hi=y1/scale)
  for oname,ob in obstacles+bedroom_motion_reservations:
   if oname==name:continue
   zz=[var(0,1)for _ in range(4)];row({j:1 for j in zz},hi=3)
   for expr,z in zip([plus(apron[2],neg(ob[0])),plus(ob[2],neg(apron[0])),plus(apron[3],neg(ob[1])),plus(ob[3],neg(apron[1]))],zz):lin(plus(expr,aff(z,-M)),hi=0)
 group="kitchen_actual_approach"
 # Real kitchen exterior approach, bound to front permanent arch.
 ki=next(i for i,z in enumerate(specs)if z[0]=='kitchen');k=4*ki
 apron=[plus(aff(k),const(.45)),plus(aff(k+1),const(-1)),plus(aff(k),const(1.75)),aff(k+1)]
 lin(apron[0],lo=x0/scale);lin(apron[1],lo=y0/scale);lin(apron[2],hi=x1/scale)
 for oname,ob in obstacles:
  if oname=='kitchen':continue
  zz=[var(0,1)for _ in range(4)];row({j:1 for j in zz},hi=3)
  for expr,z in zip([plus(apron[2],neg(ob[0])),plus(ob[2],neg(apron[0])),plus(apron[3],neg(ob[1])),plus(ob[3],neg(apron[1]))],zz):lin(plus(expr,aff(z,-M)),hi=0)
 group="bathroom_actual_approach"
 # Source wet-room front approach, actual port/actor reservation.
 ki=next(i for i,z in enumerate(specs)if z[0]=='bath');k=4*ki
 apron=[plus(aff(k),const(.7)),plus(aff(k+1),const(-.95)),plus(aff(k),const(2.3)),aff(k+1)]
 lin(apron[0],lo=x0/scale);lin(apron[1],lo=y0/scale);lin(apron[2],hi=x1/scale)
 for oname,ob in obstacles:
  if oname=='bath':continue
  zz=[var(0,1)for _ in range(4)];row({j:1 for j in zz},hi=3)
  for expr,z in zip([plus(apron[2],neg(ob[0])),plus(ob[2],neg(apron[0])),plus(apron[3],neg(ob[1])),plus(ob[3],neg(apron[1]))],zz):lin(plus(expr,aff(z,-M)),hi=0)
 group="independent_bath_apron_typed_public_floor"
 # Full source approach must not enter dining, a different typed floor role.
 # Preserve every previous obstacle constraint; zero extra architectural margin.
 from bathroom_module117 import build as source_bath
 if source_bath()['reserved_approach_gross']!=[['7/10','-19/20','23/10','0']]:raise ValueError('SOURCE_BATH_APRON_CHANGED')
 dk=4*next(i for i,z in enumerate(specs) if z[0]=='dining')
 dining_floor=[aff(dk),aff(dk+1),plus(aff(dk),aff(dk+2)),plus(aff(dk+1),aff(dk+3))]
 zz=[var(0,1) for _ in range(4)];row({z:1 for z in zz},hi=3)
 for expr,z in zip([plus(apron[2],neg(dining_floor[0])),plus(dining_floor[2],neg(apron[0])),plus(apron[3],neg(dining_floor[1])),plus(dining_floor[3],neg(apron[1]))],zz):lin(plus(expr,aff(z,-M)),hi=0)
 if any(a>b for a,b in zip(lower,upper)):return {'status':'NO_PROPOSAL_IN_THIS_PROGRAM','reason':'ROOM_OR_CORE_BOUND_CONFLICT','bedrooms':bedrooms,'variant':variant}
 diagnostic=None
 if fixed_witness is not None:
  # Bind existing physical and route geometry, never a different bedroom program.
  from fractions import Fraction as F
  assignment={};mapping=[]
  def fixed(j,value,meaning):
   v=F(str(value))/F(str(scale));assignment[j]=v
   mapping.append({'variable':j,'meaning':meaning,'metres':str(value),'grid_value':str(v)})
  for i,sp in enumerate(specs):
   q=list(map(lambda v:F(str(v)),fixed_witness['rectangles'][sp[0]]))
   for a,v in enumerate((q[0],q[1],q[2]-q[0],q[3]-q[1])):fixed(4*i+a,v,sp[0]+'.'+('x','y','width','height')[a])
  for name,px,py,bend,side in network:
   path=fixed_witness['network_paths'][name]
   fixed(px,path[-1][0],name+'.port.x');fixed(py,path[-1][1],name+'.port.y');fixed(bend,path[-2][1],name+'.bend.y')
   fixed(junction,path[1][0]if len(path)==5 else rootx*scale,'shared_junction.x')
   if side is not None:assignment[side]=F(int(fixed_witness['bed_door_sides'][name]=='right'));mapping.append({'variable':side,'meaning':name+'.door_side','grid_value':str(assignment[side])})
  violations=[]
  for j,v in assignment.items():
   if v<F(str(lower[j])) or v>F(str(upper[j])):violations.append({'kind':'BOUND','variable':j,'value':str(v),'lower':str(lower[j]),'upper':str(upper[j])})
  # Exact rational interval arithmetic on the actual emitted coefficients.
  # Auxiliary binaries may remain free; an impossible interval is a certificate.
  for ri,d in enumerate(rows):
   lo=F(0);hi=F(0)
   for j,c in d.items():
    c=F(str(c));a=b=assignment[j] if j in assignment else None
    if a is None:a,b=F(str(lower[j])),F(str(upper[j]))
    lo+=min(c*a,c*b);hi+=max(c*a,c*b)
   if (np.isfinite(lbs[ri]) and hi<F(str(lbs[ri])))or(np.isfinite(ubs[ri])and lo>F(str(ubs[ri]))):violations.append({'kind':'ROW_INTERVAL','row':ri,**row_meta[ri],'minimum':str(lo),'maximum':str(hi),'lower':str(lbs[ri]),'upper':str(ubs[ri]),'coefficients':d})
  diagnostic={'schema':'FIXED_WITNESS118','assignment':mapping,'fixed_variables':len(assignment),'violations':violations,'row_groups':{g:sum(r['group']==g for r in row_meta)for g in sorted(set(r['group']for r in row_meta))},'row_metadata':row_meta,'rational_scope':'Exact arithmetic on serialized master coefficients; not a replacement for physical Fraction gate.'}
  if violations:return {'status':'FIXED_WITNESS_CONSTRAINT_REJECTED','diagnostic':diagnostic,'no_global_infeasibility_claim':True}
  for j,v in assignment.items():lower[j]=upper[j]=float(v)
 A=lil_matrix((len(rows),len(lower)))
 for i,d in enumerate(rows):
  for j,v in d.items():A[i,j]=v
 if diagnostic_capture is not None:
  return diagnostic_capture({'objective':np.array(objective),'integrality':np.array(integer),'bounds':Bounds(lower,upper),'matrix':A.tocsr(),'lower':np.array(lbs),'upper':np.array(ubs),'row_metadata':row_meta,'specs':specs})
 start=time.monotonic();r=milp(np.array(objective),integrality=np.array(integer),bounds=Bounds(lower,upper),constraints=LinearConstraint(A.tocsr(),lbs,ubs),options={'time_limit':time_limit,'mip_rel_gap':.02,'presolve':True})
 out={'organization_profile':organization_profile,'organization_topology':topology,'objective_profile':'REPEATED_ROOT_WEIGHT_PRESERVED_PLUS_EXPLICIT_TERMINAL_L1_0.01_COMPACT_STUDY','capacity_profile':'SIX_PERSON_INTERNAL_PROGRAM121'if six_person else'LEGACY_SOURCE_PROGRAM','sleep_roles':sleep_roles,'status':'PROPOSAL_ONLY'if r.x is not None else'SEARCH_TIMEOUT_NO_WITNESS'if r.status==1 else'NO_PROPOSAL_IN_THIS_TOPOLOGY','solver_status':int(r.status),'solver_message':r.message,'solver_seconds':time.monotonic()-start,'budget_seconds':time_limit,'bedrooms':bedrooms,'variant':variant,'variables':len(lower),'binary_separation_variables':4*n*(n-1)//2,'constraints':len(rows),'no_global_infeasibility_claim':True}
 if ordered_macro:out['ordered_macro']=macro
 if diagnostic is not None:out['diagnostic']=diagnostic
 if r.x is not None:
  # Float post-round prefilter only; independent Fraction gate decides admission.
  vals=r.x.copy()
  for j,z in enumerate(integer):
   if z:vals[j]=round(vals[j])
  residual=A@vals
  if np.any(residual<np.array(lbs)-1e-7)or np.any(residual>np.array(ubs)+1e-7):out['status']='ROUNDED_PROPOSAL_REJECTED';return out
  out['rectangles']={s[0]:[round(vals[4*i]*scale,6),round(vals[4*i+1]*scale,6),round((vals[4*i]+vals[4*i+2])*scale,6),round((vals[4*i+1]+vals[4*i+3])*scale,6)]for i,s in enumerate(specs)}
  if not bath_apron_dining_separated(out['rectangles']):
   out['status']='EXACT_BATH_APRON_TYPED_FLOOR_REJECTED';return out
  out['independent_shared_group_study']={'schema':'V25_FOUR_SEAT_ENVELOPE_PROPOSAL_ONLY','envelope':[round(vals[j]*scale,6) for j in (gl,gb,gr,gt)],'body_witness':[round(vals[wx]*scale,6),round(vals[wy]*scale,6),round(vals[wx]*scale+float(BODY),6),round(vals[wy]*scale+float(BODY),6)],'seat_uses':[specs[i][0] for i in seat_indices],'source_body_m':str(BODY),'historical_shared_gate_marker':False,'accepted':False}
  from fractions import Fraction as F
  group_box=list(map(lambda v:F(str(v)),out['independent_shared_group_study']['envelope']))
  witness=list(map(lambda v:F(str(v)),out['independent_shared_group_study']['body_witness']))
  uses=[list(map(lambda v:F(str(v)),out['rectangles'][specs[i][0]])) for i in seat_indices]
  actual=[min(q[0] for q in uses),min(q[1] for q in uses),max(q[2] for q in uses),max(q[3] for q in uses)]
  def intersects(a,b):return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])
  protected=[(list(map(lambda v:F(str(v)),out['rectangles'][sp[0]])),F('.15') if sp[7] in ('private_room','service','open_room') else F(0)) for i,sp in enumerate(specs) if i not in seat_indices]
  exact_core=list(map(lambda v:F(str(v)),core['units']['A']))
  def separated(a,b,margin):return a[2]+margin<=b[0] or b[2]+margin<=a[0] or a[3]+margin<=b[1] or b[3]+margin<=a[1]
  source_body=F(str(BODY))
  if group_box!=actual or not(group_box[0]<=witness[0]<witness[2]<=group_box[2] and group_box[1]<=witness[1]<witness[3]<=group_box[3]) or any(intersects(witness,q) for q in uses) or any(not separated(group_box,q,margin) for q,margin in protected) or witness[2]-witness[0]!=source_body or witness[3]-witness[1]!=source_body or not(exact_core[0]<=group_box[0]<group_box[2]<=exact_core[2] and exact_core[1]<=group_box[1]<group_box[3]<=exact_core[3]):
   out['status']='EXACT_GROUP_PREFILTER_REJECTED';return out
  out['independent_shared_group_study']['network_paths']={name:[[round((vals[wx]+bs/2)*scale,6),round((vals[wy]+bs/2)*scale,6)],[round(vals[jx]*scale,6),round((vals[wy]+bs/2)*scale,6)],[round(vals[jx]*scale,6),round(vals[py]*scale,6)],[round(vals[px]*scale,6),round(vals[py]*scale,6)]] for name,px,py,jx in group_routes}
  out['roles']={s[0]:s[7]for s in specs}
  out['network_paths']={name:[[round(rootx*scale,6),round(rooty*scale,6)],[round(vals[junction]*scale,6),round(rooty*scale,6)],[round(vals[junction]*scale,6),round(vals[bend]*scale,6)],[round(vals[px]*scale,6),round(vals[bend]*scale,6)],[round(vals[px]*scale,6),round(vals[py]*scale,6)]]for name,px,py,bend,side in network}
  out['bed_door_sides']={name:('right'if vals[side]>.5 else'left')for name,px,py,bend,side in network if side is not None}
  out['private_module_contract']='PRIVATE_ROOM_GEOMETRY_OPERATIONS_V1; variable W>=5.45 H>=3.6; full module independently checked before and after placement'
  out['network_scope']='shared variable junction with actual root connector and 3-segment junction-to-terminal paths; limited topology, not complete router' 
 return out
