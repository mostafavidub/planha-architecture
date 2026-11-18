"""Only after independent pre-audit: one fixed-lineage build, no solver/fresh."""
import sys,json,hashlib,time,traceback
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent

def frozen():
 p=json.loads((HERE/'preregistration.json').read_text())
 for n,h in p['source_inventory'].items():
  if hashlib.sha256((BASE/n).read_bytes()).hexdigest()!=h:raise ValueError('FROZEN_SOURCE_CHANGED:'+n)
 return p
if __name__=='__main__':
 frozen()
 if '--worker'in sys.argv:
  try:
   from adapter360 import construct,lineage
   from contract114 import digest
   sys.path.insert(0,str(BASE/'semantic_rules357'))
   from modules_spatial import rect,union_area
   start=time.monotonic();x=construct();m=x['candidate']['model'];old=lineage()['candidate']['model'];areas=[]
   for u in m['units']:
    prior=next(v for v in old['units']if v['id']==u['id']);a=union_area([rect(r)for rs in prior['rooms'].values()for r in rs]);b=union_area([rect(r)for rs in u['rooms'].values()for r in rs]);areas.append({'unit':u['id'],'before_net_room_union_m2':str(a),'after_net_room_union_m2':str(b),'net_geometric_floor_nondeterioration':b>=a,'functional_use_nondeterioration':'NOT_ESTABLISHED'})
   (HERE/'actual360.json').write_text(json.dumps(x,indent=2));(HERE/'diagnostic360.json').write_text(json.dumps({'model_digest':digest(m),'parent_model_digest':digest(old),'net_floor':areas,'route_failures':m['route_failures'],'new_core':x['candidate']['packet']['core'],'seconds':time.monotonic()-start,'fresh_executed':False,'solver_executed':False,'accepted':False,'delivery_allowed':False,'transferred_floor_function':'UNKNOWN'},indent=2));print('BUILT')
  except Exception as e:(HERE/'error360.json').write_text(json.dumps({'error':type(e).__name__+':'+str(e),'traceback':traceback.format_exc(),'accepted':False}));raise
 else:
  if any((HERE/n).exists()for n in('actual360.json','error360.json','supervision360.json')):raise SystemExit('PRESERVE_ONE_DIAGNOSTIC_ATTEMPT')
  from supervisor import supervise
  r=supervise([sys.executable,str(Path(__file__).resolve()),'--worker'],110,evidence_directory=HERE);(HERE/'supervision360.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
