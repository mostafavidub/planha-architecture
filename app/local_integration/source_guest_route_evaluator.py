"""Task3.3 fresh four-route study with source destinations, not inherited routes."""
import copy,sys,inspect
from fractions import Fraction as F
from pathlib import Path
from front_rear_runtime_adapter import ROOT,ENGINE,ensure,transport,source_audit
from same_version_front_rear_contract import digest
from current_programme_evaluator import placed
from kitchen_guest_review import rect,sweeps
from guest_four_route_diagnostic import center,same_point
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def living_destination(u):
 d=u['public_program']['destinations']['guest_living']
 seats=[s for s in u['public_program']['capacity']['living_seats'] if s['fixture_id']==d['fixture_id']]
 ensure(len(seats)==1 and seats[0]['access_activity_id']==d['activity_id'],'LIVING_ACTIVITY_BINDING')
 ensure(d['fixture_id'] in u['fixtures'],'LIVING_FIXTURE')
 a=rect(u['activities'][d['activity_id']]);f=rect(u['fixtures'][d['fixture_id']])
 adjacent=((a[2]==f[0] or a[0]==f[2]) and max(a[1],f[1])<min(a[3],f[3])) or ((a[3]==f[1] or a[1]==f[3]) and max(a[0],f[0])<min(a[2],f[2]))
 ensure(adjacent,'LIVING_ACTIVITY_ADJACENCY')
 return center(u['activities'][d['activity_id']]),{'fixture_id':d['fixture_id'],'activity_id':d['activity_id'],'source':'Actual capacity instance/access binding plus original whole-model replay'}
def route_check(path,start,end,body,parts,obstacles):
 from public_program_audit118 import covered,hit
 ensure(body>0,'BODY_WIDTH')
 ensure(same_point(path[0],start) and same_point(path[-1],end),'ROUTE_ENDPOINT')
 bands=sweeps(path,body);ensure(bool(bands),'EMPTY_SWEEPS')
 for band in bands:
  ensure(covered(band,list(map(rect,parts))),'ROUTE_DOMAIN_COVERAGE')
  ensure(not any(hit(band,rect(q)) for q in obstacles),'ROUTE_OBSTACLE_COLLISION')
 return len(bands)
