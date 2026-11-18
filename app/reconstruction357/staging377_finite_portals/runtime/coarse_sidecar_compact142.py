"""Dynamic-service restricted master over one real three-bedroom bundle and public uses.
The full source/hall envelope is conservatively reserved; no room/operation relaxation. Whole independent checks remain mandatory.
"""
from fractions import Fraction as F
import time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from contract114 import S,BODY
from private_sidecar_source136 import build as private_source

def reservation_fit(core,template):
 """Exact preflight of every fixed reservation; not a solver or admission."""
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);left=F(template['origin'][0]);right=left+F('16.7');back=y0+F('6.9')
 reservations={
  'private_block':(left,y0,F('16.7'),F('6.9')),
  'entry_apron':(ex-F('.7'),y1-F('.9'),F('2.65'),F('.9')),
  'private_trunk':(ex-F('.35'),back,F('.7'),y1-F('.4')-back),
  'public_upper':(left-F('.9'),back,F('18.5'),F('.7')),
  'public_left':(left-F('.9'),y0,F('.7'),back-y0+F('.7')),
  'public_right':(right+F('.2'),y0,F('.7'),back-y0+F('.7'))}
 errors=[]
 for name,(x,y,w,h)in reservations.items():
  if w<=0 or h<=0:errors.append(name+':NONPOSITIVE_DIMENSION')
  if x<x0 or y<y0 or x+w>x1 or y+h>y1:errors.append(name+':OUTSIDE_UNIT')
 return reservations,errors

SEAT_USES=tuple(['sofa1_use','sofa2_use']+[f'chair{i}_use'for i in range(1,5)])

def add_seating_envelope(index,box,var,row,M):
 """Research-only protected envelope; zero objective cost, no source resizing."""
 x0,y0,x1,y1=map(F,box)
 if any(n not in index for n in SEAT_USES):raise ValueError('SIX_ACTUAL_SEAT_USES_REQUIRED')
 l,b,r,t=var(x0,x1),var(y0,y1),var(x0,x1),var(y0,y1)
 row({l:1,r:-1},b=0);row({b:1,t:-1},b=0)
 for name in SEAT_USES:
  x,y,w,h=index[name]
  if w<=0 or h<=0:raise ValueError('NONPOSITIVE_SEAT_SOURCE')
  row({l:1,x:-1},b=0);row({b:1,y:-1},b=0)
  row({x:1,r:-1},b=-w);row({y:1,t:-1},b=-h)
 separation={}
 for name,(x,y,w,h)in index.items():
  if name in SEAT_USES:continue # contained uses, never an exemption from physical gates
  margin=F('.15')if name in('bath','kitchen')else F(0)
  z=[var(0,1,integer=1)for _ in range(4)];separation[name]=z;row({j:1 for j in z},a=1)
  for d,limit,j in [({r:1,x:-1},-margin,z[0]),({x:1,l:-1},-w-margin,z[1]),({t:1,y:-1},-margin,z[2]),({y:1,b:-1},-h-margin,z[3])]:row(d|{j:M},b=float(limit)+M)
 return (l,b,r,t),separation

def check_seating_geometry(rects,protected,box):
 """Exact post-quantization study check. Not a replacement for the full gate."""
 qs=[list(map(F,rects[n]))for n in SEAT_USES]
 e=[min(q[0]for q in qs),min(q[1]for q in qs),max(q[2]for q in qs),max(q[3]for q in qs)];x0,y0,x1,y1=map(F,box)
 errors=[]
 if not(x0<=e[0]<e[2]<=x1 and y0<=e[1]<e[3]<=y1):errors.append('ENVELOPE_OUTSIDE_UNIT_OR_EMPTY')
 for name,q in protected.items():
  a,b,c,d=map(F,q);margin=F('.15')if name in('bath','kitchen')else F(0)
  if not(e[2]+margin<=a or c+margin<=e[0]or e[3]+margin<=b or d+margin<=e[1]):errors.append('ENVELOPE_PROTECTED_OVERLAP:'+name)
 return {'envelope':list(map(S,e)),'errors':errors,'scope':'Research reservation only; useful living area/route quality not certified.'}


