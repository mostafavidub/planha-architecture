"""Independent exact source-size packing check. Not full physical eligibility."""
from fractions import Fraction as F
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]/'planha_general150_runtime_work';sys.path.insert(0,str(ROOT))
from constructor129 import frame
from bathroom_module117 import build as bath
from kitchen_module117 import build as kitchen
from source_approach130 import module_approach
from frame_audit125 import equal

def verify(raw,p):
 errors=[];rs={}
 try:
  core,_=frame(raw,'FRONT_REAR');x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);back=y0+F('6.75');ox,oy=map(F,p['ordered_macro']['origin'])
  if oy!=y0-F('.15'):raise ValueError('SOURCE_BOUNDARY_ANCHOR')
  dims={'bath':('4.3','3.1'),'kitchen':('3.6','4.2'),'dining':('5.4','4.4')}|{f'sofa{i}_use':('2.2','1.6')for i in(1,2)}|{f'chair{i}_use':('.8','1.5')for i in range(1,5)}
  if set(p['rectangles'])!=set(dims)|{'bed1','bed2','bed3'}:raise ValueError('RECTANGLE_INVENTORY')
  for k,(w,h)in dims.items():
   q=list(map(F,p['rectangles'][k]));a,b,c,d=q
   if c-a!=F(w)or d-b!=F(h):raise ValueError('SOURCE_DIMENSIONS:'+k)
   rs[k]=q
  rs.update(private_block=[ox,y0,ox+F('16.7'),back],entry_apron=[ex-F('.7'),y1-F('.9'),ex+F('1.95'),y1],private_trunk=[ex-F('.35'),back,ex+F('.35'),y1-F('.4')],public_upper=[x0,back,x1,back+F('.7')])
  src={'bath':module_approach(bath('4.3','3.1')),'kitchen':module_approach(kitchen('3.6','4.2'))}
  if not equal(p['source_approach_reservations'],src):raise ValueError('SOURCE_APPROACH_PROFILE')
  for k,v in src.items():
   a,b,c,d=map(F,v['bbox']);x,y,_,_=rs[k];rs[k+'_approach']=[x+a,y+b,x+c,y+d]
  a,b,c,d=rs['bath'];e,f,g,h=rs['kitchen']
  if g+F('.15')!=a or h!=d:raise ValueError('ACTUAL_SERVICE_WALL_ATTACHMENT')
  for k,(a,b,c,d)in rs.items():
   if not(x0<=a<c<=x1 and y0<=b<d<=y1):raise ValueError('CONTAINMENT:'+k)
  names=list(rs)
  for i,k in enumerate(names):
   for j in names[i+1:]:
    if all(n.startswith('public_')or n in('entry_apron','private_trunk')for n in(k,j)):continue
    if any(a.endswith('_approach')and b.startswith('public_')for a,b in((k,j),(j,k))):continue
    if any(a.endswith('_approach')and b in(a.removesuffix('_approach'),'entry_apron','private_trunk')for a,b in((k,j),(j,k))):continue
    if {k,j}=={'bath','kitchen'}:continue # source-specific .15 adjacency checked above
    a,b,c,d=rs[k];e,f,g,h=rs[j];gap=F('.15')*int(k in('bath','kitchen'))+F('.15')*int(j in('bath','kitchen'))
    if not(c+gap<=e or g+gap<=a or d+gap<=f or h+gap<=b):raise ValueError('EXACT_PACKING_OVERLAP:'+k+':'+j)
 except(KeyError,ValueError,TypeError,IndexError)as e:errors.append(str(e))
 return {'status':'FAIL_PACKING'if errors else'PASS_SOURCE_PACKING_ONLY','errors':errors,'regions':{k:list(map(str,v))for k,v in rs.items()},'accepted':False,'scope':'EXACT_SOURCE_ASSET_PACKING_AND_CONNECTOR_RESERVATIONS_NOT_PHYSICAL_FUNCTIONS'}
