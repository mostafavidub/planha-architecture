"""Reconstructed357 four-relation geometry closure. Not recovered297 implementation.
Current source-profile conservative scenario only; author233 parent scope pending.
"""
from fractions import Fraction as F
import time
from common import rows,digest
from modules_spatial import rect,intersection,union_area,source_sweeps,difference
from living_closure367 import evaluate as living

def point(p):
 if type(p)is not list or len(p)!=2 or any(type(x)not in(str,int)for x in p):raise ValueError('EXACT_POINT')
 return tuple(map(F,p))
def bbox_points(ps,pad=F(0)):
 ps=[point(p)for p in ps];return min(p[0]for p in ps)-pad,min(p[1]for p in ps)-pad,max(p[0]for p in ps)+pad,max(p[1]for p in ps)+pad

def transformed_rect(raw,transform):
 r=rect(raw);matrix=transform['matrix'];t=point(transform['translation'])
 if len(matrix)!=2 or any(len(row)!=2 for row in matrix)or any(v not in(-1,0,1)for row in matrix for v in row):raise ValueError('SOURCE_ISOMETRY')
 if any(sum(abs(v)for v in row)!=1 for row in matrix)or any(sum(abs(matrix[i][j])for i in(0,1))!=1 for j in(0,1)):raise ValueError('SOURCE_ISOMETRY')
 ps=[(matrix[0][0]*x+matrix[0][1]*y+t[0],matrix[1][0]*x+matrix[1][1]*y+t[1])for x in(r[0],r[2])for y in(r[1],r[3])]
 return min(x for x,y in ps),min(y for x,y in ps),max(x for x,y in ps),max(y for x,y in ps)

