"""Install exact module geometry by isometry; receipts are not inherited."""
from copy import deepcopy
from fractions import Fraction as F
from contract114 import S,digest
from module_transform116 import reflect_x
from checker114 import check_module,check_twin_module

def install(base,m,u,uid,name,clearrect,L,side):
 extension=None
 if base.get('schema')=='ROTATABLE_PRIVATE_SOURCE133':
  from checker_source133 import examine
  checked=examine(base)
  if checked['errors'] or checked['pending']:raise ValueError('D4_SOURCE_REJECT:'+str(checked))
  extension=deepcopy(base);base=extension['base_module']
 gate=check_twin_module(base)if base.get('schema')=='PRIVATE_TWIN_ROOM_MODULE118'else check_module(base)
 if gate['status']!='PASS_MODULE_SCOPED':raise ValueError('PRIVATE_MODULE_REJECT:'+str(gate['errors'])+' pending='+str(gate['pending']))
 a,b,c,d=map(lambda x:F(str(x)),clearrect);L=F(L);W=c-a;z=deepcopy(base)
 if side not in ('left','right','top','bottom'):raise ValueError('UNKNOWN_SOURCE_ENTRY_SIDE')
 # D4 of the original independently checked source. No resizing or inherited receipt.
 source_w,source_h=map(F,[base['input_program']['width'],base['input_program']['depth']])
 if side in ('top','bottom') and extension is None:raise ValueError('SOURCE_ROTATION_NOT_AUTHORIZED_BY_CONTRACT')
 if side in ('left','right'):
  if W!=source_w or d-b!=source_h:raise ValueError('SOURCE_DIMENSION_MISMATCH')
 else:
  if W!=source_h or d-b!=source_w:raise ValueError('ROTATED_SOURCE_DIMENSION_MISMATCH')
 A={'left':[[1,0],[0,1]],'right':[[-1,0],[0,1]],'top':[[0,1],[-1,0]],'bottom':[[0,1],[1,0]]}[side]
 shift={'left':[a,b],'right':[c,b],'top':[a,d],'bottom':[a,b]}[side]
 if uid=='B':A=[A[0],[-v for v in A[1]]];shift=[shift[0],L-shift[1]]
 def pt(p):
  x,y=map(lambda v:F(str(v)),p);return [S(A[0][0]*x+A[0][1]*y+shift[0]),S(A[1][0]*x+A[1][1]*y+shift[1])]
 def rect(q):
  x,y,xx,yy=map(lambda v:F(str(v)),q);ps=[pt(v)for v in([x,y],[x,yy],[xx,y],[xx,yy])];return [S(min(F(v[0])for v in ps)),S(min(F(v[1])for v in ps)),S(max(F(v[0])for v in ps)),S(max(F(v[1])for v in ps))]
 def vec(v):
  x,y=map(lambda v:F(str(v)),v);return [S(A[0][0]*x+A[0][1]*y),S(A[1][0]*x+A[1][1]*y)]
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
 for key,q in zu['fixtures'].items():
  u['fixtures'][role(key)]=rect(q);meta=deepcopy(zu['fixture_metadata'][key]);meta['rotation_deg']=(meta.get('rotation_deg',0)+(90 if A[0][0]==0 else 0))%180;u['fixture_metadata'][role(key)]=meta
 for key,q in zu['activities'].items():u['activities'][key.replace('bed1.',name+'.')]=rect(q)
 for op in z['operations']['doors']:
  opening=next(v for v in base['openings']if v['id']==op['opening_id']);aa,bb,cc,dd=map(F,opening['rect']);axis=0 if dd-bb>cc-aa else 1
  sign=1 if op['mount']['face']=='max'else -1;target=[A[0][axis]*sign,A[1][axis]*sign];op['mount']['face']='max'if next(v for v in target if v)>0 else'min'
  motion(op);op['opening_id']=role(op['opening_id']);op['mount']['host_wall_id']=hm[op['mount']['host_wall_id']];m.setdefault('operations',{}).setdefault('doors',[]).append(op)
 for cl in z['operations']['closets']:
  axis=0 if cl['front_axis']=='x'else 1;sign=1 if cl['front_side']=='max'else -1;target=[A[0][axis]*sign,A[1][axis]*sign];cl['front_axis']='x'if target[0]else'y';cl['front_side']='max'if next(v for v in target if v)>0 else'min'
  cl['unit']=uid;cl['fixture_id']=role(cl['fixture_id']);cl['shell_rects']=[rect(q)for q in cl['shell_rects']]
  for panel in cl['panels']:motion(panel)
  m['operations'].setdefault('closets',[]).append(cl)
 m['room_metadata'][uid+'.'+name]={'role':'bedroom','private':True,'source':'independently_checked_parametric_private_module'}
 for port in z['external_ports']:
  placed=deepcopy(port);placed.update(id=role(port['id']),rect=rect(port['rect']),center=pt(port['center']),opening_id=role(port['opening_id']),role_id=role(port['role_id']));m.setdefault('module_ports',[]).append(placed)
 m.setdefault('module_aprons',{})[uid+'.'+name]=[rect(q)for q in zu['rooms']['public_access']]
 m.setdefault('module_placements',[]).append({'module':deepcopy(base),'module_hash':digest(base),'transform':{'matrix':A,'translation':list(map(S,shift))},'id_map':ids,'unit_id':uid,'room_id':name,'geometry_scope':'all module walls, fixtures, apertures, operations and room floor; external approach must remain usable in whole model'})

 if extension is not None:m['module_placements'][-1]['rotation_source133']=extension