def add_shared_witness(index,envelope,var,row,M):
 # Tighten each bbox edge to at least one actual use edge; no artificial inflation.
 l,b,r,t=envelope
 for edge,axis,far in ((l,0,False),(b,1,False),(r,0,True),(t,1,True)):
  zs=[]
  for name in SEAT_USES:
   x,y,w,h=index[name];v=(x,y)[axis];off=(w,h)[axis]if far else 0
   z=var(0,1,integer=1);zs.append(z)
   row({edge:1,v:-1,z:M},b=float(off)+M)
   row({v:1,edge:-1,z:M},b=-float(off)+M)
  row({z:1 for z in zs},a=1)
 wx=var(-M,M);wy=var(-M,M)
 row({l:1,wx:-1},b=0);row({b:1,wy:-1},b=0)
 row({wx:1,r:-1},b=-BODY);row({wy:1,t:-1},b=-BODY)
 for name in SEAT_USES:
  x,y,w,h=index[name];zs=[var(0,1,integer=1)for _ in range(4)];row({z:1 for z in zs},a=1)
  for d,limit,z in [({wx:1,x:-1},-BODY,zs[0]),({x:1,wx:-1},-w,zs[1]),({wy:1,y:-1},-BODY,zs[2]),({y:1,wy:-1},-h,zs[3])]:row(d|{z:M},b=float(limit)+M)
 return wx,wy

