"""Task3.5 exact source-wall removal accounting. Never a constructed model."""
import copy,sys,inspect
from fractions import Fraction as F
from pathlib import Path
from front_rear_runtime_adapter import ROOT,ENGINE,ensure,transport,source_audit
from same_version_front_rear_contract import digest
from source_wall_counterfactual import bound_source,exact_closure_change
from current_programme_evaluator import placed
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def assess(bundle):
 bundle,_=transport(bundle);pin=digest(bundle);m=bundle['packet']['world_model'];mh=digest(m)
 ensure(mh==bundle['model_digest'],'MODEL_DIGEST')
 ensure(m['physical_wall_network']['source_wall_hash']==digest(m['walls']),'WALL_NETWORK_BINDING')
 ensure(bundle['reports']['physical']['model_hash']==mh,'PHYSICAL_MODEL_BINDING')
 for k,r in bundle['reports'].items():ensure(digest(r)==bundle['report_digests'][k],'REPORT_DIGEST')
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration')]
 from producer_provenance import snapshot,require_unchanged
 snap=snapshot(ROOT,['app/local_integration/source_wall_function_evaluator.py','app/local_integration/source_wall_counterfactual.py','app/local_integration/current_programme_evaluator.py'])
 audit=source_audit()
 import construction_replay127
 from geometry114 import cells
 from privacy115 import rect,boundary,crosses,separator
 ensure(Path(inspect.getsourcefile(cells)).resolve()==(ENGINE/'fast_cells120.py').resolve(),'CELLS_SOURCE')
 replay=construction_replay127.verify(m,bundle['context']);ensure(replay['verified'] is True and replay['model_hash']==mh,'REPLAY')
 ensure(digest(bundle)==pin,'REPLAY_MUTATION')
 out={'schema':'SOURCE_WALL_FUNCTION_EVIDENCE_V1','criterion':'NONFUNCTIONAL_WALL_EXCLUSION','state':'UNKNOWN','model_digest':mh,
 'original_physical_digest':bundle['report_digests']['physical'],'original_physical_report':copy.deepcopy(bundle['reports']['physical']),
 'replay':replay,'walls':[],'scope':'Detached source-removal material and fixed-region boundary/limited separator consequences only; not a model, necessity proof, alternative placement, or deletion authorization.',
 'remaining':['Alternative placement/shorter organisation per wall not proven','Useful-area benefit and full furnishing/use consequences not proven','Fresh rerouted access and full privacy scenarios not evaluated by this probe','Core/shell non-module walls inventoried only, no removal authorization'],**{k:False for k in AUTH}}
 try:
  regions=[];source_ids=[]
  for p in m['module_placements']:
   ensure(digest(p['module'])==p['module_hash'],'MODULE_HASH')
   module=p['module'];source_ids += [p['id_map'][k] for k in module['walls']]
   u=next(u for u in m['units'] if u['id']==p['unit_id'])
   role=p['room_id'];local_role='bed1' if role.startswith('bed') else role
   ensure(local_role in module['unit']['rooms'],'SOURCE_ROOM_ROLE')
   local=module['unit']['rooms'][local_role];world=[list(map(str,placed(q,p['transform']))) for q in local]
   actual=u['rooms'][role]
   ensure(not cells(world,actual) and not cells(actual,world),'SOURCE_ROOM_FLOOR_BINDING')
   qualified=u['id']+'.'+role
   edges=boundary(list(map(rect,actual)))
   aps=[o for o in m['openings'] if qualified in o.get('connects',[]) and any(crosses(rect(o['rect']),e) for e in edges)]
   targets=[]
   if role.startswith('bed'):
    for key,q in module['unit']['fixtures'].items():
     if module['unit']['fixture_metadata'].get(key,{}).get('kind')=='bed':
      wid=p['id_map'][key];ensure(list(rect(u['fixtures'][wid]))==placed(q,p['transform']),'BED_TARGET_BINDING')
      targets.append({'id':wid,'rect':u['fixtures'][wid]})
   regions.append({'role':qualified,'floor':actual,'apertures':aps,'targets':targets,'module_hash':p['module_hash']})
  ensure(len(source_ids)==len(set(source_ids)),'CROSS_MODULE_WALL_ALIAS')
  before=list(m['walls'].values());oldunion=list(map(rect,cells(before,[])))
  fixed=[(u['id'],name,path) for u in m['units'] for name,path in u.get('routes',{}).items() if path]
  from kitchen_guest_review import sweeps
  from privacy115 import hit
  for sid,q in sorted(m['walls'].items()):
   row={'source_id':sid,'source_rect':q,'physical_aliases':m['physical_wall_network']['source_aliases'].get(sid,[]),'state':'UNKNOWN'}
   if sid not in source_ids:
    row.update(scope='NON_MODULE_SOURCE_INVENTORY_ONLY',removal_executed=False,function='NOT_INDEPENDENTLY_BOUND',core_deletion_authorized=False)
    out['walls'].append(row);continue
   row['source_binding']=bound_source(m,sid)
   after=[r for k,r in m['walls'].items() if k!=sid];removed=cells(before,after);newunion=list(map(rect,cells(after,[])))
   row.update(scope='DETACHED_MATERIAL_REMOVAL_PROBE',removal_executed=True,removed_material_cells=removed,
    free_geometric_gain_m2=str(sum((F(r[2])-F(r[0]))*(F(r[3])-F(r[1])) for r in removed)),
    useful_area_gain_m2=None,material_union_unchanged=not removed,served_source_space=row['source_binding']['unit_id']+'.'+row['source_binding']['room_id'])
   effects=[]
   for region in regions:
    intervals=exact_closure_change(list(map(rect,region['floor'])),oldunion,newunion,[rect(o['rect']) for o in region['apertures']])
    changed=[e for e in intervals if e['newly_missing']]
    if changed:effects.append({'region':region['role'],'source_module_hash':region['module_hash'],'newly_uncovered_length_m':str(sum(F(e['newly_uncovered_length_m']) for e in changed)),'changed_boundary_intervals':changed})
   row['fixed_region_boundary_dependencies']=effects
   row['boundary_scope']='Loss of existing boundary coverage on unchanged source room floor, not proof that the room must be fully closed or wall placement is optimal'
   visibility=[]
   for region in regions:
    for ap in region['apertures']:
     for t in region['targets']:
      b=any(separator(rect(ap['rect']),rect(t['rect']),w) for w in oldunion)
      a=any(separator(rect(ap['rect']),rect(t['rect']),w) for w in newunion)
      if b!=a:visibility.append({'region':region['role'],'opening':ap['id'],'target_fixture':t['id'],'before_sufficient_single_wall_separator':b,'after_sufficient_single_wall_separator':a,'visibility_proven':False})
   row['bed_aperture_separator_changes']=visibility
   row['privacy_scope']='Only strict single-wall sufficient certificates to source beds; absence is UNKNOWN, not a visible-ray proof; all other targets/scenarios not evaluated'
   route_effects=[]
   for uid,name,path in fixed:
    bands=sweeps(path,F(m['profile']['body_m']))
    b=any(hit(r,w) for r in bands for w in oldunion);a=any(hit(r,w) for r in bands for w in newunion)
    if b!=a:route_effects.append({'unit':uid,'route':name,'before_wall_collision':b,'after_wall_collision':a})
   row['fixed_existing_route_wall_collision_changes']=route_effects
   row['route_scope']='Existing paths against wall material only; not fresh paths, complete obstacle validity, length improvement, or missing historical guest route repair'
   row['furnishing_effect']='Fixture/activity geometry and programme fixed; use/placement consequences NOT_EVALUATED'
   out['walls'].append(row)
  ensure(len(out['walls'])==len(m['walls']),'WALL_COVERAGE')
  out['counts']={'all_source_walls':len(m['walls']),'module_bound_removal_probes':len(source_ids),'non_module_inventory_only':len(m['walls'])-len(source_ids),
    'zero_unique_material_probes':sum(r.get('material_union_unchanged') is True for r in out['walls']),
    'boundary_dependency_probes':sum(bool(r.get('fixed_region_boundary_dependencies')) for r in out['walls'])}
 except Exception as ex:out['missing']=[type(ex).__name__+':'+str(ex)]
 finally:
  try:
   ensure(digest(bundle)==pin,'INPUT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SOURCE_CHANGED');out['integrity_verified']=True
  except Exception as ex:out.update(integrity_verified=False,integrity_error=type(ex).__name__+':'+str(ex))
  out['source_snapshot']=snap
 return out
