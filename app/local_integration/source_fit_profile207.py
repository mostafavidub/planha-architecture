"""Source-bound limited fit/reservation study, not a physical or quality gate.
Bath apron vs dining is necessary for the selected typed-public-floor contract.
Kitchen motion reservations are the declared conservative guest scenario only.
"""
import copy,hashlib,inspect,json,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path.insert(0,str(ENGINE))
from contract114 import S,digest
from core_wall_audit118 import q,hit,covered,sweep
PINS={"search114.py":"65e0f278c9f9ef480388d3ea8056161c0a938a36","bathroom_module117.py":"db08bc7558db9be37ec8ac10839b1173d56555e6","kitchen_module117.py":"8ec837d51e724076d8b479763b132756137de61b","public_witness118.py":"36f49057da712f29953bbc940a0dd8e9285ee64b","typed_public_access120.py":"7c1272549e8036ba642d46f52a50810bcb33951b","final_public_floor120.py":"e91c70d8c308240e2cb7e7784634cecfb036240b","bedroom_module116.py":"289b23f25bafaa05281015b521affad5ab5a415d","twin_module118.py":"0da5c7b24a614d22f7ab9f9a4d2d68bcdb6ede15","place_bathroom117.py":"982bbb6dc584641b1a4894751e0f13e252da10ea","place_kitchen117.py":"8d4048d922f8c1052028e0c2e3172f2b8e75c3ce"}
def need(ok,code):
 if not ok:raise ValueError(code)
def source_check():
 for name,expected in PINS.items():
  data=(ENGINE/name).read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  need(actual==expected,'SOURCE_BLOB_MISMATCH')
 import bathroom_module117,kitchen_module117
 for m in (bathroom_module117,kitchen_module117):
  need(Path(inspect.getsourcefile(m.build)).resolve()==ENGINE/(m.__name__+'.py'),'ACTUAL_MODULE_PATH')
def motion_rectangles(module):
 need(module['schema']=='KITCHEN_MODULE117','KITCHEN_SCHEMA')
 ops=module['operations']['kitchen'];need(len(ops)==1,'KITCHEN_OP_INVENTORY');op=ops[0]
 need(op['profile']=='REFERENCE113_ESSENTIAL_KITCHEN_V1'and op['assumptions']['scope_hypothetical']is True,'KITCHEN_SOURCE_PROFILE')
 need(F(op['assumptions']['body_m'])==F('.7')and F(op['fridge']['body_m'])==F('.7'),'SOURCE_BODY')
 need(set(op['drawers'])=={'sink','prep'},'DRAWER_INVENTORY')
 out=[]
 for d in op['drawers'].values():
  a,b=q(d['closed_tray']),q(d['open_tray'])
  need(a[2]-a[0]==b[2]-b[0]and a[3]-a[1]==b[3]-b[1]and(a[0]==b[0]or a[1]==b[1]),'RIGID_DRAWER_SWEEP')
  out.append([min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])])
  a,b=map(lambda p:tuple(map(F,p)),(d['closed_actor'],d['open_actor']))
  need(a[0]==b[0]or a[1]==b[1],'AXIS_ALIGNED_DRAWER_ACTOR')
  out.append([min(a[0],b[0])-F('.35'),min(a[1],b[1])-F('.35'),max(a[0],b[0])+F('.35'),max(a[1],b[1])+F('.35')])
 fr=op['fridge'];x,y=map(F,fr['hinge']);r=F(fr['leaf_radius_m'])+F(fr['leaf_half_thickness_m'])
 out.append([x-r,y-r,x+r,y+r])
 a,b=map(lambda p:tuple(map(F,p)),(fr['closed_actor'],fr['open_actor']))
 out.append([min(a[0],b[0])-F('.35'),min(a[1],b[1])-F('.35'),max(a[0],b[0])+F('.35'),max(a[1],b[1])+F('.35')])
 return [list(map(S,r))for r in out]
