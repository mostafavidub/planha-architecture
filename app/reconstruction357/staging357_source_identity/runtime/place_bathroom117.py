"""Reference-bound wet-room placement without scaling source pocket assemblies."""
from copy import deepcopy
from fractions import Fraction as F
from contract114 import S,digest
from checker114 import check_bathroom_module

def install(base,m,u,uid,clearrect,L):
 gate=check_bathroom_module(base)
 if gate['status']!='PASS_MODULE_SCOPED':raise ValueError('BATHROOM_MODULE_REJECT:'+str(gate['errors'])+' pending='+str(gate['pending']))
 a,b,c,d=map(lambda x:F(str(x)),clearrect);L=F(L);sy=-1 if uid=='B'else 1;z=deepcopy(base);prefix=uid+'.bath.'
 def pt(p):x,y=map(lambda v:F(str(v)),p);return[S(a+x),S(L-b-y if uid=='B'else b+y)]
 def rr(q):x,y,xx,yy=map(lambda v:F(str(v)),q);p=pt([x,y]);r=pt([xx,yy]);return[S(min(F(p[0]),F(r[0]))),S(min(F(p[1]),F(r[1]))),S(max(F(p[0]),F(r[0]))),S(max(F(p[1]),F(r[1])))]
 def vec(q):return[S(F(str(q[0]))),S(sy*F(str(q[1])))]
 wm={k:prefix+k for k in z['walls']};hm={k:prefix+k for k in z['wall_hosts']};ids={**wm,**hm,**{'S.'+k:uid+'.'+k for k in('bath','vanity','WC','shower','public_access')},'S.port':prefix+'port','bath':'bath',**{k:k for k in z['unit']['fixtures']},**{k:k for k in z['unit']['activities']}}
 for key,q in z['walls'].items():m['walls'][wm[key]]=rr(q)
 for key,q in z['wall_hosts'].items():m['wall_hosts'][hm[key]]=rr(q);m['source_wall_hosts'][hm[key]]=rr(q)
 for opening in z['openings']:
  opening['rect']=rr(opening['rect']);opening['id']=ids[opening['id']];opening['host_wall_id']=hm[opening['host_wall_id']];opening['connects']=[ids[x]for x in opening['connects']];m['openings'].append(opening)
 zu=z['unit'];u['rooms']['bath']=[rr(q)for q in zu['rooms']['bath']]
 for key,q in zu['fixtures'].items():u['fixtures'][key]=rr(q);u['fixture_metadata'][key]=deepcopy(zu['fixture_metadata'][key])
 for key,q in zu['activities'].items():u['activities'][key]=rr(q)
 for key,region in z['logical_regions'].items():m.setdefault('logical_regions',{})[ids[key]]={'unit':uid,'parts':[rr(q)for q in region['parts']],'source_module_bound':True}
 for op in z['operations']['doors']:
  op['opening_id']=ids[op['opening_id']];op['host_wall_id']=hm[op['host_wall_id']]
  for k in('closed_panel','open_panel','pocket'):op[k]=rr(op[k])
  op['translation']=vec(op['translation']);op['open_transfer_points']=[pt(p)for p in op['open_transfer_points']]
  for st in op['states']:
   st['unit']=uid;st['role_id']=ids[st['role_id']];st['panel_rect']=rr(st['panel_rect']);st['actor_rect']=rr(st['actor_rect']);st['hand_point']=pt(st['hand_point'])
  for seg in op['continuous_actor_segments']:
   seg['unit']=uid;seg['role_id']=ids[seg['role_id']]
   for k in('actor_start','actor_end'):seg[k]=rr(seg[k])
   for k in('hand_start','hand_end'):seg[k]=pt(seg[k])
  m.setdefault('operations',{}).setdefault('doors',[]).append(op)
 for port in z['external_ports']:
  placed=deepcopy(port);placed.update(id=ids[port['id']],rect=rr(port['rect']),center=pt(port['center']),opening_id=ids[port['opening_id']],role_id=ids[port['role_id']]);m.setdefault('module_ports',[]).append(placed)
 m.setdefault('module_aprons',{})[uid+'.bath']=[rr(q)for q in zu['rooms']['public_access']]
 m.setdefault('module_placements',[]).append({'module':deepcopy(base),'module_hash':digest(base),'transform':{'matrix':[[1,0],[0,sy]],'translation':[S(a),S(L-b if uid=='B'else b)]},'id_map':ids,'unit_id':uid,'room_id':'bath','geometry_scope':'source-bound pocket doors/skins/fixtures/tasks/privacy with independent whole-neighbor revalidation'})
