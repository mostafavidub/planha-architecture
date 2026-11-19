"""One retained A.entry_dining witness: exact contacts and fixed-path clearance only."""
import copy,sys,inspect
from fractions import Fraction as F
from pathlib import Path
from front_rear_runtime_adapter import ROOT,ENGINE,ensure,transport,source_audit
from same_version_front_rear_contract import digest
from kitchen_guest_review import rect,sweeps
from source_guest_route_evaluator import living_destination,route_check,center
from ordered_guest_group_diagnostic import first_positive_body_contact
from fixed_route_clearance_diagnostic import fixed_polyline_capacity
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def contact_order(living,dining):
 return None if living is None or dining is None else F(living)<F(dining)
def assess(bundle,manifest):
 bundle,_=transport(bundle);pin=digest(bundle);mpin=digest(manifest);m=bundle['packet']['world_model'];mh=digest(m)
 ensure(mh==bundle['model_digest']==manifest['model_digest'],'MODEL_BINDING')
 ensure(bundle['reports']['physical']['model_hash']==mh,'PHYSICAL_MODEL')
 ensure(digest(bundle['reports']['physical'])==manifest['original_physical_digest']==bundle['report_digests']['physical'],'PHYSICAL_DIGEST')
 u=next(u for u in m['units'] if u['id']=='A')
 stored=next(u for u in manifest['units'] if u['unit']=='A')
 r=copy.deepcopy(next(r for r in stored['routes'] if r['id']=='entry_dining'))
 ensure(r['state']=='PASS_SOURCE_PROFILE_ROUTE_ONLY' and r['path'],'RETAINED_WITNESS')
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration')]
 from producer_provenance import snapshot,require_unchanged
 paths=['app/local_integration/'+p for p in ('guest_contact_clearance_extension.py','source_guest_route_evaluator.py','ordered_guest_group_diagnostic.py','fixed_route_clearance_diagnostic.py','kitchen_guest_review.py','current_programme_evaluator.py','guest_four_route_diagnostic.py','review_cycle.py')]
 snap=snapshot(ROOT,paths);audit=source_audit()
 from geometry114 import cells
 from public_program_audit118 import bind_operation_destination
 import construction_replay127
 for fn,path in ((cells,ENGINE/'fast_cells120.py'),(bind_operation_destination,ENGINE/'public_program_audit118.py'),(construction_replay127.verify,ENGINE/'construction_replay127.py'),
                 (first_positive_body_contact,ROOT/paths[2]),(fixed_polyline_capacity,ROOT/paths[3]),(route_check,ROOT/paths[1])):
  ensure(Path(inspect.getsourcefile(fn)).resolve()==path,'CALLABLE_SOURCE')
 out={'schema':'SINGLE_GUEST_CONTACT_CLEARANCE_V1','criterion':'KITCHEN_GUEST_PATH_SEPARATION','state':'UNKNOWN','unit':'A','route_id':'entry_dining','model_digest':mh,
  'original_physical_report':copy.deepcopy(bundle['reports']['physical']),'original_physical_digest':manifest['original_physical_digest'],
  'retained_route':r,'retained_manifest_digest':mpin,
  'scope':'One retained historicalV1-model route, not currentV2 generation, principal circulation, natural layout or ergonomic approval.',**{k:False for k in AUTH}}
 try:
  rep=construction_replay127.verify(m,bundle['context']);out['replay']=rep
  ensure(rep['verified'] is True and rep['model_hash']==mh,'REPLAY')
  body=F(m['profile']['body_m']);ensure(body==F(r['body_m'])==F('.7'),'BODY_PROFILE')
  living,lb=living_destination(u);d=u['public_program']['destinations']['guest_dining'];end=center(u['activities'][d['activity_id']])
  out['dining_binding']=bind_operation_destination(u,d,tuple(map(F,end)))
  ensure(list(map(F,r['start']))==list(map(F,u['entry_point'])) and list(map(F,r['end']))==list(map(F,end)),'ENDPOINT_BINDING')
  ko=next(o for o in m['operations']['kitchen'] if o['unit']=='A')
  ensure(digest(ko)==stored['kitchen_operation_digest'],'KITCHEN_OPERATION_BINDING')
  zones=[u['activities']['kitchen_work']]+ko['motion_envelopes']+[z['actor_rect'] for z in ko['workstations']]
  walls=list(m['walls'].values())+[z['open_panel'] for z in m['operations']['doors']]
  chairs=[]
  for z in m['operations']['dining_chairs']:
   if z['unit']!='A':continue
   a,b=rect(z['closed_rect']),rect(z['open_rect'])
   chairs += [list(map(str,[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])])),z['occupied_body']]
  roles=['living','entry_circulation','dining','kitchen'];ensure(r['floor_roles']==roles,'FLOOR_ROLES')
  parts=[q for role in roles for q in u['rooms'].get(role,[])]
  for p in m['module_placements']:
   if p['unit_id']=='A' and p['room_id'] in ('kitchen','bath'):parts+=m['module_aprons']['A.'+p['room_id']]
  parts=cells(parts,[]);owner=u['ownership'];allq=list(map(rect,owner))
  box=list(map(str,[min(q[0] for q in allq),min(q[1] for q in allq),max(q[2] for q in allq),max(q[3] for q in allq)]))
  private=[q for k,qs in u['rooms'].items() if k.startswith('bed') or k=='private_circulation' for q in qs]
  fx=[q for k,q in u['fixtures'].items() if not u['fixture_metadata'][k].get('walkable')]
  obstacles=walls+fx+chairs+private+zones+[s['occupied_body'] for s in u['public_program']['capacity']['living_seats']]+cells([box],parts)+cells([box],owner)
  ensure(digest(parts)==r['floor_digest'] and digest(owner)==r['ownership_digest'] and digest(box)==digest(r['domain_box']),'DOMAIN_BINDING')
  ensure(digest(obstacles)==r['obstacle_digest'] and len(obstacles)==r['obstacle_count'],'OBSTACLE_BINDING')
  route_check(r['path'],r['start'],r['end'],body,parts,obstacles)
  cap=fixed_polyline_capacity(r['path'],box,obstacles);w=F(cap['maximum_uniform_axis_aligned_square_width_m'])
  ensure(w>=body,'CLEARANCE_CONTRADICTS_WITNESS')
  route_check(r['path'],r['start'],r['end'],w,parts,obstacles)
  try:route_check(r['path'],r['start'],r['end'],w+F(1,1000000),parts,obstacles)
  except ValueError as ex:ensure(str(ex) in ('ROUTE_DOMAIN_COVERAGE','ROUTE_OBSTACLE_COLLISION'),'UNRELATED_SWEEP_ERROR');cause=str(ex)
  else:raise ValueError('CAPACITY_EPSILON_NOT_REJECTED')
  cap['independent_sweep_certificate']={'at_capacity_clear':True,'above_capacity_rejection':cause,'test_epsilon_m':'1/1000000','epsilon_is_not_design_threshold':True}
  seats=u['public_program']['capacity']['living_seats'];activities=[u['activities'][s['access_activity_id']] for s in seats]
  table=u['fixtures'][u['dining_module_placement']['id_map']['table']]
  contact=first_positive_body_contact(r['path'],body,activities);dining=first_positive_body_contact(r['path'],body,u['rooms']['dining'])
  occupied=first_positive_body_contact(r['path'],body,chairs+[table]);ensure(occupied is None,'DINING_OCCUPANCY_COLLISION')
  out.update(capacity=cap,first_living_access_activity_contact_m=contact,first_declared_dining_floor_contact_m=dining,dining_occupied_material_contact_m=occupied,
   living_activity_contact_strictly_before_dining_floor=contact_order(contact,dining),
   contact_comparison_state='BOTH_OBSERVED' if contact is not None and dining is not None else 'REQUIRED_CONTACT_NOT_OBSERVED',
   contact_scope='Infimum of positive body overlap, not natural first destination. Tie is not living priority; access activity is not useful living floor.')
 except Exception as ex:out['error']={'type':type(ex).__name__,'message':str(ex)}
 finally:
  try:
   ensure(digest(bundle)==pin and digest(manifest)==mpin,'INPUT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SOURCE_CHANGED');out['integrity_verified']=True
  except Exception as ex:out.update(integrity_verified=False,integrity_error=type(ex).__name__+':'+str(ex))
  out['source_snapshot']=snap
 return out
