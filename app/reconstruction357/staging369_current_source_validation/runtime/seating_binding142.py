"""Independent raw-source reconstruction for compact D4 local/world geometry."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from contract114 import BODY,S,digest
from shared_geometry137 import rect,overlaps,local_polyline_clear
from local_routes142 import search
IDS=('sofa1','sofa2','armchair1','armchair2','armchair3','armchair4')
MARKER='SIDECAR_COMPACT_D4_GROUP142_LOCAL_WORLD_PENDING'
SPEC=((270,'0','0'),(0,'1.6','0'),(90,'0','2.3'),(90,'0','3.1'),(270,'2.7','1.6'),(270,'2.7','2.4'))
SHA='2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4'
def move_point(p,m,t):return tuple(sum(F(m[i][j])*F(p[j])for j in range(2))+F(t[i])for i in range(2))
def move_rect(q,m,t):
 a,b,c,d=map(F,q);ps=[move_point(p,m,t)for p in((a,b),(a,d),(c,b),(c,d))]
 return(min(v[0]for v in ps),min(v[1]for v in ps),max(v[0]for v in ps),max(v[1]for v in ps))
def source_records(p):
 if p.get('generation_method')!=MARKER:raise ValueError('D4_METHOD_BINDING')
 if any(k in p for k in('rooted_service_study','opposing_group_study')):raise ValueError('D4_UNRELATED_GROUP_OR_ROOT_CLAIM')
 raw=(Path(__file__).parent/'references/lr_option2_125x20_model.json').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SHA or BODY!=F('.7'):raise ValueError('IMMUTABLE_SOURCE_BODY')
 u=json.loads(raw)['units'][0];ox,oy=map(F,p['rectangles']['sofa1_use'][:2]);out={}
 rotations={0:((1,0),(0,1)),90:((0,-1),(1,0)),180:((-1,0),(0,-1)),270:((0,1),(-1,0))}
 for k,(ang,dx,dy)in zip(IDS,SPEC):
  key=k if k.startswith('sofa')else('armchair1'if k in('armchair1','armchair3')else'armchair2');fx=tuple(F(str(x))for x in u['fixtures'][key]);ac=tuple(F(str(x))for x in u['activities'][key+'_front']);reserve=ac if k.startswith('sofa')else(fx[0],ac[1],fx[2],ac[3]);use=(min(fx[0],reserve[0]),min(fx[1],reserve[1]),max(fx[2],reserve[2]),max(fx[3],reserve[3]));m=rotations[ang];r=move_rect(use,m,(0,0));t=(ox+F(dx)-r[0],oy+F(dy)-r[1]);sa=move_rect(ac,m,t)
  rec={'id':k,'source_key':key,'source_sha256':SHA,'matrix':m,'translation':t,'rotation':ang,'fixture':move_rect(fx,m,t),'source_activity':sa,'reserved_activity':move_rect(reserve,m,t),'use':move_rect(use,m,t),'target':((sa[0]+sa[2])/2,(sa[1]+sa[3])/2)}
  if json.loads(json.dumps(rec,default=S))!=p['compact_d4_sources142'][k]:raise ValueError('SOURCE_RECORD:'+k)
  usekey=k+'_use'if k.startswith('sofa')else'chair'+k[-1]+'_use'
  if tuple(map(F,p['rectangles'][usekey]))!=rec['use']:raise ValueError('SOURCE_USE:'+k)
  out[k]=rec
 if set(p['compact_d4_sources142'])!=set(IDS):raise ValueError('SIX_UNIQUE_SOURCE_IDS')
 w=(ox+F('1.6'),oy+F('1.6'),ox+F('2.3'),oy+F('2.3'))
 if tuple(map(F,p['shared_body_witness']))!=w:raise ValueError('SOURCE_WITNESS')
 return out,w

def obstacles(model,uid,target):
 unit=next(u for u in model['units']if u['id']==uid)
 return list(model['walls'].values())+[o['open_panel']for o in model.get('operations',{}).get('doors',[])]+[q for u in model['units']for q in u['fixtures'].values()]+[q for u in model['units']for k,q in u['activities'].items()if not(u['id']==uid and k==target)]+unit['rooms'].get('private_circulation',[])

def unit_geometry(model,uid,records,w,local_length,world=False):
 if F(model['profile']['body_m'])!=BODY or F(model['source_geometry_contract']['body_m'])!=BODY:raise ValueError('BODY_CHANGED')
 us=[u for u in model['units']if u['id']==uid]
 if len(us)!=1:raise ValueError('UNIQUE_UNIT')
 u=us[0];bm=((1,0),(0,1))if uid=='A'else((1,0),(0,-1));bt=(0,0)if uid=='A'else(0,local_length)
 def qmove(q):
  z=move_rect(q,bm,bt);return move_rect(z,((0,1),(1,0)),(0,0))if world else z
 def pmove(q):
  z=move_point(q,bm,bt);return(z[1],z[0])if world else z
 targets={};uses=[]
 for name,r in records.items():
  if rect(u['fixtures'][name])!=qmove(r['fixture'])or rect(u['activities'][name+'_front'])!=qmove(r['reserved_activity']):raise ValueError('ACTUAL_D4_GEOMETRY:'+uid+':'+name)
  target=pmove(r['target']);reserve=qmove(r['reserved_activity'])
  if target!=((reserve[0]+reserve[2])/2,(reserve[1]+reserve[3])/2)or tuple(map(F,u['route_targets'][name+'_front']))!=target:raise ValueError('SOURCE_TARGET:'+name)
  md=u['fixture_metadata'][name];ang=(90-r['rotation'])%180 if world else r['rotation']
  if md['kind']!=r['source_key']or md['rotation_deg']!=ang or md.get('walkable'):raise ValueError('FOOTPRINT_METADATA:'+name)
  if tuple(F(str(v))for v in md['source_size_m'])!=((F('2.2'),F('.9'))if name.startswith('sofa')else(F('.8'),F('.8'))):raise ValueError('SOURCE_SIZE_METADATA')
  targets[name]=target;uses.append(qmove(r['use']))
 group=(min(q[0]for q in uses),min(q[1]for q in uses),max(q[2]for q in uses),max(q[3]for q in uses));w=qmove(w)
 if any(overlaps(w,q)for q in uses)or any(overlaps(w,rect(q))for q in obstacles(model,uid,None)):raise ValueError('ADDITIONAL_WITNESS_BLOCKED')
 return group,w,targets

def evidence(packet,context):
 trace=context['construction_trace'];p=trace['proposal'];records,w=source_records(p)
 if packet['family']!='LEFT_RIGHT'or trace['family']!='LEFT_RIGHT':raise ValueError('LEFT_RIGHT_ONLY')
 for key,hashkey in [('local_model','local_model_hash'),('world_model','model_hash'),('core','core_hash')]:
  if digest(packet[key])!=trace[hashkey]:raise ValueError('FRESH_TRACE_HASH:'+key)
 if packet['core']['world_from_local']!={'matrix':[[0,1],[1,0]],'translation':['0','0']}:raise ValueError('WORLD_D4_CONTRACT')
 local=packet['local_model'];world=packet['world_model'];L=F(local['inputs'][1]);audits={}
 for model in(local,world):
  if sorted(u['id']for u in model['units'])!=['A','B']:raise ValueError('TWO_UNIQUE_UNITS')
 for uid in('A','B'):
  group,wit,targets=unit_geometry(local,uid,records,w,L);wg,ww,wt=unit_geometry(world,uid,records,w,L,True);start=((wit[0]+wit[2])/2,(wit[1]+wit[3])/2);paths={};lengths={}
  for name in IDS:
   route=search(start,targets[name],BODY,group,obstacles(local,uid,name+'_front'))
   if route['path']is None:raise ValueError('LOCAL_SOURCE_ROUTE:'+uid+':'+name)
   path=route['path'];wp=[(y,x)for x,y in path]
   if wp[-1]!=wt[name]or not local_polyline_clear(wp,BODY,wg,obstacles(world,uid,name+'_front')):raise ValueError('WORLD_SOURCE_SWEEP:'+uid+':'+name)
   paths[name]={'local':path,'world':wp};lengths[name]=S(route['length'])
  audits[uid]={'local_witness':wit,'world_witness':ww,'paths':paths,'lengths_m':lengths}
 return json.loads(json.dumps({'status':'PASS_SOURCE_D4_LOCAL_WORLD142','local_model_hash':digest(local),'world_model_hash':digest(world),'units':audits,'scope':'Compact alternative, not superseding larger living; no comfort or seated-transfer proof.'},default=S))
