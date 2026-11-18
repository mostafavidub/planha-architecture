"""Reconstructed357 one-attempt source compound repair, not353/355 byte recovery."""
import json,sys,copy,time
from pathlib import Path
from fractions import Fraction as F
from modules_spatial import rect,intersection,union_area,source_sweeps,digest
ROOT=Path(__file__).resolve().parents[1]

def diagnose(model):
 body=F(model['profile']['body_m']);out=[]
 for u in model['units']:
  for fid,raw in u['fixtures'].items():
   aid=fid+'_front'
   if not fid.startswith(('sofa','armchair'))or aid not in u['activities']:continue
   fx,ac=rect(raw),rect(u['activities'][aid]);axes=[]
   for axis in(0,1):
    if ac[axis]>=fx[axis+2]:axes.append((axis,1))
    elif ac[axis+2]<=fx[axis]:axes.append((axis,-1))
   if len(axes)!=1:continue
   axis,front=axes[0];other=1-axis;back=fx[axis]if front==1 else fx[axis+2];possible=[]
   for wid,wraw in model['walls'].items():
    w=rect(wraw)
    if not(w[other]<=fx[other]and w[other+2]>=fx[other+2]):continue
    face=w[axis+2]if front==1 else w[axis];gap=(back-face)*front
    if not 0<gap<body:continue
    strip=list(fx);strip[axis]=min(back,face);strip[axis+2]=max(back,face)
    uses=[rect(r)for k,r in u['fixtures'].items()if k!=fid]+[rect(r)for r in u['activities'].values()]
    for mapping in(u['routes'],u['scenario_routes']):
     for path in mapping.values():uses+=source_sweeps(path,body)
    for op in model.get('operations',{}).get('doors',[]):
     if not any(s.get('unit')==u['id']for s in op.get('states',[])):continue
     for k in('closed_panel','open_panel','rail_envelope'):
      if k in op:uses.append(rect(op[k]))
     uses += [rect(s['actor_rect'])for s in op.get('states',[])if s.get('unit')==u['id']]
     for s in op.get('continuous_actor_segments',[]):
      if s.get('unit')!=u['id']:continue
      a,b=rect(s['actor_start']),rect(s['actor_end'])
      if a[0]==b[0]or a[1]==b[1]:uses.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
    for o in model.get('openings',[]):
     if any(k.startswith(u['id']+'.')for k in o.get('connects',[])):uses.append(rect(o['rect']))
    collisions=[x for r in uses if(x:=intersection(tuple(strip),r))]
    possible.append({'unit':u['id'],'fixture_id':fid,'activity_id':aid,'axis':axis,'front_sign':front,'wall_id':wid,'wall_geometry':wraw,'fixture_geometry':raw,'activity_geometry':u['activities'][aid],'gap_m':str(gap),'body_m':str(body),'strip_geometry':list(map(str,strip)),'strip_area_m2':str(union_area([tuple(strip)])),'declared_use_intersection_m2':str(union_area(collisions)),'translation_world':[str(-front*gap if i==axis else F(0))for i in(0,1)],'verdict':'UNRESOLVED_SHORT_BACK_STRIP_REPAIR_CANDIDATE'if not collisions else'INELIGIBLE_DECLARED_USE_IN_GAP'})
   if possible:out.append(min(possible,key=lambda r:F(r['gap_m'])))
 return out

def propose(envelope,case):
 if envelope['packet']['family']!='FRONT_REAR'or case['unit']!='A':raise ValueError('UNSUPPORTED_SOURCE_FRAME')
 if case['verdict']!='UNRESOLVED_SHORT_BACK_STRIP_REPAIR_CANDIDATE':raise ValueError('GAP_HAS_USE')
 p=copy.deepcopy(envelope['generation_context']['construction_trace']['proposal']);fid=case['fixture_id'];key=(fid if fid.startswith('sofa')else'chair'+fid[len('armchair'):])+'_use'
 q=rect(p['rectangles'][key]);f,a=rect(case['fixture_geometry']),rect(case['activity_geometry']);whole=min(f[0],a[0]),min(f[1],a[1]),max(f[2],a[2]),max(f[3],a[3])
 if q!=whole:raise ValueError('SOURCE_COMPOUND_NOT_BOUND')
 dx,dy=map(F,case['translation_world']);p['rectangles'][key]=list(map(str,[q[0]+dx,q[1]+dy,q[2]+dx,q[3]+dy]))
 for k in('solver_status','solver_message','seconds','variables','constraints'):p.pop(k,None)
 p.update(status='ENGINEERING_REPAIR_PROPOSAL_NOT_SOLVER_OUTPUT',generation_method='SOURCE_SEATING_BACK_STRIP_REPAIR357',scope='One exact source fixture+front-activity translation, no admission before fresh review.')
 p['repair357']={'baseline_model_hash':digest(envelope['packet']['world_model']),'operator':'SOURCE_SEATING_BACK_STRIP_FLUSH','diagnostic':case,'source_compound_key':key,'solver_claim':False,'assumption':'Back clearance not required by this source compound; source reconstruction and independent functional review required.'}
 return p

def run(envelope):
 before=digest(envelope);cases=diagnose(envelope['packet']['world_model']);eligible=[c for c in cases if c['unit']=='A'and c['verdict'].endswith('REPAIR_CANDIDATE')]
 if not eligible:return {'status':'NO_SUPPORTED_CANDIDATE','diagnostics':cases,'admission_allowed':False}
 chosen=sorted(eligible,key=lambda c:(-F(c['strip_area_m2']),c['fixture_id']))[0];proposal=propose(envelope,chosen)
 sys.path.insert(0,str(ROOT/'planha_general150_runtime_work'))
 from constructor129 import build,context
 start=time.monotonic();packet=build(envelope['raw'],envelope['packet']['family'],proposal);ctx=context(envelope['raw'],proposal,packet)
 if digest(envelope)!=before:raise ValueError('BASELINE_MUTATED')
 return {'schema':'SOURCE_REPAIR357_RECONSTRUCTED','status':'BUILT_PENDING_FULL_FRESH_REVIEW','baseline_model_hash':digest(envelope['packet']['world_model']),'diagnostics':cases,'chosen':chosen,'proposal':proposal,'packet':packet,'generation_context':ctx,'model_hash':digest(packet['world_model']),'post_diagnostics':diagnose(packet['world_model']),'admission_allowed':False,'attempt_count':1,'constructor_seconds':time.monotonic()-start}
if __name__=='__main__':
 r=json.loads((ROOT/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0];o=run(r['central_envelope']);Path(__file__).with_name('source_repair_actual357.json').write_text(json.dumps(o,indent=2));print(json.dumps({k:v for k,v in o.items()if k in('status','model_hash','chosen','constructor_seconds')}))
