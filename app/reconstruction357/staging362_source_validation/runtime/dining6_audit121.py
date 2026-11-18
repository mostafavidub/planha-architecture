"""Independent exact planar six-seat study; no producer imports/status reliance."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
BODY=F('.7')
def digest(m):return hashlib.sha256(json.dumps(m,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def q(x):
 r=tuple(F(str(v))for v in x)
 if len(r)!=4 or r[0]>=r[2]or r[1]>=r[3]:raise ValueError('RECT')
 return r
def hit(a,b):return max(a[0],b[0])<min(a[2],b[2])and max(a[1],b[1])<min(a[3],b[3])
def inside(a,b):return b[0]<=a[0]<a[2]<=b[2]and b[1]<=a[1]<a[3]<=b[3]
def sweep(a,b):
 a,b=q(a),q(b)
 if (a[2]-a[0],a[3]-a[1])!=(b[2]-b[0],b[3]-b[1])or(a[0]!=b[0]and a[1]!=b[1]):raise ValueError('NONRIGID_DIAGONAL')
 return(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))
def body(p):x,y=map(F,p);return(x-BODY/2,y-BODY/2,x+BODY/2,y+BODY/2)
def examine(m):
 errors=[];witness=[];routes=[]
 def fail(code,**kw):errors.append(dict(code=code,**kw))
 try:
  s=m['source_binding']
  source=Path(__file__).parent/'references/program6/chair_reference_model.json'
  expected_chair_hash='2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4'
  if hashlib.sha256(source.read_bytes()).hexdigest()!=expected_chair_hash or s.get('chair_source_sha256')!=expected_chair_hash or s.get('chair_source_fixture_key')!='dining_chair_front':raise ValueError('CHAIR_REFERENCE_BINDING')
  if s['metadata_sha256']!='ca992de5c7ee38a5d84addcdd8abd51ab2801317654f41ab2c9fe7522084c3c6'or s['assembly_sha256']!='24ad6e419508b4f8cb87d7f270e84df5deb5523f60e02098fab39759f8cb7d71'or s['profile_id']!='PROPOSED_IKEA_MORBYLANGA_20293766_FIXED_2200x1000':raise ValueError('SOURCE_BINDING')
  for filename,expected in [('proposal_metadata.json',s['metadata_sha256']),('assembly_AA-1924803-2.pdf',s['assembly_sha256'])]:
   if hashlib.sha256((source.parent/filename).read_bytes()).hexdigest()!=expected:raise ValueError('LOCAL_SOURCE_FILE_CHANGED:'+filename)
  frame=(F(0),F(0),F(m['width']),F(m['depth']));fs={k:q(v)for k,v in m['fixtures'].items()};table=fs['table'];seats=m['seating']['instances'];ids=[s['fixture_id']for s in seats]
  if len(seats)!=6 or len(set(ids))!=6 or set(fs)!={'table',*ids}:raise ValueError('SIX_ACTUAL_CHAIRS_REQUIRED')
  if sorted([table[2]-table[0],table[3]-table[1]])!=[F(1),F('2.2')]:raise ValueError('FIXED_TABLE_SIZE')
  occ={s['fixture_id']:q(s['occupied_body'])for s in seats};chair_sweeps={s['fixture_id']:sweep(s['closed_rect'],s['pulled_rect'])for s in seats}
  for seat in seats:
   fid=seat['fixture_id'];closed=q(seat['closed_rect']);opened=q(seat['pulled_rect']);de=tuple(map(F,seat['translation']));r=seat['rise_transfer'];segments=r['segments']
   if closed!=fs[fid]or(closed[2]-closed[0],closed[3]-closed[1])!=(F('.5'),F('.5')):raise ValueError('CHAIR_SOURCE_SIZE_OR_BINDING')
   if de[0]*de[1]or sum(abs(x)for x in de)!=F('.4')or tuple(closed[j]+de[j%2]for j in range(4))!=opened:raise ValueError('FIXED_PULL')
   if len(segments)!=2 or [z['phase']for z in segments]!=['seated_pull','rise_and_side_exit_study']:raise ValueError('TASK_PHASES')
   prev_a=occ[fid];prev_c=closed
   if q(r['closed_occupied_body'])!=prev_a or not hit(prev_a,closed):raise ValueError('SEAT_SUPPORT_BINDING')
   for i,seg in enumerate(segments):
    a,b=q(seg['actor_start']),q(seg['actor_end']);c,d=q(seg['chair_start']),q(seg['chair_end'])
    if a!=prev_a or c!=prev_c or(a[2]-a[0],a[3]-a[1])!=(BODY,BODY):raise ValueError('BODY_CONTINUITY_SIZE')
    if i==0 and (tuple(b[j]-a[j]for j in(0,1))!=de or d!=opened or b!=q(r['pulled_occupied_body'])):raise ValueError('PULL_ACTOR_BINDING')
    if i==1 and(c!=d or b!=q(r['standing_body'])or hit(b,d)or sum(de[j]*(b[j]-a[j])for j in(0,1))!=0):raise ValueError('SIDE_EXIT_STANDING')
    obstacles={**{k:v for k,v in fs.items()if k!=fid},**{'occupied:'+k:v for k,v in occ.items()if k!=fid}}
    for kind,sw in [('actor',sweep(a,b)),('chair',sweep(c,d))]:
     if not inside(sw,frame):fail('MOTION_OUTSIDE',seat=fid,phase=i,object=kind)
     for key,ob in obstacles.items():
      if hit(sw,ob):fail('MOTION_COLLISION',seat=fid,phase=i,object=kind,obstacle=key)
    prev_a,prev_c=b,d
   witness.append({'seat':fid,'other_occupied_count':5,'phases_checked':2})
   end=q(r['standing_body']);center=((end[0]+end[2])/2,(end[1]+end[3])/2)
   for role in('guest','serving'):
    key=role+'_'+seat['id'];path=[tuple(map(F,p))for p in m['routes'][key]]
    if len(path)<2 or path[0]!=tuple(map(F,m['ports'][role]))or path[-1]!=center:raise ValueError('ROUTE_ENDPOINT_BINDING')
    for a,b in zip(path,path[1:]):
     if a==b:raise ValueError('ZERO_ROUTE_SEGMENT')
     sw=sweep(body(a),body(b))
     if not inside(sw,frame):fail('ROUTE_OUTSIDE',route=key)
     for ob in [table,*chair_sweeps.values(),*occ.values()]:
      if hit(sw,ob):fail('PUBLIC_ROUTE_COLLISION',route=key)
    routes.append(key)
  if set(routes)!=set(m['routes']):raise ValueError('ROUTE_INVENTORY')
 except(KeyError,ValueError,TypeError,IndexError)as e:fail('MALFORMED',detail=str(e))
 return {'errors':errors,'status':'FAIL_SCOPED'if errors else'PASS_SIX_PLACE_PLANAR_STUDY','model_hash':digest(m),'checked_seats':witness,'checked_routes':routes,'accepted':False,'runtime119_integrated':False,'scope':'Sequential one-seat pull/side-exit with five other seats occupied. Public routes avoid all six occupied bodies and full chair sweeps; tabletop is solid. Own-chair contact only in bound seat task. Legs/rail/knees, vertical transfer, support forces, ergonomics and whole-unit capacity NOT_VERIFIED.'}
