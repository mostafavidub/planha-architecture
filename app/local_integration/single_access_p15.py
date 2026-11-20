"""Independent exact one-unit ownership/access check; no quality admission."""
import copy
from fractions import Fraction as F
from single_model_p15 import digest,require,core,RAW,FAMILY,AUTH
from checker114 import rect,intersects,covered,sweeps
# Explicit P15 adaptation of source programme inventory: one actual unit, same P2 fixtures.
def placed(q,t):
 a=rect(q);M=t['matrix'];v=t['translation']
 require(type(M) is list and len(M)==2 and all(type(r) is list and len(r)==2 for r in M),'ISOMETRY_SHAPE')
 require(all(type(x) is int and x in (-1,0,1) for r in M for x in r),'ISOMETRY_TYPE')
 require(all(sum(M[i][j]*M[k][j] for j in (0,1))==int(i==k) for i in (0,1) for k in (0,1)),'ISOMETRY_ORTHOGONAL')
 require(type(v) is list and len(v)==2,'TRANSLATION')
 pts=[[sum(F(M[i][j])*p[j] for j in (0,1))+F(str(v[i])) for i in (0,1)] for p in ((a[0],a[1]),(a[0],a[3]),(a[2],a[1]),(a[2],a[3]))]
 return (min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts))
def inventory(model,profile,catalog):
 """Source-profile identity/shape audit only; caller must establish original replay."""
 expected={'units':1,'bedrooms_per_unit':2,'sleep_roles':['double','twin'],'design_occupants_per_unit':4,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True}
 for k,v in expected.items():require(digest(model['program'][k])==digest(v),'PROGRAM_IDENTITY:'+k)
 require(profile['id']=='PROGRAM_2BED_V1' and profile['approval']['status']=='APPROVED_DESIGN_PROGRAM','REGISTRY_APPROVAL')
 require(digest([profile['bedrooms_per_unit'],profile['design_persons_per_unit'],profile['sleep_roles'],profile['capacity_means_actual_population']])==digest([2,4,['double','twin'],False]),'REGISTRY_BINDING')
 units=model['units'];require(len(units)==1 and {u['id'] for u in units}=={'A'},'UNITS')
 expected_modules={'bed1':'PRIVATE_ROOM_MODULE116','bed2':'PRIVATE_TWIN_ROOM_MODULE118','bath':'BATHROOM_MODULE117','kitchen':'KITCHEN_MODULE117'}
 rows=[]
 for u in units:
  uid=u['id'];ps=[p for p in model['module_placements'] if p['unit_id']==uid]
  require(len(ps)==4 and {p['room_id'] for p in ps}==set(expected_modules),'PLACEMENT_INVENTORY')
  fids=set();aids=set();bindings=[]
  for p in ps:
   module=p['module'];require(digest(module)==p['module_hash'],'MODULE_HASH')
   require(module['schema']==expected_modules[p['room_id']],'MODULE_ROLE')
   for category,seen in (('fixtures',fids),('activities',aids)):
    for key,q in module['unit'][category].items():
     target=p['id_map'][key];require(target not in seen,'REUSED_SOURCE_'+category)
     require(placed(q,p['transform'])==rect(u[category][target]),'ACTUAL_SOURCE_'+category+':'+uid+'.'+target)
     seen.add(target)
   bindings.append({'room':p['room_id'],'module_hash':p['module_hash'],'transform_digest':digest(p['transform'])})
  dp=u['dining_module_placement'];dm=dp['module']
  require(digest(dm)==dp['module_hash'],'DINING_MODULE_HASH')
  for key,q in dm['fixtures'].items():
   target=dp['id_map'][key];require(target not in fids,'REUSED_DINING_FIXTURE')
   require(placed(q,dp['transform'])==rect(u['fixtures'][target]),'DINING_SOURCE_FIXTURE');fids.add(target)
  seats=dm['seating']['instances'];require(len(seats)==4 and len({s['fixture_id'] for s in seats})==4,'DINING_SOURCE_INSTANCES')
  for seat in seats:
   aid='dining_'+seat['id'][5:]
   require(aid not in aids,'REUSED_DINING_ACTIVITY')
   require(placed(seat['rise_transfer']['standing_body'],dp['transform'])==rect(u['activities'][aid]),'DINING_ACTIVITY_BINDING')
   aids.add(aid)
  for fid in profile['source_inventory']['living_items']:
   q=rect(u['fixtures'][fid]);kind=u['fixture_metadata'][fid]['kind'];source=catalog['types'][kind]
   require(kind==fid,'LIVING_SOURCE_KIND')
   require(sorted((q[2]-q[0],q[3]-q[1]))==sorted((F(source['width_m']),F(source['depth_m']))),'LIVING_SOURCE_DIMENSIONS')
   require(fid not in fids,'REUSED_LIVING_FIXTURE')
   fids.add(fid);aid=fid+'_front';require(aid not in aids,'REUSED_LIVING_ACTIVITY');rect(u['activities'][aid]);aids.add(aid)
  require(set(u['fixtures'])==fids,'WHOLE_SOURCE_FIXTURE_SET')
  activity_rows=[{'activity_id':a,'present':True,'route_state':'PRESENT_NOT_RECHECKED_HERE' if u['routes'].get(a) else 'MISSING_ROUTE_WITNESS',
    'target_state':'PRESENT' if a in u['route_targets'] else 'MISSING_TARGET_BINDING'} for a in sorted(aids)]
  rows.append({'unit':uid,'design_persons':4,'fixture_ids':sorted(fids),'required_source_activity_ids':sorted(aids),
   'additional_activity_ids':sorted(set(u['activities'])-aids),'activity_coverage':activity_rows,'module_bindings':bindings,
   'dining_module_hash':dp['module_hash'],'dining_transfer_profile_validated':[s['rise_transfer']['human_transfer_and_support_profile_validated'] for s in seats],
   'operation_state_coverage':[{'category':category,'records':len([z for z in records if z.get('unit')==uid]),'state':'PRESENT_SOURCE_RECORDS_NOT_INDEPENDENT_FUNCTIONAL_APPROVAL'} for category,records in model['operations'].items() if type(records) is list],
   'activity_phase_coverage':{'arrival':'Source route presence recorded; actual clearance retained in original physical report','use':'Fresh limited capacity audit; other module operations only original physical evidence','exit':'NOT_INDEPENDENTLY_EVALUATED','simultaneous_states':'SOURCE_SCENARIOS_PARTIAL_NOT_COMPREHENSIVE_PROFILE'},'living_location_binding':'Original whole-construction replay; source dimensions independently compared',
   'operations_coverage':'Original physical report retained separately; this inventory checker does not re-prove operation collisions or simultaneous state completeness'})
 return rows

