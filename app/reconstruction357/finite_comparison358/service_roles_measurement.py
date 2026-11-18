"""Observed service-only path envelopes, not semantic exclusive floor."""
from build_ledger import *
from modules_spatial import source_sweeps,difference,union_area,rect
from fractions import Fraction as F

def measure(m):
 out=[]
 for u in m['units']:
  placements=[p for p in m['module_placements']if p['unit_id']==u['id']and p['room_id']=='bath'];assert len(placements)==1;p=placements[0];assert digest(p['module'])==p['module_hash']
  ids=set(p['module']['unit']['activities']);targets=sorted(ids & set(u['routes']));assert targets
  service=[q for k in targets for q in source_sweeps(u['routes'][k],F(m['profile']['body_m']))]
  other=[q for k,path in u['routes'].items()if k not in targets for q in source_sweeps(path,F(m['profile']['body_m']))]
  other += [q for path in u['scenario_routes'].values()if isinstance(path,list) and path and isinstance(path[0],list)for q in source_sweeps(path,F(m['profile']['body_m']))]
  bath=[rect(r)for r in u['rooms']['bath']];outside=difference(service,bath);sole=difference(outside,other)
  out.append({'unit':u['id'],'module_hash':p['module_hash'],'service_target_ids':targets,'bath_union_m2':str(union_area(bath)),'service_body_union_outside_bath_m2':str(union_area(outside)),'observed_service_only_sweep_m2':str(union_area(sole)),'observed_service_only_regions':[list(map(str,r))for r in sole],'public_access_binding':m['logical_regions'][u['id']+'.public_access'],'source_approach_regions':m['module_aprons'][u['id']+'.bath'],'semantic_exclusive_service_area':'UNKNOWN_NOT_EQUAL_TO_OBSERVED_ROUTE_ONLY_AREA','reason':'finite route occupancy does not establish exclusive floor purpose; public access is shared source role and module apron is operation clearance, not a new dedicated corridor'})
 return out
if __name__=='__main__':
 x=json.loads((ROOT/'actual_run/actual_response.json').read_text());models={'baseline351':x['selected'][0]['model']}
 for name,path in [('translated357','staging357_comparative/attached_service_final357.json'),('row358','staging358_comparative/row_candidate358.json'),('clamped359','staging359_hall_clamp/actual359.json')]:models[name]=json.loads((ROOT/path).read_text())['candidate']['model']
 result={'schema':'SERVICE_ROLE_SOURCE_GEOMETRY_MEASUREMENT_NOT_ACCEPTANCE','parent_acceptance':False,'source_files':{f:hashlib.sha256((ROOT/'planha_general150_runtime_work'/f).read_bytes()).hexdigest()for f in ['place_bathroom117.py','bathroom_module117.py']},'models':{k:{'model_digest':digest(m),'rows':measure(m),'fresh359_required':k=='clamped359'}for k,m in models.items()}}
 Path(__file__).with_name('service_roles_actual359.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print([(k,[(r['unit'],r['observed_service_only_sweep_m2'])for r in v['rows']])for k,v in result['models'].items()])