def assess(bundle):
 bundle,_=transport(bundle);pin=digest(bundle);m=bundle['packet']['world_model'];mh=digest(m)
 ensure(mh==bundle['model_digest'],'MODEL_DIGEST')
 for k,v in bundle['reports'].items():ensure(digest(v)==bundle['report_digests'][k],'ORIGINAL_REPORT_DIGEST')
 ensure(bundle['reports']['physical']['model_hash']==mh,'ORIGINAL_PHYSICAL_MODEL_BINDING')
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration')]
 from producer_provenance import snapshot,require_unchanged
 snap=snapshot(ROOT,['app/local_integration/source_guest_route_evaluator.py','app/local_integration/current_programme_evaluator.py','app/local_integration/kitchen_guest_review.py','app/local_integration/guest_four_route_diagnostic.py'])
 audit=source_audit()
 import construction_replay127
 from public_program_audit118 import bind_operation_destination,covered
 from geometry114 import route,cells
 ensure(Path(inspect.getsourcefile(route)).resolve()==(ENGINE/'geometry114.py').resolve(),'ROUTER_SOURCE')
 replay=construction_replay127.verify(m,bundle['context'])
 ensure(replay['verified'] is True and replay['model_hash']==mh,'REPLAY')
 ensure(digest(bundle)==pin,'REPLAY_INPUT_MUTATION')
 body=F(m['profile']['body_m']);ensure(body==F('.7'),'SOURCE_PROFILE_NOT_SUPPORTED')
 out={'schema':'SOURCE_BOUND_FOUR_GUEST_ROUTES_V1','criterion':'KITCHEN_GUEST_PATH_SEPARATION','state':'UNKNOWN',
  'model_digest':mh,'original_physical_digest':bundle['report_digests']['physical'],
  'original_physical_report':copy.deepcopy(bundle['reports']['physical']),'replay':copy.deepcopy(replay),'units':[],
  'profile':copy.deepcopy(m['profile']),'profile_scope':'Hypothetical source body width, not ergonomic approval',
  'remaining':['First-living/principal organisation unproved','Complete door/chair simultaneous scenario coverage unproved','Opening/bottleneck classification unproved','Conservative no-witness is not global infeasibility','This actual-work-area profile differs from historical whole-kitchen-floor exclusion; it does not overwrite that FAIL'],
  **{k:False for k in AUTH}}
 try:
  for u in m['units']:
   uid=u['id'];entry=u['entry_point'];living,lb=living_destination(u)
   d=u['public_program']['destinations']['guest_dining'];dining=center(u['activities'][d['activity_id']])
   db=bind_operation_destination(u,d,tuple(map(F,dining)))
   bp=[p for p in m['module_placements'] if p['unit_id']==uid and p['room_id']=='bath']
   ensure(len(bp)==1,'WC_MODULE');bp=bp[0];ensure(digest(bp['module'])==bp['module_hash'],'WC_MODULE_HASH')
   wcsource=bp['module']['unit']['activities']['WC_use'];wcactual=placed(wcsource,bp['transform'])
   ensure(wcactual==list(rect(u['activities']['WC_use'])),'WC_SOURCE_ACTIVITY')
   wc=center(u['activities']['WC_use'])
   ensure(same_point(u['route_targets']['WC_use'],wc),'WC_ROUTE_TARGET_SOURCE')
   ko=[o for o in m['operations']['kitchen'] if o['unit']==uid];ensure(len(ko)==1,'KITCHEN_OPERATION_INVENTORY');ko=ko[0]
   ensure(len(ko['motion_envelopes'])==6 and ko['workstations'] and ko['drawers'] and ko['fridge'],'KITCHEN_STATE_PROFILE')
   zones=[u['activities']['kitchen_work']]+ko['motion_envelopes']+[z['actor_rect'] for z in ko['workstations']]
   walls=list(m['walls'].values())+[z['open_panel'] for z in m['operations']['doors']]
   chair=[]
   for z in m['operations']['dining_chairs']:
    if z['unit']!=uid:continue
    a,b=rect(z['closed_rect']),rect(z['open_rect']);chair += [list(map(str,[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])])),z['occupied_body']]
   ensure(len(chair)==8,'DINING_CHAIR_STATE_INVENTORY')
   seats=u['public_program']['capacity']['living_seats']
   owner=u['ownership'];allq=list(map(rect,owner));box=list(map(str,[min(q[0] for q in allq),min(q[1] for q in allq),max(q[2] for q in allq),max(q[3] for q in allq)]))
   rows=[]
   for name,start,end in [('entry_living',entry,living),('entry_dining',entry,dining),('entry_WC',entry,wc),('living_dining',living,dining)]:
    try:
     roles=['living','entry_circulation','dining','kitchen']+(['bath'] if name=='entry_WC' else [])
     parts=[q for role in roles for q in u['rooms'].get(role,[])]
     # Source module approach/threshold floor is actual reserved floor, not an invented corridor.
     for p in m['module_placements']:
      if p['unit_id']==uid and p['room_id'] in (['kitchen','bath'] if name=='entry_WC' else ['kitchen']):
       parts += m['module_aprons'][uid+'.'+p['room_id']]
     parts=cells(parts,[]) # exact union, retains current role allocation
     outside=cells([box],parts)+cells([box],owner)
     private=[q for key,qs in u['rooms'].items() if key.startswith('bed') or key=='private_circulation' for q in qs]
     fx=[q for k,q in u['fixtures'].items() if not u['fixture_metadata'][k].get('walkable') and not(name=='entry_WC' and k=='WC_iranian')]
     if name=='entry_WC':
      x,y=map(F,wc);target_body=list(map(str,[x-body/2,y-body/2,x+body/2,y+body/2]))
      fx+=cells([u['fixtures']['WC_iranian']],[target_body])
     occupied=[s['occupied_body'] for s in seats]
     obstacles=walls+fx+chair+private+zones+occupied+outside
     path,reason=route(start,end,box,obstacles,body=str(body))
     row={'id':name,'start':start,'end':end,'floor_roles':roles,'floor_digest':digest(parts),'ownership_digest':digest(owner),'domain_box':box,'obstacle_digest':digest(obstacles),
      'obstacle_count':len(obstacles),'path':path,'reason':reason,'state':'NO_WITNESS_IN_THIS_CONSERVATIVE_SCENARIO',
      'wc_exception':'Only target body intersection with own WC fixture; all remaining WC fixture material stays obstacle' if name=='entry_WC' else None}
     if path:
      count=route_check(path,start,end,body,parts,obstacles)
      for band in sweeps(path,body):ensure(covered(band,list(map(rect,owner))),'OWNER_COVERAGE')
      row.update(state='PASS_SOURCE_PROFILE_ROUTE_ONLY',segments=count,length_m=str(sum(abs(F(a[0])-F(b[0]))+abs(F(a[1])-F(b[1])) for a,b in zip(path,path[1:]))))
    except Exception as ex:row={'id':name,'state':'UNKNOWN_EVALUATOR_OR_BINDING_ERROR','error':type(ex).__name__+':'+str(ex)}
    rows.append(row)
   out['units'].append({'unit':uid,'destination_bindings':{'living':lb,'dining':db,'WC':{'module_hash':bp['module_hash'],'activity_id':'WC_use'}},
    'historical_guest_dining_route_present':'guest_dining' in u['scenario_routes'],'kitchen_operation_digest':digest(ko),
    'scenario':'Actual kitchen workstations and six conservative motions; open door panels; all dining chair swept/occupied and living occupied bodies',
    'routes':rows})
 except Exception as ex:out['missing']=[type(ex).__name__+':'+str(ex)]
 finally:
  try:
   ensure(digest(bundle)==pin,'MODEL_OR_REPORT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SOURCE_CHANGED')
   out['integrity_verified']=True
  except Exception as ex:out.update(integrity_verified=False,integrity_error=type(ex).__name__+':'+str(ex))
  out['source_snapshot']=snap
 return out
