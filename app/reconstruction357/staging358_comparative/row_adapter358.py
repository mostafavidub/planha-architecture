"""Independent358 row-source construction/replay, no source357 schema reuse."""
import sys,json,copy,hashlib
from pathlib import Path
from fractions import Fraction as F
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'planha_general150_runtime_work';sys.path.insert(0,str(ROOT))
from contract114 import digest
from constructor129 import build,context,frame
from private_bundle129 import build as row_source
from frame_audit125 import equal

def inventory():
 files=[*ROOT.glob('*.py'),*ROOT.glob('*.json'),*(p for p in(ROOT/'references').rglob('*')if p.is_file()),Path(__file__).resolve(),Path(__file__).with_name('row_body358.py')]
 return {str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)}

def validate(raw,p):
 core,_=frame(raw,'FRONT_REAR');s=row_source(core)
 if p['generation_method']!='ROW_SOURCE_BODY_SEPARATED358_NOT_FULL_NETWORK_SOLVER'or p['bedrooms']!=3 or p['sleep_roles']!=['double','twin','twin']:raise ValueError('SOURCE_PROGRAM')
 if not equal(p['ordered_macro'],s)or p['bed_door_sides']!=s['bed_door_sides']:raise ValueError('PRIVATE_ROW_SOURCE')
 for k,v in s['rectangles'].items():
  if not equal(p['rectangles'][k],v):raise ValueError('PRIVATE_ROW_PLACEMENT')
 dims={'bath':('4.3','3.1'),'kitchen':('3.6','4.2'),'dining':('5.4','4.4')}|{f'sofa{i}_use':('2.2','1.6')for i in(1,2)}|{f'chair{i}_use':('.8','1.5')for i in range(1,5)}
 if set(p['rectangles'])!=set(dims)|set(s['rectangles']):raise ValueError('RECTANGLE_INVENTORY')
 x0,y0,x1,y1=map(F,core['units']['A'])
 for k,(w,h)in dims.items():
  a,b,c,d=map(F,p['rectangles'][k])
  if c-a!=F(w)or d-b!=F(h)or not(x0<=a<c<=x1 and y0<=b<d<=y1):raise ValueError('SOURCE_DIMENSIONS_OR_CONTAINMENT:'+k)
 seats=[k for k in dims if k.startswith('sofa')or k.startswith('chair')]
 for i,k in enumerate(seats):
  for j in seats[i+1:]:
   a,b,c,d=map(F,p['rectangles'][k]);e,f,g,h=map(F,p['rectangles'][j]);gap=F('.7')
   if not(c+gap<=e or g+gap<=a or d+gap<=f or h+gap<=b):raise ValueError('EXACT_SEAT_BODY_BRANCH')
 return core

def construct(raw,p):
 validate(raw,p);sources=inventory();pkt=build(copy.deepcopy(raw),'FRONT_REAR',copy.deepcopy(p));ctx=context(raw,p,pkt);c={'request':raw,'request_digest':digest(raw),'packet':pkt,'model':pkt['world_model'],'model_digest':digest(pkt['world_model']),'generation_context':ctx}
 if inventory()!=sources:raise ValueError('SOURCE_DRIFT')
 return {'candidate':c,'trace':{'schema':'ROW_BODY358_SOURCE_TRACE_V1','raw':raw,'proposal':p,'source_inventory':sources,'candidate_digest':digest(c),'model_digest':c['model_digest'],'accepted':False},'accepted':False}
def replay(t):
 if t['schema']!='ROW_BODY358_SOURCE_TRACE_V1'or t['source_inventory']!=inventory():raise ValueError('TRACE_BINDING')
 x=construct(t['raw'],t['proposal'])
 if digest(x['candidate'])!=t['candidate_digest']:raise ValueError('EXACT_REPLAY')
 return x
if __name__=='__main__':
 raw=json.loads((BASE/'staging357_comparative/attached_service_final357.json').read_text())['trace']['raw'];p=json.loads(Path(__file__).with_name('row_proposal358.json').read_text());x=construct(raw,p);Path(__file__).with_name('row_candidate358.json').write_text(json.dumps(x,ensure_ascii=False,indent=2));print(x['candidate']['model_digest'],len(x['candidate']['model']['route_failures']))
