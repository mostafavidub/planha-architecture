"""Independent exact one-unit ownership/access check; no quality admission."""
import copy
from fractions import Fraction as F
from single_model_p15 import digest,require,core,RAW,FAMILY,AUTH
from checker114 import rect,intersects,covered,sweeps
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
  domains=owner+[rect(c['stair']),rect(c['lift']),*[rect(q)for q in c['lobby']],*ports.values()]
  panels=[rect(o['open_panel'])for o in m['operations']['doors']]
  routes=[]
  for source in('stair','lift'):
   path=m['common_routes'][source+'_A'];a,b,C,d=rect(c[source]);cy=(b+d)/2
   start=[C-F('.4'),cy]if source=='stair'else[a+F('.4'),cy]
   need([F(x)for x in path[0]]==start and [F(x)for x in path[-1]]==target,'COMMON_ROUTE_ENDPOINT')
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
  evidence={'unit_ids':['A'],'common_routes':routes,'clear_internal_routes':sorted(clear),
            'ownership_digest':digest(u['ownership']),'core_digest':digest(c),'fixture_count':len(fixtures),
            'scope':'Necessary single-unit ownership and entry access only; not every activity, quality, privacy, or legal/technical approval'}
 except (KeyError,TypeError,ValueError,IndexError)as ex:
  errors.append({'code':str(ex)if type(ex)is ValueError else 'MALFORMED_MODEL','type':type(ex).__name__})
 require(digest(m)==before,'MODEL_MUTATED')
 return {'schema':'SINGLE_UNIT_OWNERSHIP_ACCESS_P15_V1','model_digest':before,
  'state':'FAIL'if errors else'PASS_SCOPED_OWNERSHIP_ACCESS','errors':errors,'evidence':evidence,
  'four_current_state':'NOT_EVALUATED','qualified':False,'accepted':False,'display_allowed':False,'delivery_allowed':False}
