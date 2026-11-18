"""Isometric kitchen module installation, with independent module recheck."""
from copy import deepcopy
from fractions import Fraction as F
from contract114 import S,digest
from checker114 import check_kitchen_module

def install(base,m,u,uid,clearrect,L):
 gate=check_kitchen_module(base)
 if gate['status']!='PASS_MODULE_SCOPED':raise ValueError('KITCHEN_MODULE_REJECT:'+str(gate['errors'])+' pending='+str(gate['pending']))
 a,b,c,d=map(lambda x:F(str(x)),clearrect);L=F(L);sy=-1 if uid=='B'else 1;z=deepcopy(base);prefix=uid+'.kitchen.'
 def pt(p):x,y=map(lambda v:F(str(v)),p);return[S(a+x),S(L-b-y if uid=='B'else b+y)]
 def rr(q):x,y,xx,yy=map(lambda v:F(str(v)),q);p=pt([x,y]);r=pt([xx,yy]);return[S(min(F(p[0]),F(r[0]))),S(min(F(p[1]),F(r[1]))),S(max(F(p[0]),F(r[0]))),S(max(F(p[1]),F(r[1])))]
 def vec(q):return[S(F(str(q[0]))),S(sy*F(str(q[1])))]
 wm={k:prefix+k for k in z['walls']};hm={k:prefix+k for k in z['wall_hosts']};ids={**wm,**hm,'K.kitchen':uid+'.kitchen','K.public_access':uid+'.kitchen_public_access','K.kitchen.entry':prefix+'entry','K.port':prefix+'port','kitchen':'kitchen',**{k:k for k in z['unit']['fixtures']},**{k:k for k in z['unit']['activities']}}
 # Typed kitchen-only access may use genuinely free dining floor. The
 # dining room remains distinct in geometry/accounting; this is a union view,
 # never a renamed room or exemption from actual occupied/motion obstacles.
 m.setdefault('logical_regions',{})[uid+'.kitchen_public_access']={'unit':uid,'source_roles':['living','entry_circulation','dining'],'kind':'KITCHEN_DINING_PUBLIC_ACCESS_VIEW','source_scope':'Blueprint294/295/380; kitchen/dining adjacency permitted, guest/cook/dining operation obstacles remain independently mandatory'}
 for key,q in z['walls'].items():m['walls'][wm[key]]=rr(q)
 for key,q in z['wall_hosts'].items():m['wall_hosts'][hm[key]]=rr(q);m['source_wall_hosts'][hm[key]]=rr(q)
 for opening in z['openings']:
  opening['rect']=rr(opening['rect']);opening['id']=ids[opening['id']];opening['host_wall_id']=hm[opening['host_wall_id']];opening['connects']=[ids[x]for x in opening['connects']];m['openings'].append(opening)
 zu=z['unit'];u['rooms']['kitchen']=[rr(q)for q in zu['rooms']['kitchen']]
 for key,q in zu['fixtures'].items():u['fixtures'][key]=rr(q);u['fixture_metadata'][key]=deepcopy(zu['fixture_metadata'][key])
 for key,q in zu['activities'].items():u['activities'][key]=rr(q)
 for op in z['operations']['kitchen']:
  op['unit']=uid;op['canonical_transform']={'matrix':[[-1,0],[0,sy]],'translation':[S(a),S(L-b if uid=='B'else-b)]};op['canonical_isometry']=op['canonical_transform'];op['access_point']=pt(op['access_point']);op['workpoint']=pt(op['workpoint']);op['front_binding']['back_wall_id']=hm[op['front_binding']['back_wall_id']]
  for binding in op['front_bindings'].values():binding['back_wall_id']=hm[binding['back_wall_id']]
  fridge=op['fridge']
  for k in('hinge','closed_actor','open_actor','open_access','shelf_target','held_target'):fridge[k]=pt(fridge[k])
  fridge['actor_offset_m']=vec(fridge['actor_offset_m'])
  for dr in op['drawers'].values():
   for k in('closed_actor','open_actor','grip_closed','grip_open','storage_target','held_target'):dr[k]=pt(dr[k])
   for k in('closed_tray','open_tray'):dr[k]=rr(dr[k])
   dr['translation']=vec(dr['translation'])
  for st in op['workstations']:st['actor_rect']=rr(st['actor_rect']);st['hand_point']=pt(st['hand_point'])
  m.setdefault('operations',{}).setdefault('kitchen',[]).append(op)
 for port in z['external_ports']:
  placed=deepcopy(port);placed.update(id=ids[port['id']],rect=rr(port['rect']),center=pt(port['center']),opening_id=ids[port['opening_id']],role_id=ids[port['role_id']]);m.setdefault('module_ports',[]).append(placed)
 m.setdefault('module_aprons',{})[uid+'.kitchen']=[rr(q)for q in zu['rooms']['public_access']]
 m.setdefault('module_placements',[]).append({'module':deepcopy(base),'module_hash':digest(base),'transform':{'matrix':[[1,0],[0,sy]],'translation':[S(a),S(L-b if uid=='B'else b)]},'id_map':ids,'unit_id':uid,'room_id':'kitchen','geometry_scope':'all source kitchen solids, fixtures, real passage and operation witnesses; whole-neighbor revalidation mandatory'})
