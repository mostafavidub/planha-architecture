"""Only after independent pre-audit: one fixed-lineage build, no solver/fresh."""
import sys,json,hashlib,time,traceback
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent

def frozen():
 data=(HERE/'preregistration.json').read_bytes()
 expected=sys.argv[sys.argv.index('--expected-prereg-sha')+1] if '--expected-prereg-sha' in sys.argv else None
 if expected is None or hashlib.sha256(data).hexdigest()!=expected:raise ValueError('PREREG_TRUST_ANCHOR_MISMATCH')
 p=json.loads(data)
 for n,h in p['source_inventory'].items():
  if hashlib.sha256((BASE/n).read_bytes()).hexdigest()!=h:raise ValueError('FROZEN_SOURCE_CHANGED:'+n)
 return p
if __name__=='__main__':
 frozen()
 if '--worker'in sys.argv:
  try:
   from adapter364 import construct,lineage
   from contract114 import digest
   sys.path.insert(0,str(BASE/'semantic_rules357'))
   from modules_spatial import rect,union_area
   from fractions import Fraction as F
   start=time.monotonic();x=construct();m=x['candidate']['model'];old=lineage()['candidate']['model'];areas=[]
   for u in m['units']:
    prior=next(v for v in old['units']if v['id']==u['id']);a=union_area([rect(r)for rs in prior['rooms'].values()for r in rs]);b=union_area([rect(r)for rs in u['rooms'].values()for r in rs]);areas.append({'unit':u['id'],'before_net_room_union_m2':str(a),'after_net_room_union_m2':str(b),'net_geometric_floor_nondeterioration':b>=a,'functional_use_nondeterioration':'NOT_ESTABLISHED'})
   (HERE/'actual364.json').write_text(json.dumps(x,indent=2));(HERE/'diagnostic364.json').write_text(json.dumps({'model_digest':digest(m),'parent_model_digest':digest(old),'net_floor':areas,'route_failures':m['route_failures'],'new_core':x['candidate']['packet']['core'],'seconds':time.monotonic()-start,'fresh_executed':False,'solver_executed':False,'accepted':False,'delivery_allowed':False,'transferred_floor_function':'UNKNOWN','candidate_policy':'INDEPENDENT_BALANCED_PORTAL_TRADEOFF_NOT_PARETO_REPAIR','actual_route_lengths':{k:str(sum(abs(F(a[0])-F(b[0]))+abs(F(a[1])-F(b[1]))for a,b in zip(v,v[1:])))for k,v in m['common_routes'].items()},'baseline_route_lengths':{k:str(sum(abs(F(a[0])-F(b[0]))+abs(F(a[1])-F(b[1]))for a,b in zip(v,v[1:])))for k,v in old['common_routes'].items()},'portal_pose_policy':x['candidate']['packet']['core']['balanced_portals364']['source_body_pose']},indent=2));print('BUILT')
  except Exception as e:(HERE/'error364.json').write_text(json.dumps({'error':type(e).__name__+':'+str(e),'traceback':traceback.format_exc(),'accepted':False}));raise
 else:
  if any((HERE/n).exists()for n in('actual364.json','error364.json','supervision364.json')):raise SystemExit('PRESERVE_ONE_DIAGNOSTIC_ATTEMPT')
  from supervisor import supervise
  r=supervise([sys.executable,str(Path(__file__).resolve()),'--worker','--expected-prereg-sha',sys.argv[sys.argv.index('--expected-prereg-sha')+1]],110,evidence_directory=HERE);(HERE/'supervision364.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
