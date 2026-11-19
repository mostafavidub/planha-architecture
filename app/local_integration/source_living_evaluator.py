"""Task3.4 living evidence accounting, not architectural usefulness certification."""
import copy,sys,inspect
from fractions import Fraction as F
from pathlib import Path
from front_rear_runtime_adapter import ROOT,ENGINE,ensure,transport,source_audit
from same_version_front_rear_contract import digest
from source_guest_route_evaluator import living_destination,route_check
from living_connectivity_diagnostic import direction_changes
from fixed_route_clearance_diagnostic import fixed_polyline_capacity
from kitchen_guest_review import rect,sweeps
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def union_area(parts):
 from geometry114 import cells
 return sum((F(q[2])-F(q[0]))*(F(q[3])-F(q[1])) for q in cells(parts,[]))
def box_of(parts):
 q=list(map(rect,parts));ensure(bool(q),'EMPTY_DOMAIN')
 return list(map(str,[min(x[0] for x in q),min(x[1] for x in q),max(x[2] for x in q),max(x[3] for x in q)]))
def assess(bundle):
 from current_entry_boundary_x03 import check_model_domain
 check_model_domain(bundle['packet']['world_model'])
 bundle,_=transport(bundle);pin=digest(bundle);m=bundle['packet']['world_model'];mh=digest(m)
 ensure(mh==bundle['model_digest'],'MODEL_DIGEST')
 ensure(bundle['reports']['physical']['model_hash']==mh,'PHYSICAL_MODEL_BINDING')
 for k,v in bundle['reports'].items():ensure(digest(v)==bundle['report_digests'][k],'ORIGINAL_REPORT_DIGEST')
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration')]
 from producer_provenance import snapshot,require_unchanged
 snap=snapshot(ROOT,['app/local_integration/current_entry_boundary_x03.py','app/local_integration/source_living_evaluator.py','app/local_integration/source_guest_route_evaluator.py','app/local_integration/living_connectivity_diagnostic.py','app/local_integration/fixed_route_clearance_diagnostic.py','app/local_integration/kitchen_guest_review.py'])
 audit=source_audit()
 import construction_replay127
 from geometry114 import cells,route
 for fn,name in ((cells,'fast_cells120.py'),(route,'fast_route120.py')):
  ensure(Path(inspect.getsourcefile(fn)).resolve()==(ENGINE/name).resolve(),'ACTUAL_SOURCE')
 replay=construction_replay127.verify(m,bundle['context']);ensure(replay['verified'] is True and replay['model_hash']==mh,'REPLAY')
 ensure(digest(bundle)==pin,'REPLAY_MUTATION')
 body=F(m['profile']['body_m']);ensure(body==F('.7'),'PROFILE')
 out={'current_domain_policy':'CURRENT_ENTRY_DOMAIN_X03_V1','schema':'CURRENT_LIVING_SOURCE_EVIDENCE_V1','criterion':'CONTINUOUS_USEFUL_LIVING','state':'UNKNOWN','model_digest':mh,
  'original_physical_digest':bundle['report_digests']['physical'],'original_physical_report':copy.deepcopy(bundle['reports']['physical']),
  'units':[],'profile':copy.deepcopy(m['profile']),'replay':copy.deepcopy(replay),
  'scope':'Source-bound seating access, exact area accounting and limited local-group-domain probe. Not a complete coherent usable living proof.',
  'remaining':['Calibrated activity/ergonomic/quality profiles unavailable','Coherent furnishing and all simultaneous use/exit scenarios unproved','No same-programme shorter physical organisation constructed or compared','Geometric residual and declared used footprint are not verified useful area'],
  **{k:False for k in AUTH}}
 try:
  for u in m['units']:
   uid=u['id'];seats=u['public_program']['capacity']['living_seats']
   expected={'sofa1','sofa2','armchair1','armchair2'}
   ensure(len(seats)==4 and {s['fixture_id'] for s in seats}==expected,'SEAT_INVENTORY')
   endpoints=[];footprints=[]
   for s in seats:
    temporary=copy.deepcopy(u);temporary['public_program']['destinations']['guest_living']={'fixture_id':s['fixture_id'],'activity_id':s['access_activity_id']}
    point,binding=living_destination(temporary);endpoints.append({'fixture_id':s['fixture_id'],'activity_id':s['access_activity_id'],'point':point,'binding':binding})
    footprints += [u['fixtures'][s['fixture_id']],u['activities'][s['access_activity_id']]]
   anchor=u['public_program']['destinations']['guest_living']['fixture_id'];ensure(anchor in expected,'ANCHOR')
   endpoints.sort(key=lambda x:(x['fixture_id']!=anchor,x['fixture_id']))
   walls=list(m['walls'].values());doorpanels=[z['open_panel'] for z in m['operations']['doors']]
   chairs=[]
   for z in m['operations']['dining_chairs']:
    if z['unit']==uid:
     a,b=rect(z['closed_rect']),rect(z['open_rect']);chairs += [list(map(str,[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])])),z['occupied_body']]
   kitchens=[z for z in m['operations']['kitchen'] if z['unit']==uid];ensure(len(kitchens)==1,'KITCHEN_INVENTORY')
   kitchen=kitchens[0];ensure(len(kitchen['motion_envelopes'])==6,'KITCHEN_MOTIONS')
   ko=kitchen['motion_envelopes']+[z['actor_rect'] for z in kitchen['workstations']]+[u['activities']['kitchen_work']]
   private=[q for k,qs in u['rooms'].items() if k.startswith('bed') or k in ('bath','private_circulation') for q in qs]
   base=walls+doorpanels+list(u['fixtures'].values())+[s['occupied_body'] for s in seats]+chairs+ko+private
   owner=u['ownership'];domain=box_of(owner);gross=union_area(owner);net=union_area(cells(owner,walls))
   living=cells(u['rooms']['living'],walls);access=cells(u['rooms']['living']+u['rooms']['entry_circulation'],walls)
   groupbox=box_of(footprints);group=cells([groupbox],cells([groupbox],access))
   studies=[]
   for name,floor in [('DECLARED_RESIDUAL_LIVING',living),('AUTHORIZED_LIVING_AND_CIRCULATION_ACCESS',access),('LOCAL_SEAT_GROUP_BBOX_DOMAIN_ONLY',group)]:
    outside=cells([domain],floor)+cells([domain],owner);obs=base+outside;rows=[]
    for target in endpoints[1:]:
     try:
      path,reason=route(endpoints[0]['point'],target['point'],domain,obs,body=str(body))
      row={'target_fixture':target['fixture_id'],'path':path,'reason':reason,'state':'NO_WITNESS_THIS_DOMAIN','body_m':str(body)}
      if path:
       route_check(path,endpoints[0]['point'],target['point'],body,floor,obs)
       clearance=fixed_polyline_capacity(path,domain,obs)
       capacity=F(clearance['maximum_uniform_axis_aligned_square_width_m']);ensure(capacity>=body,'CLEARANCE_CONTRADICTION')
       route_check(path,endpoints[0]['point'],target['point'],capacity,floor,obs)
       epsilon=F(1,1000000)
       try:route_check(path,endpoints[0]['point'],target['point'],capacity+epsilon,floor,obs)
       except ValueError as ex:
        ensure(str(ex) in ('ROUTE_DOMAIN_COVERAGE','ROUTE_OBSTACLE_COLLISION'),'NON_GEOMETRIC_CLEARANCE_REJECTION')
        clearance['sweep_certificate']={'at_capacity_clear':True,'capacity_plus_test_epsilon_rejected':True,'test_epsilon_not_design_threshold':str(epsilon)}
       else:raise ValueError('CLEARANCE_NEGATIVE_CERTIFICATE')
       row.update(state='PASS_ACCESS_WITNESS_ONLY',length_m=str(sum(abs(F(a[0])-F(b[0]))+abs(F(a[1])-F(b[1])) for a,b in zip(path,path[1:]))),direction_changes_including_reversal=direction_changes(path),fixed_path_clearance=clearance)
     except Exception as ex:row={'target_fixture':target['fixture_id'],'path':None,'state':'EVALUATOR_ERROR','error':type(ex).__name__+':'+str(ex)}
     rows.append(row)
    studies.append({'domain':name,'floor_digest':digest(floor),'obstacle_digest':digest(obs),'anchor_fixture_id':anchor,'target_fixture_ids':[e['fixture_id'] for e in endpoints[1:]],
     'floor_area_m2':str(union_area(floor)),'routes':rows,'all_targets_connected':bool(rows) and all(r['path'] for r in rows),
     'not_a_useful_area_or_coherent_group_claim':True})
   area=union_area(living);used=union_area(footprints)
   out['units'].append({'unit':uid,'actual_seat_endpoints':endpoints,'studies':studies,
    'area_accounting':{'gross_unit_ownership_union_m2':str(gross),'net_unit_ownership_minus_actual_wall_solids_m2':str(net),
     'declared_residual_living_union_m2':str(area),'declared_fixture_activity_union_m2':str(used),
     'residual_over_gross_ownership':str(area/gross),'residual_over_net_nonwall_floor':str(area/net),
     'area_ratios_are_geometric_not_quality_scores':True,'verified_useful_living_area_m2':None},
    'group_bbox':groupbox,'group_bbox_is_only_probe_domain':True,
    'shorter_organisation_comparison':{'state':'NOT_RUN','reason':'No alternative physical organisation supplied under the same locked programme; domain comparisons on same geometry are not organisation alternatives'},
    'activity_phase_coverage':{'approach':'Independent width sweep per recorded route','use':'Original source seat activities and occupied bodies; fresh approach is not seated transfer proof','exit_and_simultaneous_group_use':'NOT_FULLY_VERIFIED'}})
 except Exception as ex:out['missing']=[type(ex).__name__+':'+str(ex)]
 finally:
  try:
   ensure(digest(bundle)==pin,'MODEL_REPORT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SOURCE_CHANGED');out['integrity_verified']=True
  except Exception as ex:out.update(integrity_verified=False,integrity_error=type(ex).__name__+':'+str(ex))
  out['source_snapshot']=snap
 return out
