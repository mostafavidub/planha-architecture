"""Eight dining arrivals in a source-bound hypothetical planar state, never admission."""
import copy,inspect,json,pathlib,sys
from fractions import Fraction as F
from front_rear_runtime_adapter import ROOT,ENGINE,ensure,transport,source_audit
from same_version_front_rear_contract import digest
from current_programme_evaluator import placed,inventory
from program_profile_registry import lookup
from source_guest_route_evaluator import route_check
from kitchen_guest_review import rect,sweeps
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def strict_json(x):
 if x is None or type(x) in (bool,str,int):return
 if type(x) is float:
  import math
  ensure(math.isfinite(x),'NONFINITE');return
 if type(x) is list:
  for v in x:strict_json(v)
 elif type(x) is dict:
  ensure(all(type(k) is str for k in x),'JSON_KEY')
  for v in x.values():strict_json(v)
 else:raise ValueError('NON_JSON_TYPE')
def check_units(m):
 ensure(type(m['units']) is list and len(m['units'])==2,'UNIT_COUNT')
 ensure([u['id'] for u in m['units']]==['A','B'],'UNIT_IDENTITY')
 ensure(F(m['profile']['body_m'])==F('.7'),'BODY_PROFILE')
def seat_binding(u,seat,ops):
 p=u['dining_module_placement'];module=p['module'];fid=p['id_map'][seat['fixture_id']]
 ensure(digest(module)==p['module_hash'],'MODULE_HASH')
 ensure(len([o for o in ops if o['fixture_id']==fid])==1,'OPERATION_UNIQUE')
 op=next(o for o in ops if o['fixture_id']==fid);transfer=seat['rise_transfer']
 ensure(transfer['human_transfer_and_support_profile_validated'] is False,'UNEXPECTED_APPROVAL')
 ensure(transfer['other_seats_remain_occupied'] is True,'OTHER_OCCUPIED_PROFILE')
 ensure(F(transfer['source_body_m'])==F('.7'),'BODY_PROFILE')
 ensure(op['source_module_hash']==p['module_hash'],'OPERATION_MODULE')
 ensure(placed(seat['closed_rect'],p['transform'])==list(rect(u['fixtures'][fid])),'FIXTURE_SOURCE')
 for key,source in [('closed_rect',seat['closed_rect']),('open_rect',seat['pulled_rect']),('occupied_body',seat['occupied_body'])]:
  ensure(placed(source,p['transform'])==list(rect(op[key])),'OPERATION_STATE_BINDING')
 M=p['transform']['matrix'];delta=list(map(F,seat['translation']))
 ensure(list(map(F,op['translation']))==[sum(F(M[i][j])*delta[j] for j in (0,1)) for i in (0,1)],'PULL_VECTOR')
 aid='dining_'+seat['id'][5:];standing=placed(transfer['standing_body'],p['transform'])
 ensure(standing==list(rect(u['activities'][aid])),'STANDING_ACTIVITY')
 end=[str((standing[0]+standing[2])/2),str((standing[1]+standing[3])/2)]
 ensure([F(v) for v in op['egress_route'][-1]]==list(map(F,end)),'EGRESS_STANDING')
 return fid,aid,end,op
def scenario_fixture_obstacles(u,ops,fid):
 ensure(len(ops)==4 and len({o['fixture_id'] for o in ops})==4,'FOUR_UNIQUE_CHAIRS')
 ensure(fid in {o['fixture_id'] for o in ops},'SELECTED_CHAIR')
 # Arrival actor is not already seated. Only own chair is pulled and static.
 fx=[v for k,v in u['fixtures'].items() if k!=fid and not u['fixture_metadata'][k].get('walkable')]
 own=next(o for o in ops if o['fixture_id']==fid)
 others=[o['occupied_body'] for o in ops if o['fixture_id']!=fid]
 return fx+[own['open_rect']]+others
