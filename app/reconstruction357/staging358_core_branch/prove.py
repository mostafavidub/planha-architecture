"""Fresh source primitive measurement, not historical354 or a generated plan."""
from pathlib import Path
import sys,json,hashlib
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'planha_general150_runtime_work';sys.path.insert(0,str(ROOT));sys.path.insert(0,str(BASE/'semantic_rules357'))
from contract114 import full_band_core_first,core_first,parse,digest
from modules_spatial import rect,union_area,intersection,difference,source_sweeps
from intrinsic_access358 import evaluate as access

def run():
 names=['contract114.py','constructor129.py','coarse_master129.py','core_wall_audit118.py'];before={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in names}
 readpaths=[Path(__file__).resolve(),BASE/'semantic_rules357/modules_spatial.py',BASE/'semantic_rules357/intrinsic_access358.py',BASE/'semantic_rules357/method_registry_source358.json',BASE/'staging358_comparative/row_candidate358.json',BASE/'review358_source_validation/result.json'];readset={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in readpaths}
 record=json.loads((BASE/'staging358_comparative/row_candidate358.json').read_text());fresh=json.loads((BASE/'review358_source_validation/result.json').read_text());c=record['candidate'];raw=c['request'];m=c['model'];W,L,n=parse(raw);full=full_band_core_first(W,L);compact=core_first(W,L)
 if digest(compact)!=digest(c['packet']['core']):raise ValueError('ACTUAL_COMPACT_CORE_BINDING')
 rows=[]
 for u in m['units']:
  uid=u['id'];a=list(map(rect,u['ownership']));b=list(map(rect,full.get('unit_ownership',{}).get(uid,[full['units'][uid]])))
  expected=list(map(rect,compact['unit_ownership'][uid]))
  if difference(a,expected)or difference(expected,a):raise ValueError('ACTUAL_OWNERSHIP_BINDING')
  before_area=union_area(a);after_area=union_area(b)
  rows.append({'unit':uid,'before_regions':u['ownership'],'after_regions':list(map(lambda r:list(map(str,r)),b)),'before_exact_m2':str(before_area),'after_exact_m2':str(after_area),'delta_exact_m2':str(after_area-before_area),'nondeterioration':after_area>=before_area})
 intr=access(m,fresh['raw_report']);lobby=list(map(rect,m['common_spaces']['lobby']));body=m['profile']['body_m'];routes=[s for p in m['common_routes'].values()for s in source_sweeps(p,body)];routeparts=[i for s in routes for r in lobby if(i:=intersection(s,r))]
 actors=[]
 for op in m['operations']['doors']:
  if op['opening_id']not in('A.entry','B.entry'):continue
  for state in op['states']:
   if state.get('role_id')!='lobby':continue
   q=rect(state['actor_rect']);actors.extend(i for r in lobby if(i:=intersection(q,r)))
 covered=routeparts+actors;residual=difference(lobby,covered)
 after={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()for name in names}
 if before!=after or any(hashlib.sha256((BASE/n).read_bytes()).hexdigest()!=h for n,h in readset.items()):raise ValueError('SOURCE_OR_READSET_CHANGED')
 return {'schema':'ACTUAL_SOURCE_FULL_BAND_BRANCH358','raw':raw,'raw_digest':digest(raw),'current_model_digest':digest(m),'current_core_digest':digest(compact),'full_band_core_digest':digest(full),'compact_core':compact,'full_band_core':full,'ownership_rows':rows,'branch_disposition':'PROTECTED_AREA_NONDETERIORATION_COUNTEREXAMPLE'if any(not r['nondeterioration']for r in rows)else'UNRESOLVED','restriction_authority':'EXPLICIT_SAME_PROGRAM_PROTECTED_AREA_COMPARATIVE_BRANCH_NOT_GENERAL_ARCHITECTURAL_INVALIDITY','solver_executed':False,'fresh_executed':False,'full_plan_constructed':False,'not_global_infeasibility':True,'adapter_status':{'full_band_has_core_extent_x':'core_extent_x'in full,'coarse129_requires_core_extent_x':True,'constructor129_FRONT_REAR_uses_compact':True,'full_band_solver_supported_without_new_adapter':False},'current_lobby_role':{'arrival_intrinsic':intr,'lobby_area_m2':str(union_area(lobby)),'actual_arrival_swept_union_m2':str(union_area(routeparts)),'entry_actor_staging_overlap_m2':str(union_area(actors)),'union_arrival_and_bound_entry_actor_m2':str(union_area(covered)),'unassigned_by_these_witnesses_m2':str(union_area(residual)),'residual_regions':[list(map(str,r))for r in residual],'whole_lobby_minimality_proven':False,'scope':'ACTUAL_SOURCE_ARRIVAL_AND_DECLARED_ENTRY_ACTOR_POSES_ONLY; NO_INVENTED_STAGING_OR_TECHNICAL_CORE_CERTIFICATION'},'readset':readset,'source_before':before,'source_after':after,'source_unchanged':True,'accepted':False,'delivery_allowed':False}
if __name__=='__main__':
 out=run();Path(__file__).with_name('actual_full_band358.json').write_text(json.dumps(out,indent=2));print(out['branch_disposition'],out['ownership_rows']);print('lobby', {k:v for k,v in out['current_lobby_role'].items()if k.endswith('_m2')})
