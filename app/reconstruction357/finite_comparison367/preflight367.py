"""Read-only actual geometry/objective diagnostic. No raw/gate/admission reuse."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'finite_comparison365'),str(ROOT/'semantic_rules357')]
from q04_closure365_v7 import objective,compare,digest
from service_candidate_criterion365 import measure,classify,domain_partition,transformed_rect,rect

def run():
 p=ROOT/'review367_joint_attempt2/actual367.json';r=json.loads(p.read_text());m=r['candidate']['model'];assert digest(m)==r['candidate']['model_digest'];v,bindings=objective(m);comparisons=[]
 for name,path in [('balanced365','staging365_balanced_portals/actual365.json'),('service365','staging365_service_grammar/candidate365.json'),('notch362','staging362_core_notch/actual362.json')]:
  z=ROOT/path;b=json.loads(z.read_text());same={k:b['candidate']['model'][k]==m[k]for k in ('program','profile')};same['request']=b['candidate']['request']==r['candidate']['request']
  comparisons.append({'id':name,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'same':same,'diagnostic':compare(m,b['candidate']['model'])})
 service=[]
 for a,c in zip(measure(m),classify(m,measure(m))):
  u=next(u for u in m['units']if u['id']==a['unit']);p=next(p for p in m['module_placements']if p['unit_id']==u['id']and p['room_id']=='bath');approach=[transformed_rect(q,p['transform'])for q in p['module']['unit']['rooms']['public_access']];o=next(o for o in m['openings']if o['id']==u['id']+'.bath')
  service.append({'unit':u['id'],'measurement':a,'classification_diagnostic':c,'partition_diagnostic':domain_partition(m,u,a['service_target_ids'],approach,rect(o['rect']))})
 return {'schema':'367_GEOMETRY_ONLY_PREFLIGHT','model_digest':digest(m),'record_digest':digest(r),'objectives':{k:str(x)for k,x in v.items()},'common_bindings':bindings,'comparisons':comparisons,'service_diagnostics':service,'accepted':False,'fresh_gate_used':False,'role_or_compactness_verdict':'NOT_ASSESSED','note':'Declared geometry only; source replay/fresh/intrinsic callbacks are not replaced by these measurements.'}
if __name__=='__main__':
 x=run();p=Path(__file__).with_name('preflight_actual367.json');assert not p.exists();p.write_text(json.dumps(x,indent=2));print(x['model_digest']);print([(u['unit'],u['partition_diagnostic']['exclusive_after_source_clearance_m2'])for u in x['service_diagnostics']])
