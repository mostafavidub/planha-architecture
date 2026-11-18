"""ENGINEERING_OPERATIONALIZATION362, not recovered missing common definitions.
Finite declared source-profile intrinsic/use eligibility, no Q04/Q11-final/Q12
or all-parent dependency. Pinned stored-artifact analysis, NEVER live authority.
"""
import builtins,hashlib,json,types,time
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent.parent/'semantic_rules357'
REGISTRY=(
 ('B01','H01','input_exact_domain'),('B02','H02/H03','containment_all_entities valid_exact_regions'),
 ('B03','H04/H06','partition_ledger'),('B04','H05','unit_independence'),
 ('B05','H07','bath_nonprivate_access'),('B06','H08','body_route_sweeps'),
 ('B07','H09','wall_network'),('B08','H10','opening_hosts actual_opening_geometry'),
 ('B09','H11','door_operation closet_operation'),('B10','H12','fixture_inventory_use'),
 ('B11','H13/Q01','program_functional_roles zero_laundry'),('B12','H15','core_concept'),
 ('B13','H17','kitchen_essential_operation bath_service_operation'),('B14','Q05.VISIBILITY_ONLY','privacy_scenarios'),
 ('B15','Q06','guest_living_route guest_dining_route'),('B16','Q07.ESSENTIAL_USE','serving_route'),
 ('B17','Q10.ARRIVAL_USE','core_concept'),('B18','H19',''))
EXCLUDED_DEPENDENCIES=('Q04','Q11_FINAL','Q12','ALL_12_PARENT_PASS','long_corridor_necessity')

def _loader():
 import importlib
 from adapters381 import load
 pins=json.loads((HERE/'eligibility_intrinsic365_pins.json').read_text())
 return load,pins

def _inventory(items,key):
 ids=[key(x) for x in items]
 if not ids or len(ids)!=len(set(ids)):raise ValueError('EMPTY_OR_DUPLICATE_INVENTORY')
 return set(ids)

def _row(rs,k):
 r=rs[k];w=r['evidence']['witness']
 if type(w)is not dict:raise ValueError('WITNESS_REQUIRED:'+k)
 if w.get('errors'):return 'FAIL',w
 if r['status']!='PASS_LIMITED' or w.get('pending'):return 'UNKNOWN',w
 return 'PASS',w

def _reduce(rows):
 if len(rows)!=18 or {r['id']for r in rows}!={r[0]for r in REGISTRY}:return 'UNKNOWN'
 return 'FAIL' if any(r['verdict']=='FAIL'for r in rows)else 'PASS' if all(r['verdict']=='PASS'for r in rows)else 'UNKNOWN'

