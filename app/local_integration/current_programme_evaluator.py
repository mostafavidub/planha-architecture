"""Task3.2 actual source-programme inventory and evidence coverage, not quality approval."""
import copy,inspect,json,sys
from fractions import Fraction as F
from pathlib import Path
from front_rear_runtime_adapter import ROOT,ENGINE,ensure,transport,source_audit,preserve_report,verify_reports
from same_version_front_rear_contract import digest,ENGINE_REVISION
from program_profile_registry import lookup
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def rect(q):
 ensure(type(q) is list and len(q)==4,'RECT_SHAPE')
 v=[F(str(x)) for x in q];ensure(v[0]<v[2] and v[1]<v[3],'RECT_EXTENT');return v
def placed(q,t):
 a=rect(q);M=t['matrix'];v=t['translation']
 ensure(type(M) is list and len(M)==2 and all(type(r) is list and len(r)==2 for r in M),'ISOMETRY_SHAPE')
 ensure(all(type(x) is int and x in (-1,0,1) for r in M for x in r),'ISOMETRY_TYPE')
 ensure(all(sum(M[i][j]*M[k][j] for j in (0,1))==int(i==k) for i in (0,1) for k in (0,1)),'ISOMETRY_ORTHOGONAL')
 ensure(type(v) is list and len(v)==2,'TRANSLATION')
 pts=[[sum(F(M[i][j])*p[j] for j in (0,1))+F(str(v[i])) for i in (0,1)] for p in ((a[0],a[1]),(a[0],a[3]),(a[2],a[1]),(a[2],a[3]))]
 return [min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)]
def inventory(model,profile,catalog):
 """Source-profile identity/shape audit only; caller must establish original replay."""
 expected={'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin'],'design_occupants_per_unit':4,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True}
 for k,v in expected.items():ensure(digest(model['program'][k])==digest(v),'PROGRAM_IDENTITY:'+k)
 ensure(profile['id']=='PROGRAM_2BED_V1' and profile['approval']['status']=='APPROVED_DESIGN_PROGRAM','REGISTRY_APPROVAL')
 ensure(digest([profile['bedrooms_per_unit'],profile['design_persons_per_unit'],profile['sleep_roles'],profile['capacity_means_actual_population']])==digest([2,4,['double','twin'],False]),'REGISTRY_BINDING')
 units=model['units'];ensure(len(units)==2 and {u['id'] for u in units}=={'A','B'},'UNITS')
 expected_modules={'bed1':'PRIVATE_ROOM_MODULE116','bed2':'PRIVATE_TWIN_ROOM_MODULE118','bath':'BATHROOM_MODULE117','kitchen':'KITCHEN_MODULE117'}
 rows=[]
 for u in units:
  uid=u['id'];ps=[p for p in model['module_placements'] if p['unit_id']==uid]
  ensure(len(ps)==4 and {p['room_id'] for p in ps}==set(expected_modules),'PLACEMENT_INVENTORY')
  fids=set();aids=set();bindings=[]
  for p in ps:
   module=p['module'];ensure(digest(module)==p['module_hash'],'MODULE_HASH')
   ensure(module['schema']==expected_modules[p['room_id']],'MODULE_ROLE')
   for category,seen in (('fixtures',fids),('activities',aids)):
    for key,q in module['unit'][category].items():
     target=p['id_map'][key];ensure(target not in seen,'REUSED_SOURCE_'+category)
     ensure(placed(q,p['transform'])==rect(u[category][target]),'ACTUAL_SOURCE_'+category+':'+uid+'.'+target)
     seen.add(target)
   bindings.append({'room':p['room_id'],'module_hash':p['module_hash'],'transform_digest':digest(p['transform'])})
  dp=u['dining_module_placement'];dm=dp['module']
  ensure(digest(dm)==dp['module_hash'],'DINING_MODULE_HASH')
  for key,q in dm['fixtures'].items():
   target=dp['id_map'][key];ensure(target not in fids,'REUSED_DINING_FIXTURE')
   ensure(placed(q,dp['transform'])==rect(u['fixtures'][target]),'DINING_SOURCE_FIXTURE');fids.add(target)
  seats=dm['seating']['instances'];ensure(len(seats)==4 and len({s['fixture_id'] for s in seats})==4,'DINING_SOURCE_INSTANCES')
  for seat in seats:
   aid='dining_'+seat['id'][5:]
   ensure(placed(seat['rise_transfer']['standing_body'],dp['transform'])==rect(u['activities'][aid]),'DINING_ACTIVITY_BINDING')
   aids.add(aid)
  for fid in profile['source_inventory']['living_items']:
   q=rect(u['fixtures'][fid]);kind=u['fixture_metadata'][fid]['kind'];source=catalog['types'][kind]
   ensure(kind==fid,'LIVING_SOURCE_KIND')
   ensure(sorted((q[2]-q[0],q[3]-q[1]))==sorted((F(source['width_m']),F(source['depth_m']))),'LIVING_SOURCE_DIMENSIONS')
   fids.add(fid);aid=fid+'_front';rect(u['activities'][aid]);aids.add(aid)
  ensure(set(u['fixtures'])==fids,'WHOLE_SOURCE_FIXTURE_SET')
  activity_rows=[{'activity_id':a,'present':True,'route_state':'PRESENT_NOT_RECHECKED_HERE' if u['routes'].get(a) else 'MISSING_ROUTE_WITNESS',
    'target_state':'PRESENT' if a in u['route_targets'] else 'MISSING_TARGET_BINDING'} for a in sorted(aids)]
  rows.append({'unit':uid,'design_persons':4,'fixture_ids':sorted(fids),'required_source_activity_ids':sorted(aids),
   'additional_activity_ids':sorted(set(u['activities'])-aids),'activity_coverage':activity_rows,'module_bindings':bindings,
   'dining_module_hash':dp['module_hash'],'living_location_binding':'Original whole-construction replay; source dimensions independently compared',
   'operations_coverage':'Original physical report retained separately; this inventory checker does not re-prove operation collisions or simultaneous state completeness'})
 return rows
