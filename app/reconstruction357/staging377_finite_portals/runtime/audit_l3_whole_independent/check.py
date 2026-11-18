import json,sys,copy,itertools,hashlib
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'audit_l3_independent'))
import importlib.util
sp=importlib.util.spec_from_file_location('helper',P/'audit_l3_independent'/'check.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);q,hit,covered,digest=h.q,h.hit,h.covered,h.digest
RECT={'rect','closed_panel','open_panel','pocket','rail_envelope','panel_rect','actor_rect','actor_start','actor_end'}
POINT={'center','hand_point','hand_start','hand_end'}
def audit(m,w):
 e=[];counts={'source_rects':0,'motion_geometry':0,'segments':0,'frame_rects':0}
 def req(v,s):
  if not v:e.append(s)
 def swap(r):a,b,c,d=q(r);return b,a,d,c
 for p in m['module_placements']:
  if not p['room_id'].startswith('bed'):continue
  uid=p['unit_id'];u=next(u for u in m['units']if u['id']==uid);s=p['module'];ids=p['id_map'];a=p['transform']['matrix'];t=q(p['transform']['translation'])
  req(digest(s)==p['module_hash'],'SOURCE_HASH')
  def pt(v):v=q(v);return tuple(sum(F(a[i][j])*v[j]for j in (0,1))+t[i]for i in (0,1))
  def rect(v):x,y,X,Y=q(v);ps=list(map(pt,[(x,y),(x,Y),(X,y),(X,Y)]));return min(v[0]for v in ps),min(v[1]for v in ps),max(v[0]for v in ps),max(v[1]for v in ps)
  for k in ('fixtures','activities'):
   for name,r in s['unit'][k].items():req(q(u[k][ids[name]])==rect(r),'SOURCE_'+k+':'+ids[name]);counts['source_rects']+=1
  for name,r in s['walls'].items():req(covered(rect(r),m['walls'].values()),'SOURCE_WALL:'+ids.get(name,name))
  def motion(x,y,key=''):
   if isinstance(x,dict):
    for k,v in x.items():
     if k in y:motion(v,y[k],k)
     elif k in RECT|POINT:req(False,'MISSING_MOTION:'+k)
   elif isinstance(x,list):
    if key in RECT|POINT and x and not isinstance(x[0],(dict,list)):
     req(q(y)==(rect(x)if key in RECT else pt(x)),'MOTION:'+uid+':'+key);counts['motion_geometry']+=1
    elif key=='translation':req(q(y)==tuple(sum(F(a[i][j])*F(x[j])for j in (0,1))for i in(0,1)),'MOTION_VECTOR')
    else:
     req(len(x)==len(y),'MOTION_COUNT')
     for z,v in zip(x,y):motion(z,v)
  for kind,idkey in [('doors','opening_id'),('closets','fixture_id')]:
   for x in s['operations'][kind]:
    y=next(z for z in m['operations'][kind]if z[idkey]==ids[x[idkey]] and z.get('unit',uid)==uid);motion(x,y)
 net=m['physical_wall_network'];ph=net['solids'];req(net['source_wall_hash']==digest(m['walls']),'PHYSICAL_HASH')
 req(all(covered(r,ph.values())for r in m['walls'].values())and all(covered(r,m['walls'].values())for r in ph.values()),'PHYSICAL_UNION')
 for (_,r),(_,z)in itertools.combinations(ph.items(),2):req(not hit(r,z),'PHYSICAL_OVERLAP')
 for d in m['private_domains']:
  u=next(u for u in m['units']if u['id']==d['unit']);ports={x['opening_id'].rsplit('.',1)[0]:q(x['center'])for x in m['module_ports']}
  req(set(d['paths'])==set(d['bedrooms']),'PATH_COUNT');floor=d['parts']+[d['public_interface']['rect']];obs=list(m['walls'].values())+list(u['fixtures'].values())
  for name,path in d['paths'].items():
   pts=list(map(q,path));req(pts[-1]==ports[name],'PATH_ENDPOINT')
   for a,b in zip(pts,pts[1:]):
    req(a[0]==b[0]or a[1]==b[1],'PATH_DIAGONAL');h=F('.35');r=min(a[0],b[0])-h,min(a[1],b[1])-h,max(a[0],b[0])+h,max(a[1],b[1])+h
    req(covered(r,floor),'PATH_FLOOR');req(not any(hit(r,z)for z in obs),'PATH_COLLISION');counts['segments']+=1
 for key in ('walls','wall_hosts','source_wall_hosts'):
  req(set(m[key])==set(w[key]),'FRAME_IDS')
  for name,r in m[key].items():req(name in w[key] and swap(r)==q(w[key][name]),'FRAME:'+key+':'+name);counts['frame_rects']+=1
 for u,v in zip(m['units'],w['units']):
  for key in ('fixtures','activities'):
   for name,r in u[key].items():req(swap(r)==q(v[key][name]),'FRAME:'+name);counts['frame_rects']+=1
 for d,z in zip(m['private_domains'],w['private_domains']):
  req([swap(r)for r in d['parts']]==list(map(q,z['parts'])),'FRAME_DOMAIN')
  req(swap(d['public_interface']['rect'])==q(z['public_interface']['rect']),'FRAME_INTERFACE')
  for name,path in d['paths'].items():req([tuple(reversed(q(p)))for p in path]==list(map(q,z['paths'][name])),'FRAME_PATH')
 return {'errors':sorted(set(e)),'counts':counts}
if __name__=='__main__':
 m=json.loads((P/'evidence_l3_whole131/local.json').read_text());w=json.loads((P/'evidence_l3_whole131/world.json').read_text());r=audit(m,w);neg={}
 for name in ('source_fixture','actor','path_obstacle','frame_wall','frame_path','source_hash'):
  a,b=copy.deepcopy(m),copy.deepcopy(w)
  if name=='source_fixture':a['units'][0]['fixtures'][next(iter(a['units'][0]['fixtures']))][0]='0'
  if name=='actor':a['operations']['doors'][0]['states'][0]['actor_rect'][0]='0'
  if name=='path_obstacle':a['walls']['injected']=['10','5','10.7','6']
  if name=='frame_wall':b['walls'][next(iter(b['walls']))][0]=str(F(b['walls'][next(iter(b['walls']))][0])+F('.1'))
  if name=='frame_path':next(iter(b['private_domains'][0]['paths'].values()))[-1]=['0','0']
  if name=='source_hash':a['module_placements'][0]['module_hash']='bad'
  z=audit(a,b);neg[name]={'rejected':bool(z['errors']),'errors':z['errors'][:5]}
 out={'baseline':r,'negative_tests':neg,'local_sha256':digest(m),'world_sha256':digest(w)};(Path(__file__).parent/'result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
