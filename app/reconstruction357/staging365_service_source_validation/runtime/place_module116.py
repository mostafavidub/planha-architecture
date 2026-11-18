"""Install exact module geometry by isometry; receipts are not inherited."""
from copy import deepcopy
from fractions import Fraction as F
from contract114 import S,digest
from module_transform116 import reflect_x
from checker114 import check_module,check_twin_module

def install(base,m,u,uid,name,clearrect,L,side):
 gate=check_twin_module(base)if base.get('schema')=='PRIVATE_TWIN_ROOM_MODULE118'else check_module(base)
 if gate['status']!='PASS_MODULE_SCOPED':raise ValueError('PRIVATE_MODULE_REJECT:'+str(gate['errors'])+' pending='+str(gate['pending']))
 a,b,c,d=map(lambda x:F(str(x)),clearrect);L=F(L);W=c-a;z=reflect_x(base)if side=='right'else deepcopy(base)
 sy=-1 if uid=='B'else 1;sx=-1 if side=='right'else 1
 def pt(p):x,y=map(lambda v:F(str(v)),p);return[S(a+x),S(L-b-y if uid=='B'else b+y)]
 def rect(q):x,y,xx,yy=map(lambda v:F(str(v)),q);p=pt([x,y]);r=pt([xx,yy]);return[S(min(F(p[0]),F(r[0]))),S(min(F(p[1]),F(r[1]))),S(max(F(p[0]),F(r[0]))),S(max(F(p[1]),F(r[1])))]
 def vec(v):x,y=map(lambda v:F(str(v)),v);return[S(x),S(sy*y)]
 prefix=uid+'.'+name+'.';wm={k:prefix+k for k in z['walls']};hm={k:prefix+k for k in z['wall_hosts']};ids={**wm,**hm,'M.bed1':uid+'.'+name,'M.public_access':uid+('.private_access'if m.get('ordered_macro')else'.bedroom_public_access'),'M.bed1.entry':prefix+'entry','bed1':name,'bed1.bed':name+'.bed','bed1.closet':name+'.closet'}
 for k in z['unit']['fixtures']:ids[k]=k.replace('bed1.',name+'.')
 for k in z['unit']['activities']:ids[k]=k.replace('bed1.',name+'.')
 ids['M.port']=prefix+'port'
 def role(s):return ids.get(s,s)
 def motion(op):
  for k in('closed_panel','open_panel','pocket','rail_envelope'):
   if k in op:op[k]=rect(op[k])
  op['translation']=vec(op['translation'])
  for st in op.get('states',[]):
   st['unit']=uid;st['role_id']=role(st.get('role_id',''))
   for k in('panel_rect','actor_rect'):st[k]=rect(st[k])
   st['hand_point']=pt(st['hand_point'])
  for seg in op.get('continuous_actor_segments',[]):
   seg['unit']=uid;seg['role_id']=role(seg.get('role_id',''))
   for k in('actor_start','actor_end'):seg[k]=rect(seg[k])
   for k in('hand_start','hand_end'):seg[k]=pt(seg[k])
 for key,q in z['walls'].items():m['walls'][wm[key]]=rect(q)
 for key,q in z['wall_hosts'].items():m['wall_hosts'][hm[key]]=rect(q);m['source_wall_hosts'][hm[key]]=rect(q)
 for opening in z['openings']:
  opening['rect']=rect(opening['rect']);opening['id']=role(opening['id']);opening['host_wall_id']=hm[opening['host_wall_id']];opening['connects']=[role(x)for x in opening['connects']];m['openings'].append(opening)
 zu=z['unit'];u['rooms'][name]=[rect(q)for q in zu['rooms']['bed1']]
 for key,q in zu['fixtures'].items():u['fixtures'][role(key)]=rect(q);u['fixture_metadata'][role(key)]=deepcopy(zu['fixture_metadata'][key])
 for key,q in zu['activities'].items():u['activities'][key.replace('bed1.',name+'.')]=rect(q)
 for op in z['operations']['doors']:
  motion(op);op['opening_id']=role(op['opening_id']);op['mount']['host_wall_id']=hm[op['mount']['host_wall_id']];m.setdefault('operations',{}).setdefault('doors',[]).append(op)
 for cl in z['operations']['closets']:
  cl['unit']=uid;cl['fixture_id']=role(cl['fixture_id']);cl['shell_rects']=[rect(q)for q in cl['shell_rects']]
  for panel in cl['panels']:motion(panel)
  m['operations'].setdefault('closets',[]).append(cl)
 m['room_metadata'][uid+'.'+name]={'role':'bedroom','private':True,'source':'independently_checked_parametric_private_module'}
 for port in z['external_ports']:
  placed=deepcopy(port);placed.update(id=role(port['id']),rect=rect(port['rect']),center=pt(port['center']),opening_id=role(port['opening_id']),role_id=role(port['role_id']));m.setdefault('module_ports',[]).append(placed)
 m.setdefault('module_aprons',{})[uid+'.'+name]=[rect(q)for q in zu['rooms']['public_access']]
 m.setdefault('module_placements',[]).append({'module':deepcopy(base),'module_hash':digest(base),'transform':{'matrix':[[sx,0],[0,sy]],'translation':[S(a+W if side=='right'else a),S(L-b if uid=='B'else b)]},'id_map':ids,'unit_id':uid,'room_id':name,'geometry_scope':'all module walls, fixtures, apertures, operations and room floor; external approach must remain usable in whole model'})