def assess(bundle):
 """Same-model artifact evaluation. No generator, repair or admission."""
 bundle,_=transport(bundle);baseline=digest(bundle);model=bundle['packet']['world_model'];mh=digest(model)
 ensure(mh==bundle['model_digest'],'MODEL_DIGEST')
 for k,v in bundle['reports'].items():ensure(digest(v)==bundle['report_digests'][k],'REPORT_DIGEST:'+k)
 ensure(bundle['reports']['physical']['model_hash']==mh,'PHYSICAL_MODEL')
 profile=lookup('PROGRAM_2BED_V1');profilepin=digest(profile)
 audit=source_audit()
 from producer_provenance import snapshot,require_unchanged
 snap=snapshot(ROOT,['app/local_integration/current_programme_evaluator.py','app/local_integration/program_profile_registry.py','specs/V25_TASK_3_1_CURRENT_FUNCTIONAL_CRITERIA.json'])
 import construction_replay127,program_capacity_audit118
 for mod,fn in ((construction_replay127,'verify'),(program_capacity_audit118,'examine')):
  ensure(Path(inspect.getsourcefile(getattr(mod,fn))).resolve()==(ENGINE/(mod.__name__+'.py')).resolve(),'ACTUAL_EVALUATOR_SOURCE')
 reports={};live={};pins={}
 out={'schema':'CURRENT_PROGRAMME_SOURCE_EVALUATION_V1','criterion':'CURRENT_PROGRAM_SUITABILITY',
  'model_digest':mh,'profile_digest':profilepin,'engine_revision':ENGINE_REVISION,'state':'UNKNOWN',
  'scope':'Approved two-bedroom/four-design-person source programme, source-bound inventory and limited planar capacity; not quality, automatic selection or whole-bundle qualification',
  'findings':[],'reports':reports,**{k:False for k in AUTH}}
 try:
  replay=construction_replay127.verify(model,bundle['context']);preserve_report(reports,live,pins,'replay',replay)
  ensure(replay['verified'] is True and replay['model_hash']==mh,'ORIGIN_NOT_VERIFIED')
  cat=json.loads((ENGINE/'fixture_catalog114.json').read_text())
  ensure(model['fixture_catalog_hash']==digest(cat),'FIXTURE_CATALOG_BINDING')
  out['inventory']=inventory(model,profile,cat)
  cap=program_capacity_audit118.examine(model);preserve_report(reports,live,pins,'capacity',cap)
  ensure(cap['evidence']['model_hash']==mh,'CAPACITY_BINDING')
  out['source_capacity_state']='FAIL_SCOPED' if cap['errors'] else 'UNKNOWN' if cap['pending'] else 'PASS_SCOPED'
  out['historical_physical_report']=copy.deepcopy(bundle['reports']['physical'])
  out['historical_physical_digest']=bundle['report_digests']['physical']
  out['findings']=[
   {'kind':'MISSING_PROFILE','code':'CALIBRATED_ROOM_UNIT_QUALITY_AND_ERGONOMIC_SCENARIOS'},
   {'kind':'MISSING_RULE','code':'OPERATIONAL_QUALITY_DIMENSIONS_AND_ACCEPTANCE_ANCHORS_OPEN'},
   {'kind':'MISSING_EVIDENCE','code':'AP07_ALTERNATIVE_SEQUENCE_AND_PARETO_SELECTION'},
   {'kind':'MISSING_EVIDENCE','code':'CLOTHING_STORAGE_VOLUME_AND_FULL_SIMULTANEOUS_BUNDLE_ADEQUACY'},
   {'kind':'NOT_EVALUATED','code':'NET_CAPACITY_PREFILTER_SOURCE_BOUND_NOT_AVAILABLE'}]
  if cap['errors']:out['findings'].append({'kind':'SOURCE_PROFILE_VIOLATION','code':'SCOPED_CAPACITY_FAILURE','errors':cap['errors']})
  out['decision']='BLOCK_DELIVERY_UNKNOWN_PROGRAMME_AND_RETAIN_INDEPENDENT_PHYSICAL_RESULT'
 except Exception as ex:
  out.update(state='UNKNOWN',decision='BLOCK_DELIVERY_INVALID_OR_INCOMPLETE_EVIDENCE')
  out['findings'].append({'kind':'EVALUATOR_OR_SOURCE_BINDING_ERROR','type':type(ex).__name__,'detail':str(ex)})
 finally:
  verify_reports(reports,pins);verify_reports(live,pins)
  ensure(digest(bundle)==baseline and digest(profile)==profilepin,'INPUT_MUTATION')
  require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SOURCE_CHANGED')
  out.update(report_digests=pins,source_snapshot=snap,input_bundle_digest=baseline)
 return out