def propose(core,time_limit=3):
 from shared_binding137 import source_check
 source_check()
 start=time.monotonic();template=private_source(core,variant=3)
 if template is None:return {'status':'UNSUPPORTED_BUNDLE_FIT','not_global_infeasibility':True}
 reservations,fit_errors=reservation_fit(core,template)
 if fit_errors:return {'status':'UNSUPPORTED_MASTER_RESERVATION_FIT','fit_errors':fit_errors,'not_global_infeasibility':True}
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);C,R=map(F,core['core_extent_x']);beds={k:list(map(F,v))for k,v in template['rectangles'].items()if k.startswith('bed')}
 left=F(template['origin'][0]);right=left+F('16.7');back=y0+F('6.9')
 specs=[('private_block',F('16.7'),F('6.9')),('bath',F('4.3'),F('3.1')),('kitchen',F('3.6'),F('4.2')),('dining',F('5.4'),F('4.4'))]+[('sofa1_use',F('1.6'),F('2.2')),('sofa2_use',F('2.2'),F('1.6'))]+[(f'chair{i}_use',F('1.5'),F('.8'))for i in range(1,5)]+[('entry_apron',F('2.65'),F('.9')),('private_trunk',F('.7'),y1-F('.4')-back)]
 # Reserve connected public body strips from actual service/source geometry.
 # No guessed fixed public strips: actual source service approaches and private
 # trunk remain mandatory packing reservations; complete physical routes are gated.

 # Connected upper public band and two side branches, derived from source extents.
 specs += [('public_upper',right-left+F('1.8'),F('.7')),('public_left',F('.7'),back-y0+F('.7')),('public_right',F('.7'),back-y0+F('.7'))]
 lower=[];upper=[];obj=[];ints=[];rows=[];lo=[];hi=[]
 def var(a,b,c=0,integer=0):
  k=len(lower);lower.append(float(a));upper.append(float(b));obj.append(c);ints.append(integer);return k
 def row(d,a=-np.inf,b=np.inf):rows.append(d);lo.append(float(a));hi.append(float(b))
 # Build source modules once; reserve their actual external operation approaches.
 from bathroom_module117 import build as bath_source
 from kitchen_module117 import build as kitchen_source
 from source_approach130 import module_approach
 approaches={'bath':module_approach(bath_source('4.3','3.1')),'kitchen':module_approach(kitchen_source('3.6','4.2'))}
 for owner,witness in approaches.items():
  l,b,r,t=map(F,witness['bbox']);specs.append((owner+'_approach',r-l,t-b))
 invalid=[name for name,w,h in specs if w<=0 or h<=0 or w>x1-x0 or h>y1-y0]
 if invalid:return {'status':'UNSUPPORTED_MASTER_RESERVATION_FIT','fit_errors':[n+':INVALID_VARIABLE_DIMENSION'for n in invalid],'not_global_infeasibility':True}
 bath_lo=max(x0,C);bath_hi=min(x1-F('4.3'),R-F('4.3'))
 if bath_lo>bath_hi:return {'status':'UNSUPPORTED_MASTER_RESERVATION_FIT','fit_errors':['bath:EMPTY_CORE_BOUND_INTERVAL'],'not_global_infeasibility':True}
 index={}
 for name,w,h in specs:index[name]=(var(x0,x1-w),var(y0,y1-h),w,h)
 def fixed(name,x,y):
  a,b,w,h=index[name]
  if w<=0 or h<=0 or not(x0<=x<=x1-w and y0<=y<=y1-h):raise ValueError('FIXED_RESERVATION_OUTSIDE_BOUNDS:'+name)
  lower[a]=upper[a]=float(x);lower[b]=upper[b]=float(y)
 for owner,witness in approaches.items():
  l,b,r,t=map(F,witness['bbox']);ax,ay,_,_=index[owner+'_approach'];ox,oy,_,_=index[owner];row({ax:1,ox:-1},l,l);row({ay:1,oy:-1},b,b)
 for name,(x,y,w,h)in reservations.items():
  if index[name][2:]!=(w,h):raise ValueError('FIXED_RESERVATION_DIMENSION_MISMATCH:'+name)
  fixed(name,x,y)
 bx,by,bw,bh=index['bath'];lower[bx]=float(bath_lo);upper[bx]=float(bath_hi)
 kx,ky,kw,kh=index['kitchen'];row({kx:1,bx:-1},-kw-F('.15'),-kw-F('.15'));row({ky:1,by:-1},bh-kh,bh-kh)
 # Fixed source-size, disjoint use envelopes. The trunk is a reserved actual
 # body corridor connecting the source private interface to entry, not a wall.
 M=float(max(x1-x0,y1-y0)*2)
 for i,(name,_,_)in enumerate(specs):
  for other,_,_ in specs[i+1:]:
   if all(n.startswith('public_')or n in('entry_apron','private_trunk')for n in(name,other)):continue
   if any(n.endswith('_approach')and o.startswith('public_')for n,o in((name,other),(other,name))):continue
   if any(n.endswith('_approach')and o in(n.removesuffix('_approach'),'entry_apron','private_trunk')for n,o in((name,other),(other,name))):continue
   if {name,other}in ({'entry_apron','private_trunk'},{'bath','kitchen'}):continue
   ax,ay,aw,ah=index[name];bx,by,bw,bh=index[other];ma=F('.15')if name in('bath','kitchen')else F(0);mb=F('.15')if other in('bath','kitchen')else F(0);clearance=ma+mb;z=[var(0,1,integer=1)for _ in range(4)];row({j:1 for j in z},a=1)
   for d,b,j in [({ax:1,bx:-1},-aw-clearance,z[0]),({bx:1,ax:-1},-bw-clearance,z[1]),({ay:1,by:-1},-ah-clearance,z[2]),({by:1,ay:-1},-bh-clearance,z[3])]:row(d|{j:M},b=float(b)+M)
 envelope_vars,envelope_separation=add_seating_envelope(index,(x0,y0,x1,y1),var,row,M)
 shared_xy=add_shared_witness(index,envelope_vars,var,row,M)
 # Fixed-source compact grammar, not six variants from translating a group.
 sx,sy,_,_=index['sofa1_use']
 offsets={'sofa2_use':('1.6','0'),'chair1_use':('0','2.3'),'chair2_use':('0','3.1'),'chair3_use':('2.7','1.6'),'chair4_use':('2.7','2.4')}
 for name,(dx,dy)in offsets.items():
  x,y,_,_=index[name];row({x:1,sx:-1},F(dx),F(dx));row({y:1,sy:-1},F(dy),F(dy))
 wx,wy=shared_xy;row({wx:1,sx:-1},F('1.6'),F('1.6'));row({wy:1,sy:-1},F('1.6'),F('1.6'))
 # Prefer public use centers near entry; not a distance regulation.
 for name,(x,y,w,h)in index.items():
  if name.startswith('public_')or name.endswith('_approach')or name in('private_block','entry_apron','private_trunk'):continue
  for axis,target in ((x,ex-w/2),(y,y1-F('.4')-h/2)):
   e=var(0,M,1);row({axis:1,e:-1},b=target);row({axis:-1,e:-1},b=-target)
 A=np.zeros((len(rows),len(lower)))
 for i,d in enumerate(rows):
  for k,v in d.items():A[i,k]=v
 res=milp(np.array(obj),integrality=np.array(ints),bounds=Bounds(lower,upper),constraints=LinearConstraint(A,lo,hi),options={'time_limit':time_limit})
 out={'status':'PROPOSAL_ONLY'if res.x is not None else'TIMEOUT_NO_WITNESS'if res.status==1 else'NO_PROPOSAL_IN_THIS_RESTRICTED_MASTER','solver_status':int(res.status),'solver_message':res.message,'variables':len(lower),'constraints':len(rows),'seconds':time.monotonic()-start,'not_global_infeasibility':True,'scope':'Restricted coarse bundle master, no full-network or operational acceptance.'}
 if res.x is None:return out
 rects={k:list(map(S,v))for k,v in beds.items()}
 for name,(x,y,w,h)in index.items():
  if name.startswith('public_')or name.endswith('_approach')or name in ('private_block','private_trunk','entry_apron'):continue
  # Quantization is explicit proposal construction; whole exact gate decides.
  a=F(str(round(float(res.x[x]),3)));b=F(str(round(float(res.x[y]),3)));rects[name]=list(map(S,[a,b,a+w,b+h]))
 protected={name:list(map(S,[x,y,x+w,y+h]))for name,(x,y,w,h)in reservations.items()}
 for name in ('bath','kitchen','dining'):protected[name]=rects[name]
 for owner,witness in approaches.items():
  ox,oy,_,_=map(F,rects[owner]);a,b,c,d=map(F,witness['bbox']);protected[owner+'_approach']=list(map(S,[ox+a,oy+b,ox+c,oy+d]))
 seating=check_seating_geometry(rects,protected,(x0,y0,x1,y1))
 if seating['errors']:
  out.update(status='QUANTIZED_SEATING_RESERVATION_REJECTED',seating_reservation=seating);return out
 out['seating_reservation']=seating
 from shared_geometry137 import overlaps,rect
 sx,sy=[F(str(round(float(res.x[k]),3)))for k in shared_xy];sw=(sx,sy,sx+BODY,sy+BODY);g=list(map(F,seating['envelope']))
 if not(g[0]<=sw[0]<sw[2]<=g[2]and g[1]<=sw[1]<sw[3]<=g[3])or any(overlaps(sw,rect(rects[n]))for n in SEAT_USES):
  out.update(status='QUANTIZED_SHARED_WITNESS_REJECTED');return out
 out['shared_body_witness']=list(map(S,sw))
 out.update(source_approach_reservations=approaches,rectangles=rects,bedrooms=3,sleep_roles=['double','twin','twin'],capacity_profile='SIX_PERSON_INTERNAL_PROGRAM121',variant=3,bed_door_sides=template['bed_door_sides'],ordered_macro=template,quantization_m='.001',generation_method='SIDECAR_COMPACT_D4_GROUP142_LOCAL_WORLD_PENDING')
 from seating_source142 import serialized_records,validate_proposal
 out['compact_d4_sources142']=serialized_records(rects['sofa1_use'][:2])
 try:validate_proposal(out)
 except (KeyError,ValueError,TypeError)as exc:
  out.update(status='QUANTIZED_COMPACT_D4_REJECTED',compact_error=str(exc))
 return out
