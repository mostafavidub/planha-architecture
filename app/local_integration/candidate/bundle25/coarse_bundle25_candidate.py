# TEST_ONLY local candidate; fresh checker required.
"""Small restricted master over one real three-bedroom bundle and public uses.
No internal room/operation relaxation. Whole independent checks remain mandatory.
"""
from fractions import Fraction as F
import time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from contract114 import S
from private_bundle25_candidate import build as private_source

def propose(core,time_limit=3):
 start=time.monotonic();template=private_source(core,variant=2)
 if template is None:return {'status':'UNSUPPORTED_BUNDLE_FIT','not_global_infeasibility':True}
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);C,R=map(F,core['core_extent_x']);beds={k:list(map(F,v))for k,v in template['rectangles'].items()if k.startswith('bed')}
 left=beds['bed1'][0]-F('.15');right=beds['bed3'][2]+F('.15');back=max(v[3]for v in beds.values())+F('1.3')
 specs=[('private_bundle',right-left,back-y0),('bath',F('4.3'),F('3.1')),('kitchen',F('3.6'),F('4.2')),('dining',F('5.4'),F('4.4'))]+[(f'sofa{i}_use',F('2.2'),F('1.6'))for i in(1,2)]+[(f'chair{i}_use',F('.8'),F('1.5'))for i in range(1,5)]+[('entry_apron',F('2.65'),F('.9')),('private_trunk',F('.7'),y1-F('.4')-back)]
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
 index={}
 for name,w,h in specs:index[name]=(var(x0,x1-w),var(y0,y1-h),w,h)
 def fixed(name,x,y):
  a,b,_,_=index[name];lower[a]=upper[a]=float(x);lower[b]=upper[b]=float(y)
 for owner,witness in approaches.items():
  l,b,r,t=map(F,witness['bbox']);ax,ay,_,_=index[owner+'_approach'];ox,oy,_,_=index[owner];row({ax:1,ox:-1},l,l);row({ay:1,oy:-1},b,b)
 fixed('private_bundle',left,y0);fixed('entry_apron',ex-F('.7'),y1-F('.9'));fixed('private_trunk',ex-F('.35'),back)
 bx,by,bw,bh=index['bath'];lower[bx]=float(C);upper[bx]=float(R-bw);lower[by]=upper[by]=float(y1-bh)
 kx,ky,kw,kh=index['kitchen'];row({kx:1,bx:-1},-kw-F('.15'),-kw-F('.15'));lower[ky]=upper[ky]=float(y1-kh)
 # Fixed source-size, disjoint use envelopes. The trunk is a reserved actual
 # body corridor connecting the source private interface to entry, not a wall.
 M=float(max(x1-x0,y1-y0)*2)
 for i,(name,_,_)in enumerate(specs):
  for other,_,_ in specs[i+1:]:
   if any(n.endswith('_approach')and o in(n.removesuffix('_approach'),'entry_apron','private_trunk')for n,o in((name,other),(other,name))):continue
   if {name,other}in ({'entry_apron','private_trunk'},{'bath','kitchen'}):continue
   ax,ay,aw,ah=index[name];bx,by,bw,bh=index[other];ma=F('.15')if name in('bath','kitchen')else F(0);mb=F('.15')if other in('bath','kitchen')else F(0);clearance=ma+mb;z=[var(0,1,integer=1)for _ in range(4)];row({j:1 for j in z},a=1)
   for d,b,j in [({ax:1,bx:-1},-aw-clearance,z[0]),({bx:1,ax:-1},-bw-clearance,z[1]),({ay:1,by:-1},-ah-clearance,z[2]),({by:1,ay:-1},-bh-clearance,z[3])]:row(d|{j:M},b=float(b)+M)
 # Prefer public use centers near entry; not a distance regulation.
 for name,(x,y,w,h)in index.items():
  if name.endswith('_approach')or name in('private_bundle','entry_apron','private_trunk'):continue
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
  if name.endswith('_approach')or name in ('private_bundle','private_trunk','entry_apron'):continue
  # Quantization is explicit proposal construction; whole exact gate decides.
  a=F(str(round(float(res.x[x]),3)));b=F(str(round(float(res.x[y]),3)));rects[name]=list(map(S,[a,b,a+w,b+h]))
 out.update(source_approach_reservations=approaches,rectangles=rects,bedrooms=3,sleep_roles=['double','twin','twin'],capacity_profile='SIX_PERSON_INTERNAL_PROGRAM121',variant=2,bed_door_sides=template['bed_door_sides'],ordered_macro=template,quantization_m='.001',generation_method='COARSE_BUNDLE_MILP_NOT_FULL_NETWORK_SOLVER')
 return out