def evaluate(envelope,result,groups,seconds=8):
 start=time.monotonic();out={'rule_id':'GUEST_ROUTE_INDEPENDENCE','verdict':'UNKNOWN','parent_complete':False,'evidence':{},'missing':[]}
 def need(x,c):
  if not x:raise ValueError(c)
 try:
  need(type(seconds)in(int,float)and 0<seconds<=10,'BOUNDED_BUDGET');m=envelope['packet']['world_model'];req=rows(m,result['raw_fresh_report']);base=digest([envelope,result,groups])
  intr=living(envelope,result,groups,min(seconds,6));need(intr['verdict']=='PASS_SCOPED_INTRINSIC_LIVING','SAME_FRESH_SOURCE_INTRINSIC_PREREQUISITES')
  need(F(m['profile']['body_m'])==F('.7'),'SOURCE_PROFILE_ONLY');body=F('.7');half=body/2;unitrows=[]
  for u in m['units']:
   uid=u['id'];root=point(u['entry_point']);owner=[rect(x)for x in u['ownership']];network=next(r for r in intr['evidence']['network']['rows']if r['unit']==uid)
   need(root==tuple(map(F,network['source_root'])),'SOURCE_ROOT')
   paths={'entry_living':u['scenario_routes']['guest_living'],'entry_dining':u['scenario_routes']['guest_dining'],'entry_WC':u['routes']['WC_front']};paths['living_dining']=list(reversed(paths['entry_living']))+paths['entry_dining'][1:]
   destinations=u['public_program']['destinations'];endpoints={}
   for rel,name in(('entry_living','guest_living'),('entry_dining','guest_dining')):
    d=destinations[name];need(d['fixture_id']in u['fixtures']and d['activity_id']in u['activities'],'ACTUAL_DESTINATION_INSTANCE');a=rect(u['activities'][d['activity_id']]);p=point(paths[rel][-1]);pose=(p[0]-half,p[1]-half,p[0]+half,p[1]+half)
    need(union_area([z for q in[a]if(z:=intersection(q,pose))])==body*body,'FULL_SOURCE_DESTINATION_POSE');endpoints[rel]=p
   need(endpoints['entry_living']==tuple(map(F,network['targets'][destinations['guest_living']['fixture_id']])),'ACTUAL_LIVING_TARGET')
   dp=u['dining_module_placement'];dm=dp['module'];need(dp['module_hash']==digest(dm),'DINING_MODULE_HASH');need(dm['schema']in('SIX_PLACE_PLANAR_SOURCE_STUDY_V1','DINING_CAPACITY_MODULE118_PROPOSAL'),'SOURCE_DINING_PROFILE')
   destination=destinations['guest_dining'];source_fixture=next((k for k,v in dp['id_map'].items()if v==destination['fixture_id']),None);seat=[x for x in dm['seating']['instances']if x['fixture_id']==source_fixture];need(len(seat)==1,'DINING_TARGET_INSTANCE')
   standing=transformed_rect(seat[0]['rise_transfer']['standing_body'],dp['transform']);need(standing==rect(u['activities'][destination['activity_id']]),'SOURCE_DINING_STANDING_GEOMETRY');need(endpoints['entry_dining']==((standing[0]+standing[2])/2,(standing[1]+standing[3])/2),'SOURCE_DINING_CENTER')
   bp=[p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath'];need(len(bp)==1 and bp[0]['module_hash']==digest(bp[0]['module']),'SOURCE_BATH_MODULE');bp=bp[0]
   need(bp['module']['schema']=='BATHROOM_MODULE117'and bp['id_map'].get('WC_front')=='WC_front','SOURCE_WC_INSTANCE')
   wc=rect(u['activities']['WC_front']);need(wc==transformed_rect(bp['module']['unit']['activities']['WC_front'],bp['transform']),'SOURCE_WC_STANDING_GEOMETRY');wcpoint=((wc[0]+wc[2])/2,(wc[1]+wc[3])/2);need(point(u['route_targets']['WC_front'])==wcpoint,'SOURCE_WC_ACTIVITY_TARGET');endpoints['entry_WC']=wcpoint;endpoints['living_dining']=endpoints['entry_dining']
   pd=[d for d in m['private_domains']if d['unit']==uid];need(len(pd)==1,'SOURCE_PRIVATE_DOMAIN_INVENTORY');pd=pd[0]
   need(set(pd['bedrooms'])=={uid+'.'+k for k in u['rooms']if k.startswith('bed')},'SOURCE_PRIVATE_BED_INVENTORY');pa=[rect(q)for q in pd['parts']];pb=[rect(q)for q in u['rooms']['private_circulation']]
   need(not difference(pa,pb)and not difference(pb,pa),'FULL_PRIVATE_DOMAIN_UNION_BINDING')
   obs=[('wall:'+k,rect(q))for k,q in m['walls'].items()]+[(v['id']+'.fixture:'+k,rect(q))for v in m['units']for k,q in v['fixtures'].items()]
   obs += [('private:'+k,rect(q))for k,rs in u['rooms'].items()if k.startswith('bed')or k in('private_circulation','kitchen')for q in rs]
   obs += [('door_open:'+o['opening_id'],rect(o['open_panel']))for o in m['operations']['doors']]
   obs += [('occupied_living',rect(s['occupied_body']))for s in u['public_program']['capacity']['living_seats']]
   for op in m['operations']['dining_chairs']:
    if op['unit']!=uid:continue
    a,b=rect(op['closed_rect']),rect(op['open_rect']);obs += [('dining_occupied',rect(op['occupied_body'])),('dining_pull',(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))]
   ks=[k for k in m['operations']['kitchen']if k['unit']==uid];need(len(ks)==1,'SOURCE_KITCHEN_INVENTORY');k=ks[0];need(k['profile']=='REFERENCE113_ESSENTIAL_KITCHEN_V1'and F(k['assumptions']['body_m'])==body,'SOURCE_KITCHEN_PROFILE')
   # Conservative enclosures of complete quarter-turn leaf and actor/hand/object
   # trajectories. These may overreject a stored path; cannot create false clear.
   f=k['fridge'];need(f['angle_range_degrees']==[0,90]and f['interval_count']==360,'SOURCE_QUARTER_TURN')
   hx,hy=point(f['hinge']);rad=F(f['leaf_radius_m'])+F(f['leaf_half_thickness_m']);obs.append(('fridge_full_leaf_enclosure',(hx-rad,hy-rad,hx+rad,hy+rad)))
   obs.append(('fridge_actor_enclosure',bbox_points([f['closed_actor'],f['open_actor']],half)))
   obs.append(('fridge_hand_object_enclosure',bbox_points([f['closed_actor'],f['open_actor'],f['hinge'],f['shelf_target'],f['held_target']],F(f['object_half_size_m']))))
   need(set(k['drawers'])=={'sink','prep'},'SOURCE_DRAWERS')
   for d in k['drawers'].values():
    a,b=rect(d['closed_tray']),rect(d['open_tray']);obs.append(('drawer_tray',(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))));obs.append(('drawer_actor',bbox_points([d['closed_actor'],d['open_actor']],half)));obs.append(('drawer_hand_object',bbox_points([d['closed_actor'],d['open_actor'],d['grip_closed'],d['grip_open'],d['storage_target'],d['held_target']],F(d['object_half_size_m']))))
   for st in k['workstations']:
    a=rect(st['actor_rect']);obs.append(('kitchen_station_actor',a));p=point(st['hand_point']);obs.append(('kitchen_station_hand',(min(a[0],p[0]),min(a[1],p[1]),max(a[2],p[0]),max(a[3],p[1]))))
   for rel,path in paths.items():
    need(time.monotonic()-start<seconds,'CLOSURE_DEADLINE');need(point(path[0])==(endpoints['entry_living']if rel=='living_dining'else root)and point(path[-1])==endpoints[rel],'SOURCE_RELATION_ENDPOINT')
    collision=[]
    for i,s in enumerate(source_sweeps(path,body)):
     need(union_area([z for q in owner if(z:=intersection(q,s))])==union_area([s]),'PATH_OUTSIDE_OWNER')
     for kind,q in obs:
      if(z:=intersection(s,q)):collision.append({'segment':i,'obstacle':kind,'intersection':list(map(str,z))})
    unitrows.append({'unit':uid,'relation':rel,'verdict':'PASS_SOURCE_CONSERVATIVE_PATH'if not collision else'UNKNOWN_STORED_PATH_BLOCKED_NOT_GLOBAL_INFEASIBILITY','collisions':collision,'body_m':str(body),'scenario':'OPEN_TRANSIT_DOORS; ALL_DECLARED_OCCUPIED_CHAIRS; CONSERVATIVE_COMPLETE_SOURCE_KITCHEN_ENCLOSURES; PRIVATE_EXCLUSION'})
  need(digest([envelope,result,groups])==base,'INPUT_MUTATION');ready=all(r['verdict']=='PASS_SOURCE_CONSERVATIVE_PATH'for r in unitrows)
  out.update(verdict='PASS_SCOPED_FOUR_SOURCE_GUEST_RELATIONS'if ready else'UNKNOWN',missing=['AUTHOR233_APPLICABILITY_AND_SCOPE_AUDIT_PENDING']if ready else['SOURCE_SCENARIO_STORED_PATH_CLOSURE_INCOMPLETE'],evidence={'model_hash':digest(m),'base_fresh_digest':digest(result),'relations':unitrows,'intrinsic_closure_digest':digest(intr)},scope='CURRENT_RECOVERED_SOURCE_PROFILE_FOUR_RELATIONS_NOT_PARENT_Q06_ADMISSION')
 except (ValueError,KeyError,TypeError,IndexError,AttributeError,StopIteration)as e:out['missing']=['CLOSURE_BLOCKED:'+str(e)]
 out['elapsed_seconds']=time.monotonic()-start;return out