_CACHE=None
def profiles():
 global _CACHE
 source_check()
 if _CACHE is None:
  import bathroom_module117,kitchen_module117
  bath=bathroom_module117.build('3.15','2.25');bathmax=bathroom_module117.build('4.3','3.1')
  kitchen=kitchen_module117.build('2.35','3.05');kitchenmax=kitchen_module117.build('3.6','4.2')
  apron=bath['unit']['rooms']['public_access'];motions=motion_rectangles(kitchen)
  need(digest(apron)==digest(bathmax['unit']['rooms']['public_access']),'BATH_APRON_DIMENSION_INVARIANCE')
  need(digest(motions)==digest(motion_rectangles(kitchenmax)),'MOTION_DIMENSION_INVARIANCE')
  _CACHE={'schema':'SOURCE_FIT_PROFILE207_V1','bath_apron':apron,'kitchen_motions':motions,'body_m':'.7',
   'source_module_hashes':{'bath_min':digest(bath),'bath_max':digest(bathmax),'kitchen_min':digest(kitchen),'kitchen_max':digest(kitchenmax)},
   'source_blob_pins':copy.deepcopy(PINS),'invariance_scope':'Endpoint checks plus source formula inspection, not enumeration of all dimensions',
   'bath_scope':'Necessary for selected bath public_access living/entry floor; not a universal owner room-role rule',
   'motion_scope':'Six source conservative envelopes for guest scenario, not minimal motion or ergonomic approval',
   'accepted':False,'qualified':False}
 return copy.deepcopy(_CACHE)
def guest_bands(path):
 need(type(path)is list and len(path)==5 and all(type(v)is list and len(v)==2 for v in path),'GUEST_PATH_SHAPE')
 pts=[[F(str(v))for v in p]for p in path]
 need(all(a[0]==b[0]or a[1]==b[1]for a,b in zip(pts,pts[1:])),'GUEST_PATH_ORTHOGONAL')
 return list(sweep([[str(v)for v in p]for p in pts],F('.7')))
def reservation_errors(aprons,dining,motions,paths,owner):
 necessary=[];conservative=[]
 for r in aprons:
  if not covered(r,owner):necessary.append('BATH_APRON_OUTSIDE_OWNERSHIP')
  if hit(r,dining):necessary.append('BATH_APRON_IN_DINING_EXCLUDED_PUBLIC_ROLE')
 need(set(paths)=={'sofa1_use','dining_east'},'DECLARED_GUEST_TERMINALS')
 for path in paths.values():
  for band in guest_bands(path):
   if not covered(band,owner):necessary.append('GUEST_BODY_OUTSIDE_OWNERSHIP')
   if any(hit(band,r)for r in motions):conservative.append('GUEST_BODY_SOURCE_MOTION_INTRUSION')
 return sorted(set(necessary)),sorted(set(conservative))
def translated(rect,x,y):
 a,b,c,d=q(rect);return(a+x,b+y,c+x,d+y)
