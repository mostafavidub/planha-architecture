"""Executable interface contract for a restricted real three-bedroom macro.
No constructor/solver; snapshot extraction is not a new admitted whole plan.
"""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from private_binding121 import examine as private_binding
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def q(r):return tuple(F(str(x))for x in r)
def transform(p,r):
 M=p['transform']['matrix'];t=list(map(F,p['transform']['translation']));M=[[F(str(x))for x in row]for row in M]
 if len(M)!=2 or any(len(r)!=2 for r in M)or any(x not in(-1,0,1)for row in M for x in row)or any(sum(M[k][i]*M[k][j]for k in range(2))!=int(i==j)for i in range(2)for j in range(2)):raise ValueError('NON_D4_MODULE_PLACEMENT')
 x,y,X,Y=q(r);ps=[tuple(sum(M[i][j]*v[j]for j in range(2))+t[i]for i in range(2))for v in((x,y),(x,Y),(X,y),(X,Y))]
 return(min(v[0]for v in ps),min(v[1]for v in ps),max(v[0]for v in ps),max(v[1]for v in ps))
def inspect(model):
 r=private_binding(model);errors=list(r['errors']);pending=list(r['pending']);sources=[]
 try:
  if len(model.get('private_domains',[]))!=len(model['units']):pending.append('ONE_THREE_BED_DOMAIN_PER_UNIT_STUDY_ONLY')
  for u in model['units']:
   uid=u['id'];beds={k for k in u['rooms']if k.startswith('bed')}
   if beds!={'bed1','bed2','bed3'}:pending.append(uid+':EXACT_THREE_BEDROOM_STUDY_ONLY');continue
   ps=[p for p in model['module_placements']if p['unit_id']==uid and p['room_id']in beds]
   if {p['room_id']for p in ps}!=beds or len(ps)!=3:errors.append(uid+':SOURCE_ROOM_INVENTORY')
   for p in ps:
    s=p['module'];rid=p['room_id'];ids=p['id_map']
    if digest(s)!=p['module_hash']:errors.append(uid+':SOURCE_MODULE_HASH')
    if s['schema']not in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118'):pending.append(uid+':UNSUPPORTED_SLEEP_SOURCE');continue
    for key,rect in s['unit']['fixtures'].items():
     if q(u['fixtures'][ids[key]])!=transform(p,rect):errors.append(uid+':ACTUAL_SLEEP_FIXTURE_BINDING')
    for key,rect in s['walls'].items():
     if q(model['walls'][ids[key]])!=transform(p,rect):errors.append(uid+':ACTUAL_SLEEP_WALL_BINDING')
    sources.append({'unit':uid,'room':rid,'source_hash':p['module_hash'],'schema':s['schema']})
 except(KeyError,ValueError,TypeError,IndexError)as e:errors.append('MACRO_SCHEMA:'+str(e))
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_PRIVATE_MACRO_INTERFACE_ONLY','errors':sorted(set(errors)),'pending':sorted(set(pending)),'model_hash':digest(model),'source_rooms':sources,'private_topology':r,'accepted':False,'scope':'Fresh topology/boundary/ports/nonbed-route exclusion and source fixture/wall binding; not bed/closet operational completeness, all-scenario privacy, six-person dining/living/kitchen capacity, Q11 superiority or whole admission.'}

def bundle(model,unit):
 check=inspect(model)
 if check['errors']or check['pending']:return {'status':'NOT_EXPORTABLE_MACRO_INTERFACE','check':check}
 u=next(u for u in model['units']if u['id']==unit);d=next(d for d in model['private_domains']if d['unit']==unit)
 placements=[p for p in model['module_placements']if p['unit_id']==unit and p['room_id'].startswith('bed')]
 wallids={p['id_map'][k]for p in placements for k in p['module']['walls']}|{k for k in model['walls']if k.startswith(unit+'.private_hall.')}
 fixtureids={p['id_map'][k]for p in placements for k in p['module']['unit']['fixtures']}
 rooms={k:v for k,v in u['rooms'].items()if k.startswith('bed')or k=='private_circulation'}
 parts=[r for rs in rooms.values()for r in rs]+[model['walls'][k]for k in wallids]
 rs=list(map(q,parts));envelope=[str(min(r[0]for r in rs)),str(min(r[1]for r in rs)),str(max(r[2]for r in rs)),str(max(r[3]for r in rs))]
 result={'schema':'SOURCE_BOUND_PRIVATE_MACRO128_STUDY','status':'INTERFACE_WITNESS_NOT_WHOLE_PLAN','source_model_hash':digest(model),'unit':unit,'placements':placements,'rooms':rooms,'walls':{k:model['walls'][k]for k in sorted(wallids)},'fixtures':{k:u['fixtures'][k]for k in sorted(fixtureids)},'domain':d,'module_ports':[p for p in model['module_ports']if any(p['opening_id']==x['id_map'].get(o['id'])for x in placements for o in x['module']['openings'])],'envelope':envelope,'residual_policy':'Envelope is a placement bound, NOT all useful floor. Only exact supplied rooms/actual domain are claimed; all other leftover remains unprogrammed.','composition_contract':['Translate/rotate/reflect all source geometry/ports/paths/operations using one D4, never independent room scaling.','Reserve actual public interface and a body-clear connection to the common entry.','Every bath/kitchen/guest/service path stays out of private-domain interior.','After placement rerun real sources, body paths, door/closet operations, privacy, walls and Q11. Macro receipt cannot replace these checks.'],'accepted':False}
 result['bundle_hash']=digest(result);return result