def assess(m):
 before=digest(m);errors=[];evidence={}
 def need(ok,code):
  if not ok:raise ValueError(code)
 try:
  need(m.get('schema')==FAMILY and m.get('contract_version')=='p15-single-v1','MODEL_SCHEMA')
  need(digest(m['inputs'])==digest(['18','20',1]),'INPUT_BINDING')
  need(type(m['program']['units'])is int and m['program']['units']==1,'PROGRAM_UNITS')
  need(type(m['program']['bedrooms_per_unit'])is int and m['program']['bedrooms_per_unit']==2 and m['program']['sleep_roles']==['double','twin'] and type(m['program']['design_occupants_per_unit'])is int and m['program']['design_occupants_per_unit']==4,'PROGRAMME')
  need(type(m['units'])is list and len(m['units'])==1 and m['units'][0]['id']=='A','EXACT_ONE_UNIT')
  need(all(m.get(k)is False for k in AUTH),'AUTHORITY')
  c=core(RAW);u=m['units'][0];owner=[rect(q)for q in u['ownership']]
  need(digest(u['ownership'])==digest(c['unit_ownership']['A']),'OWNERSHIP_BINDING')
  need(digest(m['common_spaces'])==digest({k:c[k]for k in('stair','lift','lobby')}),'CORE_BINDING')
  # Every unit-bearing reference and relation is accounted, not only len(units).
  def scan(v):
   if type(v)is dict:
    for k,x in v.items():
     need(not(k=='B' or k.startswith('B.') or k.endswith('_B')),'HIDDEN_UNIT_REFERENCE')
     if k=='unit':need(x in('A','COMMON'),'HIDDEN_UNIT_OWNER')
     if k not in ('module','fixture_catalog'):scan(x)
   elif type(v)is list:
    for x in v:scan(x)
   elif type(v)is str:need(not(v=='B' or v.startswith('B.') or v.endswith('_B')),'HIDDEN_UNIT_REFERENCE')
  scan(m)
  need(set(m['common_routes'])=={'stair_A','lift_A'},'COMMON_ROUTE_SET')
  need(set(u['rooms'])>={'bed1','bed2','bath','kitchen','dining','living'},'ROOM_INVENTORY')
  need(bool(u['routes']),'UNIT_ROUTE_EMPTY')
  walls={k:rect(q)for k,q in m['walls'].items()}
  frame=rect(['0','0','18','20'])
  for q in walls.values():need(covered(q,[frame]),'WALL_OUTSIDE_FRAME')
  for rs in u['rooms'].values():
   for q in rs:need(covered(rect(q),owner),'ROOM_OUTSIDE_OWNERSHIP')
  for q in u['fixtures'].values():need(covered(rect(q),owner),'FIXTURE_OUTSIDE_OWNERSHIP')
  from single_model_p15 import ENGINE
  from program_profile_registry import lookup
  import json
  catalog=json.loads((ENGINE/'fixture_catalog114.json').read_text())
  need(m['fixture_catalog_hash']==digest(catalog),'CATALOG_HASH')
  inventory_rows=inventory(m,lookup('PROGRAM_2BED_V1'),catalog)
  for x in m['module_placements']:
   need(x['unit_id']=='A','MODULE_OWNER')
  for q in owner:
   for r in [rect(c['stair']),rect(c['lift']),*[rect(z)for z in c['lobby']]]:
    need(not intersects(q,r),'OWNERSHIP_COMMON_OVERLAP')
  openings=m['openings']
  roles=set(m['logical_regions'])|{'A.'+k for k in u['rooms']}|{'stair','lift','lobby'}
  need(all(type(o['connects'])is list and len(o['connects'])==2 and all(x in roles for x in o['connects'])for o in openings),'OPENING_OWNER_REFERENCE')
  entry=[o for o in openings if o['id']=='A.entry']
  need(len(entry)==1 and set(entry[0]['connects'])=={'lobby','A.public_access'},'ENTRY_BINDING')
  entryq=rect(entry[0]['rect']);cx=(entryq[0]+entryq[2])/2
  target=[cx,owner[0][3]-F('.4')]
  ports={o['id']:rect(o['rect'])for o in openings if o['id']in('stair.entry','lift.entry','A.entry')}
  need(set(ports)=={'stair.entry','lift.entry','A.entry'},'CORE_PORTS')
  all_floor=owner+[rect(c['stair']),rect(c['lift']),*[rect(q)for q in c['lobby']],*ports.values(),*walls.values()]
  need(covered(frame,all_floor),'UNACCOUNTED_FLOOR_GAP')
  panels=[rect(o['open_panel'])for o in m['operations']['doors']]
  routes=[]
  for source in('stair','lift'):
   path=m['common_routes'][source+'_A'];a,b,C,d=rect(c[source]);cy=(b+d)/2
   start=[C-F('.4'),cy]if source=='stair'else[a+F('.4'),cy]
   need([F(x)for x in path[0]]==start and [F(x)for x in path[-1]]==target,'COMMON_ROUTE_ENDPOINT')
   domains=[rect(c[source]),*[rect(q)for q in c['lobby']],ports[source+'.entry'],ports['A.entry'],*[rect(q)for q in u['rooms']['entry_circulation']]]
   sw=sweeps(path)
   for q in sw:
    need(covered(q,domains),'COMMON_ROUTE_FLOOR')
    need(not any(intersects(q,z)for z in walls.values()),'COMMON_ROUTE_WALL')
    need(not any(intersects(q,z)for z in panels),'COMMON_ROUTE_OPEN_PANEL')
   routes.append({'id':source+'_A','body_width_m':'0.7','segments':len(sw),'verified':True})
  # At least one genuinely clear internal route from the same entry, not an empty path placeholder.
  clear=[]
  fixtures={k:rect(q)for k,q in u['fixtures'].items()}
  for key,path in u['routes'].items():
   if not path:continue
   if [F(x)for x in path[0]]!=target:continue
   if key not in u['route_targets']or [F(x)for x in path[-1]]!=[F(x)for x in u['route_targets'][key]]:continue
   if all(covered(q,owner)and not any(intersects(q,z)for z in list(walls.values())+panels+list(fixtures.values()))for q in sweeps(path)):clear.append(key)
  need(bool(clear),'NO_CLEAR_ENTRY_TO_UNIT_ACTIVITY')
  evidence={'unit_ids':['A'],'source_inventory':inventory_rows,'whole_frame_accounted':True,'common_routes':routes,'clear_internal_routes':sorted(clear),
            'ownership_digest':digest(u['ownership']),'core_digest':digest(c),'fixture_count':len(fixtures),
            'scope':'Necessary single-unit ownership and entry access only; not every activity, quality, privacy, or legal/technical approval'}
 except (KeyError,TypeError,ValueError,IndexError)as ex:
  errors.append({'code':str(ex)if type(ex)is ValueError else 'MALFORMED_MODEL','type':type(ex).__name__})
 require(digest(m)==before,'MODEL_MUTATED')
 return {'schema':'SINGLE_UNIT_OWNERSHIP_ACCESS_P15_V1','model_digest':before,
  'state':'FAIL'if errors else'PASS_SCOPED_OWNERSHIP_ACCESS','errors':errors,'evidence':evidence,
  'four_current_state':'NOT_EVALUATED','qualified':False,'accepted':False,'display_allowed':False,'delivery_allowed':False}
