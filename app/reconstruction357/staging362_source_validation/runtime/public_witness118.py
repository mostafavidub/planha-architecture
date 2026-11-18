"""Bind actual dining motions and independent public/serving route proposals.
No ergonomic transfer or capacity approval is generated here.
"""
from fractions import Fraction as F
from copy import deepcopy
from contract114 import S
from geometry114 import Q,route

def install(m):
 allwalls=list(m['walls'].values())+[o['open_panel']for o in m.get('operations',{}).get('doors',[])]
 m.setdefault('operations',{})['dining_chairs']=[]
 for u in m['units']:
  uid=u['id'];pl=u['dining_module_placement'];mat=pl['transform']['matrix'];t=list(map(F,pl['transform']['translation']))
  def pt(p):p=list(map(F,p));return [S(sum(F(mat[i][j])*p[j]for j in range(2))+t[i])for i in range(2)]
  def rect(q):q=Q(q);a,b=pt(q[:2]),pt(q[2:]);return [S(min(F(a[0]),F(b[0]))),S(min(F(a[1]),F(b[1]))),S(max(F(a[0]),F(b[0]))),S(max(F(a[1]),F(b[1])))]
  def center(q):q=Q(q);return[S((q[0]+q[2])/2),S((q[1]+q[3])/2)]
  chairblocks=[]
  for seat in pl['module']['seating']['instances']:
   q,r=rect(seat['closed_rect']),rect(seat['pulled_rect']);a,b=Q(q),Q(r);sweep=[S(min(a[0],b[0])),S(min(a[1],b[1])),S(max(a[2],b[2])),S(max(a[3],b[3]))];occ=rect(seat['occupied_body']);rise=seat['rise_transfer']
   op={'unit':uid,'fixture_id':pl['id_map'][seat['fixture_id']],'closed_rect':q,'open_rect':r,'translation':[S(F(r[0])-F(q[0])),S(F(r[1])-F(q[1]))],'occupied_body':occ,'egress_route':[pt(center(rise['pulled_occupied_body'])),pt(center(rise['standing_body']))],'source_module_hash':pl['module_hash'],'human_transfer_validated':False}
   m['operations']['dining_chairs'].append(op);chairblocks += [sweep,occ]
  kmotions=[]
  for k in m['operations'].get('kitchen',[]):
   if k['unit']!=uid:continue
   envelope=[]
   for d in k['drawers'].values():
    a,b=Q(d['closed_tray']),Q(d['open_tray']);envelope.append([S(min(a[0],b[0])),S(min(a[1],b[1])),S(max(a[2],b[2])),S(max(a[3],b[3]))])
    a,b=list(map(F,d['closed_actor'])),list(map(F,d['open_actor']));envelope.append([S(min(a[0],b[0])-F('.35')),S(min(a[1],b[1])-F('.35')),S(max(a[0],b[0])+F('.35')),S(max(a[1],b[1])+F('.35'))])
   fr=k['fridge'];x,y=map(F,fr['hinge']);r=F(fr['leaf_radius_m'])+F(fr['leaf_half_thickness_m']);envelope.append(list(map(S,[x-r,y-r,x+r,y+r])))
   a,b=list(map(F,fr['closed_actor'])),list(map(F,fr['open_actor']));envelope.append([S(min(a[0],b[0])-F('.35')),S(min(a[1],b[1])-F('.35')),S(max(a[0],b[0])+F('.35')),S(max(a[1],b[1])+F('.35'))])
   k['motion_envelopes']=envelope;k['motion_envelope_scope']='Conservative actual source motion bounds, including full leaf-radius box; not claimed minimal.';kmotions+=envelope
  six_person=pl['module']['schema']=='SIX_PLACE_PLANAR_SOURCE_STUDY_V1';dining_activity='dining_right'if six_person else'dining_east';dining_fixture='dining_chair_right'if six_person else'dining_chair_east'
  entry=next(iter(u['routes'].values()))[0];u['entry_point']=entry
  u['public_program']={'destinations':{'guest_living':{'activity_id':'sofa1_front','fixture_id':'sofa1'},'guest_dining':{'activity_id':dining_activity,'fixture_id':dining_fixture,'binding':'actual_dining_operation_standing_endpoint'},'kitchen_to_dining_floor':{'activity_id':dining_activity,'fixture_id':dining_fixture,'binding':'actual_dining_operation_standing_endpoint'}},'capacity_status':'NOT_PROVEN_BY_FURNITURE_COUNT'}
  bind_capacity(u)
  private=sum([rs for k,rs in u['rooms'].items()if k.startswith('bed')or k in('bath','private_circulation')],[]);base=allwalls+list(u['fixtures'].values())+private+chairblocks;box=Q(u['ownership'][0])
  # Access to each actual living seat must also avoid other occupied
  # living/dining bodies, not only their smaller furniture footprints.
  living=u['public_program']['capacity']['living_seats']
  for seat in living:
   k=seat['fixture_id'];target=center(u['activities'][k+'_front']);obs=base+[z['occupied_body']for z in living if z['fixture_id']!=k]
   path,why=route(entry,target,box,obs)
   if path:u['routes'][k+'_front']=path
   else:u['routes'].pop(k+'_front',None);m['route_failures'].append({'unit':uid,'route':k+'_front','reason':why,'profile':'living_access_other_occupied_seats'})
  for name,target in [('guest_living',center(u['activities']['sofa1_front'])),('guest_dining',center(u['activities'][dining_activity])),('kitchen_to_dining_floor',center(u['activities'][dining_activity]))]:
   start=entry if name.startswith('guest')else center(u['activities']['kitchen_work']);obs=base+(u['rooms']['kitchen']+kmotions if name.startswith('guest')else[]);path,why=route(start,target,box,obs)
   if path:u['scenario_routes'][name]=path
   else:u['scenario_routes'].pop(name,None);m['route_failures'].append({'unit':uid,'route':name,'reason':why,'profile':'public_all_seat_motion_occupied_and_kitchen_exclusion'})
 return m

def bind_capacity(u):
 pl=u['dining_module_placement']
 sleeping=[{'id':k+'.place','fixture_id':k,'places':2 if v['kind']=='bed'else 1,'source_basis':'Reference double design2 / A9 single design1; actual access separately checked'}for k,v in u['fixture_metadata'].items()if v['kind']in('bed','single_bed')]
 dining=[{'id':s['id'],'fixture_id':pl['id_map'][s['fixture_id']],'places':1,'source_basis':'One actual source chair; continuous external-obstacle proof only, own-seat transfer remains explicit'}for s in pl['module']['seating']['instances']]
 living=[]
 for k in [key for key,v in u['fixture_metadata'].items()if v['kind']in('sofa1','sofa2','armchair1','armchair2')]:
  q=Q(u['fixtures'][k]);cx,cy=(q[0]+q[2])/2,(q[1]+q[3])/2
  living.append({'id':k+'.one_person_study','fixture_id':k,'places':1,'occupied_body':list(map(S,[cx-F('.35'),cy-F('.35'),cx+F('.35'),cy+F('.35')])),'source_basis':'Conservative one distinct person-body study per actual furniture item, not capacity inferred from sofa length; seated transfer unvalidated','access_activity_id':k+'_front'})
 u['public_program']['capacity']={'residents':sum(s['places']for s in sleeping),'sleeping_places':sleeping,'dining_seats':dining,'living_seats':living,'source_basis':'D07/A9 instance-bound design program; no assumption of actual residents; all functional scenarios remain independently gated'}
 return u
