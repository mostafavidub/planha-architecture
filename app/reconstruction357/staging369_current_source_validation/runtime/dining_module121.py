"""Separate six-place planar study. No runtime119 imports or modifications."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from contract114 import S
from geometry114 import route
ROOT=Path(__file__).parent
seq=lambda r:list(map(S,r))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build(width='5.4',depth='4.4'):
 W,H=F(width),F(depth)
 if W<=0 or H<=0:raise ValueError('POSITIVE_FRAME_REQUIRED')
 cx,cy=W/2,H/2
 table=[cx-F('1.1'),cy-F('.5'),cx+F('1.1'),cy+F('.5')]
 # Four side chairs and two end chairs; immutable .5m square instances.
 # Normal points away from the tabletop; tangent exit points away from the
 # neighboring side seat. These are proposed trajectories, not ergonomics.
 specs=[('front_left',(-F('.55'),-F('.75')),(0,-1),(-1,0)),('front_right',(F('.55'),-F('.75')),(0,-1),(1,0)),('back_left',(-F('.55'),F('.75')),(0,1),(-1,0)),('back_right',(F('.55'),F('.75')),(0,1),(1,0)),('left',(-F('1.35'),0),(-1,0),(0,-1)),('right',(F('1.35'),0),(1,0),(0,1))]
 fixtures={'table':seq(table)};seats=[]
 def rect(x,y,size):return [x-size/2,y-size/2,x+size/2,y+size/2]
 def shift(q,dx,dy):return [v+(dx if i%2==0 else dy)for i,v in enumerate(q)]
 for name,off,n,t in specs:
  x,y=cx+off[0],cy+off[1];q=rect(x,y,F('.5'));de=(F('.4')*n[0],F('.4')*n[1]);pulled=shift(q,*de)
  occ=rect(x+F('.1')*n[0],y+F('.1')*n[1],F('.7'));pb=shift(occ,*de);standing=shift(pb,F('.85')*t[0],F('.85')*t[1]);fid='chair_'+name;fixtures[fid]=seq(q)
  seats.append({'id':name,'fixture_id':fid,'closed_rect':seq(q),'pulled_rect':seq(pulled),'translation':seq(de),'occupied_body':seq(occ),'rise_transfer':{'closed_occupied_body':seq(occ),'pulled_occupied_body':seq(pb),'standing_body':seq(standing),'other_seats_remain_occupied':True,'other_occupied_seat_count':5,'segments':[{'phase':'seated_pull','actor_start':seq(occ),'actor_end':seq(pb),'chair_start':seq(q),'chair_end':seq(pulled)},{'phase':'rise_and_side_exit_study','actor_start':seq(pb),'actor_end':seq(standing),'chair_start':seq(pulled),'chair_end':seq(pulled)}]},'own_chair_contact_scope':'Only bound seated-pull and side-exit task. No walking exception; vertical support/ergonomics NOT_VERIFIED.'})
 obstacles=list(fixtures.values())
 for s in seats:
  a,b=list(map(F,s['closed_rect'])),list(map(F,s['pulled_rect']));obstacles += [seq([min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])]),s['occupied_body']]
 ports={'guest':[S(F('.35')),S(H/2)],'serving':[S(W-F('.35')),S(H/2)]};routes={};fail=[]
 for port,start in ports.items():
  for seat in seats:
   q=list(map(F,seat['rise_transfer']['standing_body']));target=[(q[0]+q[2])/2,(q[1]+q[3])/2];key=port+'_'+seat['id'];path,why=route(start,target,['0','0',S(W),S(H)],obstacles)
   if path:routes[key]=path
   else:fail.append({'route':key,'reason':why})
 source=ROOT/'references/program6/proposal_metadata.json';meta=json.loads(source.read_text());pdf=ROOT/'references/program6/assembly_AA-1924803-2.pdf'
 assert hashlib.sha256(pdf.read_bytes()).hexdigest()==meta['assembly_sha256']
 return {'schema':'SIX_PLACE_PLANAR_SOURCE_STUDY_V1','width':S(W),'depth':S(H),'fixtures':fixtures,'seating':{'requested_places':6,'distinct_chair_count':6,'instances':seats},'ports':ports,'routes':routes,'route_failures':fail,'source_binding':{'profile_id':meta['suggested_profile_id'],'metadata_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'assembly_sha256':meta['assembly_sha256'],'table_fixed_dimensions_m':['2.20','1.00','.74'],'chair_source':'Existing reference immutable .5x.5 footprint; six distinct instances, no resizing','chair_source_file':'references/program6/chair_reference_model.json','chair_source_sha256':hashlib.sha256((ROOT/'references/program6/chair_reference_model.json').read_bytes()).hexdigest(),'chair_source_fixture_key':'dining_chair_front','nominal_seats_not_operational_proof':True},'assumptions':{'body_m':'.7','chair_pull_m':'.4','side_exit_m':'.85','planar_tangency_allowed':True,'tabletop_footprint_is_solid_for_all_body_and_public_routes':True},'not_verified':['Exact legs/rail sections and coordinates','Knee/under-table clearance','Vertical seated transfer and support forces','Real ergonomics','Whole-unit serving/guest approach outside module','Six-person living/storage/day-to-day capacity'],'accepted':False,'technical_approved':False,'runtime119_integrated':False}