def source_fit(proposal,core):
 """Pre-construction exact check of added constraints, not the whole solver proof."""
 p=profiles();rs=proposal['rectangles'];bath=q(rs['bath']);kit=q(rs['kitchen']);dining=q(rs['dining'])
 need(type(proposal.get('bedrooms'))is int and proposal['bedrooms']==2 and digest(proposal.get('sleep_roles'))==digest(['double','twin']),'PROGRAM_SCOPE')
 import bathroom_module117,kitchen_module117,bedroom_module116,twin_module118
 modules={'bath':bathroom_module117.build(S(bath[2]-bath[0]),S(bath[3]-bath[1])),
 'kitchen':kitchen_module117.build(S(kit[2]-kit[0]),S(kit[3]-kit[1]))}
 for name,builder in (('bed1',bedroom_module116.build),('bed2',twin_module118.build)):
  a,b,c,d=q(rs[name]);modules[name]=builder(S(c-a),S(d-b))
 need(digest(modules['bath']['unit']['rooms']['public_access'])==digest(p['bath_apron']),'ACTUAL_BATH_APRON_PROFILE')
 need(digest(motion_rectangles(modules['kitchen']))==digest(p['kitchen_motions']),'ACTUAL_KITCHEN_MOTION_PROFILE')
 aprons=[translated(r,bath[0],bath[1])for r in p['bath_apron']]
 motions=[translated(r,kit[0],kit[1])for r in p['kitchen_motions']]
 owner=[q(r)for r in core.get('unit_ownership',{}).get('A',[core['units']['A']])]
 necessary,conservative=reservation_errors(aprons,dining,motions,{n:proposal['network_paths'][n]for n in ('sofa1_use','dining_east')},owner)
 return {'schema':'PRECONSTRUCTION_SOURCE_FIT207_V1','proposal_digest':digest(proposal),'core_digest':digest(core),'profile_digest':digest(p),
 'necessary_fit':not necessary,'conservative_scenario_fit':not conservative,'state':'PASS_LIMITED_CONSTRAINTS'if not necessary and not conservative else'REJECT_SELECTED_CONSTRAINTS_NOT_GLOBAL_INFEASIBILITY',
 'necessary_errors':sorted(set(necessary)),'conservative_errors':sorted(set(conservative)),'source_module_hashes':{k:digest(v)for k,v in modules.items()},
 'remaining':['ACTUAL_TYPED_PUBLIC_FLOOR_AFTER_INSTALLATION','WHOLE_NEIGHBOR_OPERATIONS','ALL_REQUIRED_ROUTES','QUALITY_AND_HUMAN_PROFILE'],
 'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}

def installation_expectations(proposals,L):
 """Rebuild only wet/kitchen installed subsets with actual source installers."""
 import bathroom_module117,kitchen_module117,place_bathroom117,place_kitchen117
 expected={'module_aprons':{},'operations':{},'units':[],'walls':{},'wall_hosts':{},'source_wall_hosts':{},'openings':[]}
 for uid in ('A','B'):
  u={'id':uid,'rooms':{},'fixtures':{},'fixture_metadata':{},'activities':{}};expected['units'].append(u)
  for role,builder,installer in (('bath',bathroom_module117.build,place_bathroom117.install),('kitchen',kitchen_module117.build,place_kitchen117.install)):
   need(Path(inspect.getsourcefile(installer)).resolve()==ENGINE/('place_bathroom117.py'if role=='bath'else'place_kitchen117.py'),'INSTALLER_PATH')
   rect=proposals[uid]['rectangles'][role];a,b,c,d=q(rect)
   module=builder(S(c-a),S(d-b))
   installer(module,expected,u,uid,rect,L)
 return expected
def verify_installed_subset(model,expected):
 errors=[];checks=0
 for key,value in expected['module_aprons'].items():
  checks+=1
  if digest(model.get('module_aprons',{}).get(key))!=digest(value):errors.append('INSTALLED_APRON_SOURCE_MISMATCH')
 for kind in ('kitchen','doors'):
  for op in expected['operations'][kind]:
   identity=('unit',op['unit'])if kind=='kitchen'else('opening_id',op['opening_id'])
   actual=[v for v in model.get('operations',{}).get(kind,[])if v.get(identity[0])==identity[1]]
   checks+=1
   if len(actual)!=1 or digest(actual[0])!=digest(op):errors.append('INSTALLED_OPERATION_SOURCE_MISMATCH')
 for eu in expected['units']:
  us=[u for u in model['units']if u['id']==eu['id']];need(len(us)==1,'INSTALLED_UNIT_NAMESPACE')
  for field in ('fixtures','activities','fixture_metadata'):
   for key,value in eu[field].items():
    checks+=1
    if digest(us[0].get(field,{}).get(key))!=digest(value):errors.append('INSTALLED_SOURCE_RECORD_MISMATCH')
 return {'schema':'WET_KITCHEN_INSTALLATION207_V1','state':'FAIL_SOURCE_BINDING'if errors else'PASS_SOURCE_SUBSET_ONLY',
 'errors':sorted(set(errors)),'pending':[],'checked_record_count':checks,'model_digest':digest(model),'expected_subset_digest':digest(expected),
 'remaining':['OTHER_MODULES','WHOLE_FLOOR_ACCESS','WHOLE_NEIGHBOR_PHYSICS','HUMAN_PROFILE_QUALITY'],'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
def installation_negatives(model,expected):
 pin=digest(model);rows=[]
 for name in ('REMOVE_APRON','MOVE_DRAWER_ACTOR','CHANGE_FRIDGE_RADIUS','CHANGE_FIXTURE_DIMENSION'):
  mutated=copy.deepcopy(model)
  if name=='REMOVE_APRON':mutated['module_aprons']['A.bath']=[]
  elif name=='MOVE_DRAWER_ACTOR':
   op=next(v for v in mutated['operations']['kitchen']if v['unit']=='A');op['drawers']['sink']['open_actor'][0]=S(F(op['drawers']['sink']['open_actor'][0])+1)
  elif name=='CHANGE_FRIDGE_RADIUS':
   op=next(v for v in mutated['operations']['kitchen']if v['unit']=='A');op['fridge']['leaf_radius_m']='.1'
  else:
   u=next(u for u in mutated['units']if u['id']=='A');u['fixtures']['fridge'][2]=S(F(u['fixtures']['fridge'][2])+F('.1'))
  r=verify_installed_subset(mutated,expected);rows.append({'mutation':name,'detected':r['state']=='FAIL_SOURCE_BINDING','error_codes':r['errors'],'mutated_model_digest':digest(mutated)})
 need(digest(model)==pin,'NEGATIVE_MUTATED_ORIGINAL')
 return {'schema':'INSTALLATION_DETACHED_NEGATIVES207_V1','original_model_digest':pin,'original_unchanged':True,'all_detected':all(r['detected']for r in rows),'rows':rows,
 'scope':'Direct source-subset correspondence failures, not complete neighbor physics or architectural infeasibility','accepted':False}