def evaluate(record,new_result,seconds=30,source_profile='SOURCE_BALANCED365'):
 out={'schema':'ENGINEERING_OPERATIONALIZATION362_INTRINSIC_ELIGIBILITY','verdict':'UNKNOWN','eligible':False,'live_authority':False,'repair_authority':False,'delivery_allowed':False,'parent_complete':False,'new_fresh_execution':False,'rows':[],'missing':[],'excluded_dependencies':list(EXCLUDED_DEPENDENCIES),'scope':'CURRENT_TWO_UNIT_THREE_BEDROOM_SOURCE_PROFILE; STORED_ARTIFACT; OPEN_TRANSIT_AND_DECLARED_SOURCE_OPERATION_SCENARIOS; NOT_GLOBAL_OPTIMUM_OR_TECHNICAL_CORE'}
 try:
  if source_profile!='SOURCE_BALANCED365':raise ValueError('UNREGISTERED_SOURCE_PROFILE')
  if type(seconds)not in(int,float)or not 0<seconds<=30:raise ValueError('BOUNDED_SECONDS')
  deadline=time.monotonic()+seconds;load,pins=_loader();common=load('common');digest=common.digest
  contract=(HERE.parents[1]/'recovered233_rendered/sections.json').read_bytes()
  if hashlib.sha256(contract).hexdigest()!='98e39063ee7ba733335c450c7fb661b9939762873f19c788d1b0764cb2daf0e3':raise ValueError('RECOVERED_CONTRACT_SOURCE_CHANGED')
  before=digest([record,new_result]);view=load('group_readsets365_v2').build(record,new_result,seconds=min(seconds,8),source_profile='SOURCE_BALANCED365')
  m=view['envelope']['packet']['world_model'];raw=view['result']['raw_fresh_report'];rs=common.rows(m,raw)
  def remain():
   r=deadline-time.monotonic()
   if r<=0:raise ValueError('ELIGIBILITY_DEADLINE')
   return min(r,8)
  access=load('intrinsic_access365').evaluate(m,raw,profile='SOURCE_BALANCED365',seconds=remain())
  opening=load('closure_openings').evaluate(m,raw)
  guest=load('guest_closure365').evaluate(view['envelope'],view['result'],view['groups'],seconds=remain())
  kitchen=load('kitchen_closure365').evaluate(view['envelope'],view['result'],view['groups'],seconds=remain())
  try:bundle=load('closure_room_program365').bundle_inventory(m,rs);bundle_error=None
  except (ValueError,TypeError,KeyError,IndexError,StopIteration)as e:bundle=[];bundle_error=str(e)
  unitids=_inventory(m['units'],lambda u:u['id']);body=F(m['profile']['body_m'])
  if len(unitids)!=2 or m['program']['sleep_roles']!=['double','twin','twin']or body!=F('.7'):raise ValueError('UNREGISTERED_SOURCE_PROGRAM_PROFILE')
  def require(ok,why):
   if not ok:raise ValueError(why)
  for bid,source,keys in REGISTRY:
   remain();row={'id':bid,'source_section':source,'source_requirement_ids':keys.split(),'verdict':'UNKNOWN','missing':[],'row_digests':{k:digest(rs[k])for k in keys.split()}}
   try:
    statuses=[_row(rs,k)[0]for k in keys.split()]
    if 'FAIL'in statuses:row['verdict']='FAIL';row['missing']=['SOURCE_INTRINSIC_COUNTERPROOF'];out['rows'].append(row);continue
    require(all(x=='PASS'for x in statuses),'SOURCE_PENDING_OR_UNEVALUATED')
    if bid=='B01':
     require(list(map(F,_row(rs,'input_exact_domain')[1]['exact']))==list(map(F,m['inputs'])),'INPUT_READSET')
     W,L,n=map(F,m['inputs']);require(5<=W<=45 and 5<=L<=45 and n==2,'OWNER_INPUT_DOMAIN')
     require(list(map(F,m['inputs']))==[F(view['envelope']['raw'][k]) for k in ('W','L','n')],'REQUEST_MODEL_INPUTS')
    elif bid=='B02':
     w=_row(rs,'valid_exact_regions')[1];require(w.get('representation')=='Exact unions of positive rectangles; holes are not replaced by a bbox'and w.get('positive_rectangles',0)>0,'EXACT_UNION_REPRESENTATION')
     require(_row(rs,'containment_all_entities')[1]['checked_entities']>0,'ENTITY_COVERAGE')
    elif bid=='B03':
     w=_row(rs,'partition_ledger')[1];require(w.get('model_hash')==digest(m)and w.get('exact_role_cells',0)>0,'PARTITION_MODEL')
     _inventory(w['groups'],lambda g:g['role'])
    elif bid in ('B04','B05','B12','B17'):
     minima=access.get('minima',{});require(set(minima)==unitids,'ACCESS_UNIT_COVERAGE')
     key='H07'if bid=='B05'else'H05_H15_Q10_ARRIVAL'
     require(all(minima[u][key]['verdict']=='PASS_SCOPED_INTRINSIC'for u in unitids),'PRIVATE_DELETION_OR_ARRIVAL_PATH_UNPROVEN')
    elif bid=='B06':
     w=_row(rs,'body_route_sweeps')[1];actual=_inventory(w['routes'],lambda r:(r['unit'],r['route']))
     expected={(u['id'],k)for u in m['units']for k in u['routes']};require(actual==expected,'SOURCE_ROUTE_INVENTORY')
     require(all(F(r['body_m'])==body for r in w['routes']),'BODY_PROFILE')
     require(bundle_error is None,'SOURCE_REQUIRED_BED_ACTIVITY_INVENTORY:'+str(bundle_error))
    elif bid=='B07':
     w=_row(rs,'wall_network')[1];require(w.get('physical_union_verified')is True and len(w['host_components'])==1,'WALL_UNION_AND_CONNECTIVITY')
    elif bid in ('B08','B09'):
     require(opening.get('scope_complete')is True,'OPENING_SCOPE:'+str(opening.get('missing')))
    elif bid in ('B10','B11'):
     require(bundle_error is None,'SOURCE_BUNDLE:'+str(bundle_error));require({x['unit']for x in bundle}==unitids,'BUNDLE_UNIT_COVERAGE')
     if bid=='B11':require(_row(rs,'zero_laundry')[1]['forbidden_entities']==[],'LAUNDRY_PRESENT')
    elif bid=='B13':
     w=_row(rs,'kitchen_essential_operation')[1];require(_inventory(w['actual_operation_ids'],lambda x:x)==unitids,'KITCHEN_OPERATIONS')
     require(kitchen['verdict']=='PASS_SCOPED_ESSENTIAL_KITCHEN_RELATIONS','ESSENTIAL_SERVICE_OPERATIONS')
    elif bid=='B14':
     w=_row(rs,'privacy_scenarios')[1];require(w['privacy']['errors']==[]and w['privacy']['pending']==[],'VISIBILITY_PENDING')
     targets=w['privacy']['evidence']['targets'];covered={(x['unit'],x['room'])for x in targets};expected={(u['id'],k)for u in m['units']for k in u['rooms']if k.startswith('bed')}
     require(expected<=covered,'PRIVATE_VISIBILITY_TARGET_INVENTORY');require(bool(w.get('state_coverage')),'VISIBILITY_STATE_COVERAGE')
    elif bid=='B15':require(guest['verdict']=='PASS_SCOPED_FOUR_SOURCE_GUEST_RELATIONS','GUEST_SCENARIOS')
    elif bid=='B16':require(kitchen['verdict']=='PASS_SCOPED_ESSENTIAL_KITCHEN_RELATIONS','KITCHEN_SERVICE_PATHS')
    elif bid=='B18':require(view['groups']['model_hash']==digest(m),'PROVENANCE_GATE_MODEL')
    row['verdict']='PASS'
   except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError)as e:row['missing']=[str(e)]
   out['rows'].append(row)
  require(digest([record,new_result])==before,'INPUT_MUTATION')
  for file,sha in pins['files'].items():require(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==sha,'SOURCE_CHANGED:'+file)
  out['verdict']=_reduce(out['rows']);out['eligible']=out['verdict']=='PASS';out['missing']=[{'id':r['id'],'reasons':r['missing']}for r in out['rows']if r['verdict']!='PASS']
  out['evidence']={'record_digest':digest(record),'new_result_digest':digest(new_result),'model_digest':digest(m),'group_digest':digest(view['groups']),'component_digests':{k:digest(v)for k,v in [('access',access),('openings',opening),('guest',guest),('kitchen',kitchen)]},'source_pins_digest':digest(pins)}
 except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError,OverflowError,FileNotFoundError)as e:
  out['verdict']='UNKNOWN';out['eligible']=False;out['missing'].append({'id':'GATE','reasons':[str(e)]})
 return out
