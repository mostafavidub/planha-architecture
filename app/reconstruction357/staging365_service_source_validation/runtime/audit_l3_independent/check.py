"""Independent exact subset, no solver/producer/geometry kernel imports."""
import json,hashlib,itertools,copy
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def q(r):return tuple(map(F,r))
def hit(a,b):
 a,b=q(a),q(b);return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])
def inside(p,rs):return any(r[0]<=p[0]<=r[2] and r[1]<=p[1]<=r[3]for r in rs)
def covered(r,rs):
 r=q(r);rs=list(map(q,rs));xs=sorted({r[0],r[2]}|{v for z in rs for v in (z[0],z[2])if r[0]<v<r[2]});ys=sorted({r[1],r[3]}|{v for z in rs for v in (z[1],z[3])if r[1]<v<r[3]})
 return all(inside(((a+b)/2,(c+d)/2),rs)for a,b in zip(xs,xs[1:])for c,d in zip(ys,ys[1:]))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def check(m):
 errors=[];counts={'source_geometry_items':0,'motion_values':0,'swept_segments':0};expectedwalls=[]
 def require(v,s):
  if not v:errors.append(s)
 try:
  require(len(m['module_placements'])==3,'SOURCE_COUNT');u=m['units'][0]
  for p in m['module_placements']:
   s=p['module'];name=p['room_id'];ids=p['id_map'];a=p['transform']['matrix'];t=list(map(F,p['transform']['translation']))
   require(a in ([[1,0],[0,1]],[[-1,0],[0,1]]),'UNSUPPORTED_TRANSFORM')
   require(digest(s)==p['module_hash'],'SOURCE_HASH:'+name)
   def pt(v):v=list(map(F,v));return tuple(sum(F(a[i][j])*v[j]for j in (0,1))+t[i]for i in (0,1))
   def vec(v):v=list(map(F,v));return tuple(sum(F(a[i][j])*v[j]for j in (0,1))for i in (0,1))
   def rr(v):x,y,X,Y=q(v);ps=[pt(z)for z in((x,y),(X,y),(x,Y),(X,Y))];return(min(z[0]for z in ps),min(z[1]for z in ps),max(z[0]for z in ps),max(z[1]for z in ps))
   def eq(actual,expected,label):counts['source_geometry_items']+=1;require(q(actual)==expected,label)
   expectedwalls +=[rr(v)for v in s['walls'].values()]
   for key,v in s['unit']['fixtures'].items():eq(u['fixtures'][ids[key]],rr(v),'FIXTURE:'+name+key)
   for key,v in s['unit']['activities'].items():eq(u['activities'][ids[key]],rr(v),'ACTIVITY:'+name+key)
   require(list(map(q,u['rooms'][name]))==[rr(v)for v in s['unit']['rooms']['bed1']],'ROOM:'+name)
   for o in s['openings']:
    z=next(z for z in m['openings']if z['id']==ids[o['id']]);eq(z['rect'],rr(o['rect']),'APERTURE:'+name);require(z['connects']==[ids.get(x,x)for x in o['connects']],'CONNECTS:'+name)
   for z in s['external_ports']:
    out=next(x for x in m['module_ports']if x['id']==ids[z['id']]);eq(out['rect'],rr(z['rect']),'PORT_RECT:'+name);eq(out['center'],pt(z['center']),'PORT_POINT:'+name)
   def motion(old,new,label):
    for k in ('closed_panel','open_panel','pocket','rail_envelope'):
     if k in old:eq(new[k],rr(old[k]),label+k);counts['motion_values']+=1
    eq(new['translation'],vec(old['translation']),label+'translation')
    for group in ('states','continuous_actor_segments'):
     require(len(old[group])==len(new[group]),label+group+'count')
     for x,y in zip(old[group],new[group]):
      for k in ('panel_rect','actor_rect','actor_start','actor_end'):
       if k in x:eq(y[k],rr(x[k]),label+k);counts['motion_values']+=1
      for k in ('hand_point','hand_start','hand_end'):
       if k in x:eq(y[k],pt(x[k]),label+k);counts['motion_values']+=1
      require(y['role_id']==ids.get(x['role_id'],x['role_id']),label+'role')
   for z in s['operations']['doors']:
    out=next(x for x in m['operations']['doors']if x['opening_id']==ids[z['opening_id']]);motion(z,out,'DOOR:'+name)
   for z in s['operations']['closets']:
    out=next(x for x in m['operations']['closets']if x['fixture_id']==ids[z['fixture_id']]);require(list(map(q,out['shell_rects']))==[rr(v)for v in z['shell_rects']],'SHELL:'+name)
    require(out['front_side']==('min'if z['front_side']=='max'else'max')if a[0][0]==-1 else out['front_side']==z['front_side'],'SHELL_FACE:'+name)
    for x,y in zip(z['panels'],out['panels']):motion(x,y,'CLOSET:'+name)
  hall=[['6.75','3.9','6.9','9.45'],['5.6','9.3','6.75','9.45']];expectedwalls +=list(map(q,hall));walls=list(m['walls'].values())
  require(all(covered(r,walls)for r in expectedwalls)and all(covered(r,expectedwalls)for r in walls),'SOURCE_WALL_UNION')
  net=m['physical_wall_network'];physical=net['solids'];aliases=net['source_aliases']
  require(net['source_wall_hash']==digest(m['walls']),'PHYSICAL_SOURCE_HASH')
  require(all(covered(r,physical.values())for r in walls)and all(covered(r,walls)for r in physical.values()),'PHYSICAL_UNION')
  require(set(aliases)==set(m['walls']),'PHYSICAL_ALIAS_INVENTORY')
  for name,r in m['walls'].items():
   require(set(aliases.get(name,[]))=={k for k,v in physical.items()if hit(r,v)},'PHYSICAL_ALIAS:'+name)
  for (a,r),(b,s)in itertools.combinations(physical.items(),2):require(not hit(r,s),'DUPLICATE_SOLID:'+a+':'+b)
  for (a,rs),(b,ss)in itertools.combinations(u['rooms'].items(),2):require(not any(hit(r,s)for r in rs for s in ss),'ROOM_AREA_OVERLAP:'+a+':'+b)
  # Source aliases may refer to subdivisions; every declared source host retained.
  for a,b in m.get('physical_wall_aliases',{}).items():require(a in m['source_wall_hosts'] and b in m['walls']and covered(m['source_wall_hosts'][a],[m['walls'][b]]),'ALIAS:'+a)
  d=m['private_domains'][0];parts=d['parts'];interface=d['public_interface']['rect'];floor=parts+[interface];obs=walls+list(u['fixtures'].values());ports={z['opening_id'].rsplit('.',1)[0]:q(z['center'])for z in m['module_ports']}
  require(set(d['paths'])==set(ports),'PATH_INVENTORY');require(not any(hit(r,['6.9','3.9','12.35','9.3'])for r in parts),'ABSENT_QUADRANT_CONSUMED')
  for name,path in d['paths'].items():
   pts=list(map(q,path));require(pts[0]==(F('6.25'),F('.15'))and pts[-1]==ports[name],'PATH_END:'+name)
   for a,b in zip(pts,pts[1:]):
    require(a[0]==b[0]or a[1]==b[1],'PATH_DIAGONAL');h=F('.35');r=(min(a[0],b[0])-h,min(a[1],b[1])-h,max(a[0],b[0])+h,max(a[1],b[1])+h);counts['swept_segments']+=1;require(covered(r,floor),'PATH_FLOOR:'+name);require(not any(hit(r,z)for z in obs),'PATH_OBSTACLE:'+name)
  # Exact partition-edge check, separate from runtime topology implementation.
  cover=walls+[z['rect']for z in m['openings']];allr=list(map(q,parts+cover+[interface]));xs=sorted({z[i]for z in allr for i in(0,2)});ys=sorted({z[i]for z in allr for i in(1,3)});rs=list(map(q,parts));cv=list(map(q,cover))
  for axis,edges,spans in ((0,xs,ys),(1,ys,xs)):
   for i,v in enumerate(edges):
    lo=(edges[i-1]+v)/2 if i else v-1;hi=(v+edges[i+1])/2 if i+1<len(edges)else v+1
    for a,b in zip(spans,spans[1:]):
     z=(a+b)/2;l=(lo,z)if axis==0 else(z,lo);r=(hi,z)if axis==0 else(z,hi)
     if inside(l,rs)==inside(r,rs):continue
     x,y=(v,z)if axis==0 else(z,v)
     port=axis==1 and v==F('.15')and F('5.75')<=z<=F('6.75')
     require(port or inside((x,y),cv),'BOUNDARY_GAP:'+str((x,y)))
 except(Exception)as e:errors.append('SCHEMA:'+type(e).__name__+':'+str(e))
 return {'errors':sorted(set(errors)),'counts':counts,'scope':'Independent exact source-transform, physical-solid union, corridor/body and boundary subset only. No whole model privacy/placement/quality or concurrent user acceptance.'}
if __name__=='__main__':
 m=json.loads((P/'evidence_l3_primitive131/model.json').read_text());r=check(m);(P/'audit_l3_independent/result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