def assess(bundle,save=lambda out:None):
 strict_json(bundle);pin=digest(bundle);m=bundle['packet']['world_model'];mh=digest(m)
 ensure(mh==bundle['model_digest'],'MODEL_DIGEST');check_units(m)
 ensure(bundle['reports']['physical']['model_hash']==mh,'PHYSICAL_MODEL')
 for k,r in bundle['reports'].items():ensure(digest(r)==bundle['report_digests'][k],'REPORT_DIGEST')
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration')]
 from producer_provenance import snapshot,require_unchanged
 paths=['app/local_integration/dining_arrival_episode_study.py','app/local_integration/current_programme_evaluator.py','app/local_integration/source_guest_route_evaluator.py','app/local_integration/kitchen_guest_review.py']
 snap=snapshot(ROOT,paths);audit=source_audit()
 import construction_replay127
 from geometry114 import route,cells
 from public_program_audit118 import covered
 for fn,name in [(route,'fast_route120.py'),(cells,'fast_cells120.py'),(covered,'public_program_audit118.py'),(construction_replay127.verify,'construction_replay127.py')]:
  ensure(pathlib.Path(inspect.getsourcefile(fn)).resolve()==(ENGINE/name).resolve(),'IMPORT_SOURCE')
 replay=construction_replay127.verify(m,bundle['context']);ensure(replay['verified'] is True and replay['model_hash']==mh,'REPLAY')
 cat=json.loads((ENGINE/'fixture_catalog114.json').read_text());ensure(digest(cat)==m['fixture_catalog_hash'],'CATALOG_HASH')
 for fn,name in [(placed,'current_programme_evaluator.py'),(inventory,'current_programme_evaluator.py'),(route_check,'source_guest_route_evaluator.py')]:
  ensure(pathlib.Path(inspect.getsourcefile(fn)).resolve()==(ROOT/'app/local_integration'/name).resolve(),'INTEGRATION_IMPORT_SOURCE')
 inventory(m,lookup('PROGRAM_2BED_V1'),cat)
 ensure(digest(bundle)==pin,'INPUT_MUTATION')
 out={'schema':'DINING_EIGHT_ARRIVAL_EPISODE_STUDY_V1','state':'UNKNOWN','model_digest':mh,'input_digest':pin,
      'historical_physical_digest':bundle['report_digests']['physical'],'historical_physical_status':bundle['reports']['physical']['status'],
      'replay_digest':digest(replay),'source_snapshot':snap,'rows':[],'completed':False,'integrity_verified':False,
      'scenario':'Selected chair pulled and static; other three chairs closed and occupied; living occupied; actual kitchen work and six motions; open door panels. Not all simultaneous scenarios.',
      'phase_coverage':{'arrival':'NEW_PER_INSTANCE_ROUTE_PROBE','seated_pull_side_exit':'SOURCE_PHASE_DEFINITIONS_PRESENT_NOT_REEVALUATED_NO_NEW_PHASE_PASS','vertical_transfer':'MISSING_VALIDATED_PROFILE','end_to_end_episode':'NOT_VERIFIED'},
      'scope':'Historical model, not fresh current input execution. No geometry edits. No source profile approval or architectural admission.',
      **{k:False for k in AUTH}}
 save(out)
 try:
  for u in m['units']:
   uid=u['id'];p=u['dining_module_placement'];seats=p['module']['seating']['instances']
   ensure(len(seats)==4 and len({s['fixture_id'] for s in seats})==4,'SOURCE_SEATS')
   ops=[o for o in m['operations']['dining_chairs'] if o['unit']==uid]
   bindings={s['id']:seat_binding(u,s,ops) for s in seats}
   ensure(len(ops)==4 and len({o['fixture_id'] for o in ops})==4,'FOUR_UNIQUE_CHAIRS')
   ko=[o for o in m['operations']['kitchen'] if o['unit']==uid];ensure(len(ko)==1 and len(ko[0]['motion_envelopes'])==6,'KITCHEN_STATES');ko=ko[0]
   parts=[q for role in ('living','entry_circulation','dining','kitchen') for q in u['rooms'].get(role,[])]
   for role in ('bath','kitchen'):parts+=m['module_aprons'][uid+'.'+role]
   parts=cells(parts,[]);owner=u['ownership'];qs=list(map(rect,owner))
   box=list(map(str,[min(q[0] for q in qs),min(q[1] for q in qs),max(q[2] for q in qs),max(q[3] for q in qs)]))
   outside=cells([box],parts)+cells([box],owner)
   common=list(m['walls'].values())+[o['open_panel'] for o in m['operations']['doors']]+outside
   common += [u['activities']['kitchen_work']]+ko['motion_envelopes']+[z['actor_rect'] for z in ko['workstations']]
   common += [s['occupied_body'] for s in u['public_program']['capacity']['living_seats']]
   common += [q for role,qs in u['rooms'].items() if role.startswith('bed') or role=='private_circulation' for q in qs]
   for seat in seats:
    row={'unit':uid,'seat_id':seat['id'],'state':'STARTED','body_m':'7/10','other_occupied_seats':3,'human_transfer_validated':False}
    out['rows'].append(row);save(out)
    try:
     fid,aid,end,op=bindings[seat['id']];obs=common+scenario_fixture_obstacles(u,ops,fid)
     row.update(fixture_id=fid,activity_id=aid,module_digest=p['module_hash'],operation_digest=digest(op),floor_digest=digest(parts),ownership_digest=digest(owner),obstacle_digest=digest(obs),endpoint_digest=digest(end))
     path,reason=route(u['entry_point'],end,box,obs,body='.7')
     row.update(state='NO_WITNESS_IN_THIS_SCENARIO',router_reason=reason,path_digest=digest(path))
     if path:
      count=route_check(path,u['entry_point'],end,F('.7'),parts,obs)
      for band in sweeps(path,F('.7')):ensure(covered(band,list(map(rect,owner))),'OWNER_COVERAGE')
      row.update(state='PASS_PLANAR_ARRIVAL_ONLY',segments=count,length_m=str(sum(abs(F(a[0])-F(b[0]))+abs(F(a[1])-F(b[1])) for a,b in zip(path,path[1:]))))
     ensure(digest(bundle)==pin,'INPUT_MUTATION');require_unchanged(ROOT,snap)
    except Exception as ex:row.update(state='EVALUATOR_OR_BINDING_ERROR',error_type=type(ex).__name__,error_code=str(ex)[:120])
    save(out)
  out['visited_all_rows']=len(out['rows'])==8
  out['completed']=out['visited_all_rows'] and all(r['state'] in ('PASS_PLANAR_ARRIVAL_ONLY','NO_WITNESS_IN_THIS_SCENARIO') for r in out['rows'])
 except Exception as ex:out.update(error_type=type(ex).__name__,error_code=str(ex)[:120])
 finally:
  try:ensure(digest(bundle)==pin,'INPUT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SOURCE_CHANGED');out['integrity_verified']=True
  except Exception as ex:out.update(integrity_verified=False,integrity_error=type(ex).__name__)
  out['counts']={s:sum(r['state']==s for r in out['rows']) for s in sorted({r['state'] for r in out['rows']})};save(out)
 return out
if __name__=='__main__':
 source=pathlib.Path(sys.argv[1]);target=pathlib.Path(sys.argv[2])
 def save(out):
  tmp=target.with_suffix('.tmp');tmp.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False));tmp.replace(target)
 assess(json.loads(source.read_bytes()),save)
