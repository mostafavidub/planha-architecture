"""Explicit365 proposal/source rebuild registry; never a live gate or selection."""
import json,hashlib,copy,sys
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;RUNTIME=ROOT/'planha_general150_runtime_work'
sys.path.insert(0,str(RUNTIME))
from contract114 import digest
from constructor129 import frame,build,context
from private_branch_source146 import build as private_source
from bathroom_module117 import build as bath_source
from kitchen_module117 import build as kitchen_source
from source_approach130 import module_approach
from nonseating146 import require
from service_anchor365 import choose,validate_rectangles,q
from coarse_branch365 import reservation_fit,check_seating_geometry
SCHEMA='SOURCE_SERVICE_ANCHOR365_TRACE_V1'
def inventory():
 fs=[*RUNTIME.glob('*.py'),*RUNTIME.glob('*.json'),*(p for p in(RUNTIME/'references').rglob('*')if p.is_file()),HERE/'adapter365.py',HERE/'service_anchor365.py',HERE/'coarse_branch365.py']
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(fs)}
def validate(raw,p):
 if set(raw)!={'W','L','n','requested_count'}or type(raw['n'])is not int or raw['n']!=2:raise ValueError('SOURCE_RAW_PROGRAM')
 require(p);core,_=frame(raw,'FRONT_REAR');private=private_source(core,variant=3)
 if not private or digest(p['ordered_macro'])!=digest(private):raise ValueError('PRIVATE_SOURCE_BINDING')
 if p['bedrooms']!=3 or p['sleep_roles']!=['double','twin','twin']:raise ValueError('PROGRAM')
 if p['bed_door_sides']!=private['bed_door_sides']:raise ValueError('SOURCE_DOOR_SIDES')
 for key,r in private['rectangles'].items():
  if q(p['rectangles'][key])!=q(r):raise ValueError('FIXED_PRIVATE_SOURCE_GEOMETRY')
 mods={'bath':bath_source('4.3','3.1'),'kitchen':kitchen_source('3.6','4.2')};app={k:module_approach(v)for k,v in mods.items()};box=core['units']['A'];anchor=choose(mods['bath'],mods['kitchen'],app,box,'BATH_RIGHT_KITCHEN_LEFT')
 if digest(p['service_anchor365'])!=digest(anchor):raise ValueError('ACTUAL_SOURCE_ANCHOR_CONTRACT')
 validate_rectangles(p['rectangles'],anchor)
 reservations,errors=reservation_fit(core,private)
 if errors:raise ValueError('RESERVATION_FIT')
 def expand(r):x,y,w,h=map(F,r);return(x,y,x+w,y+h)
 rects={k:expand(v)for k,v in reservations.items()}
 dims={'bath':('4.3','3.1'),'kitchen':('3.6','4.2'),'dining':('5.4','4.4')}|{f'sofa{i}_use':('2.2','1.6')for i in(1,2)}|{f'chair{i}_use':('.8','1.5')for i in range(1,5)}
 if set(p['rectangles'])!=set(private['rectangles'])|set(dims):raise ValueError('RECTANGLE_INVENTORY')
 x0,y0,x1,y1=map(F,box)
 for k,(w,h)in dims.items():
  a,b,c,d=q(p['rectangles'][k])
  if(c-a,d-b)!=(F(w),F(h))or not(x0<=a<c<=x1 and y0<=b<d<=y1):raise ValueError('ASSET_SIZE_OR_CONTAINMENT:'+k)
  rects[k]=(a,b,c,d)
 for k,v in app.items():
  a,b,_,_=rects[k];l,B,r,t=map(F,v['bbox']);rects[k+'_approach']=(a+l,b+B,a+r,b+t)
 keys=list(rects)
 for i,n in enumerate(keys):
  for o in keys[i+1:]:
   if all(k.startswith('public_')or k in('entry_apron','private_trunk')for k in(n,o)):continue
   if any(k.endswith('_approach')and v.startswith('public_')for k,v in((n,o),(o,n))):continue
   if any(k.endswith('_approach')and v in(k.removesuffix('_approach'),'entry_apron','private_trunk')for k,v in((n,o),(o,n))):continue
   gap=sum((F('.15')if k in('bath','kitchen')else F(0))for k in(n,o));a,b,c,d=rects[n];e,f,g,h=rects[o]
   if not(c+gap<=e or g+gap<=a or d+gap<=f or h+gap<=b):raise ValueError('EXACT_MASTER_OVERLAP:'+n+':'+o)
 protected={k:list(map(str,r))for k,r in rects.items()if not k.startswith(('sofa','chair'))};seat=check_seating_geometry(p['rectangles'],protected,box)
 if seat['errors']:raise ValueError('EXACT_SEATING_ENVELOPE:'+str(seat['errors']))
 return core,anchor

def construct(raw,p):
 before=inventory();core,anchor=validate(raw,p);packet=build(copy.deepcopy(raw),'FRONT_REAR',copy.deepcopy(p));ctx=context(raw,p,packet);m=packet['world_model']
 if digest(packet['core'])!=digest(core):raise ValueError('ASSEMBLED_CORE_DRIFT')
 c={'request':raw,'request_digest':digest(raw),'packet':packet,'model':m,'model_digest':digest(m),'generation_context':ctx}
 if inventory()!=before:raise ValueError('SOURCE_CHANGED_DURING_BUILD')
 return {'candidate':c,'trace':{'schema':SCHEMA,'raw':raw,'proposal':p,'source_inventory':before,'candidate_digest':digest(c),'model_digest':digest(m),'anchor_contract':anchor},'accepted':False,'delivery_allowed':False,'pending':['INDEPENDENT_REPLAY','FRESH365_REGISTRY_AND_ALL_USE','ACTUAL_Q14_PAIR','SOURCE_SELECTED_SET']}

def replay(trace):
 if trace.get('schema')!=SCHEMA or trace['source_inventory']!=inventory():raise ValueError('UNREGISTERED_SOURCE_OR_DRIFT')
 out=construct(trace['raw'],trace['proposal'])
 if digest(out['candidate'])!=trace['candidate_digest']or out['candidate']['model_digest']!=trace['model_digest']:raise ValueError('EXACT_REPLAY_MISMATCH')
 return out
