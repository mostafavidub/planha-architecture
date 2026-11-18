"""Independent exact continuous axis-aligned dining study; no producer oracle.
Own-seat support is reported, not silently treated as a walkable fixture.
"""
from public_program_audit118 import F,q,hit,covered,digest,examine_dining_module

def motion(a,b):
 a,b=q(a),q(b);d=(b[0]-a[0],b[1]-a[1])
 if (a[2]-a[0],a[3]-a[1])!=(b[2]-b[0],b[3]-b[1]) or d[0]*d[1]:raise ValueError('NONRIGID_OR_DIAGONAL')
 return (min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))

def examine(module):
 if module.get('schema')=='SIX_PLACE_PLANAR_SOURCE_STUDY_V1':
  from dining6_audit121 import examine as six_audit
  r=six_audit(module)
  return {'errors':r['errors'],'pending':[],'evidence':r}
 base=examine_dining_module(module);errors=list(base['errors']);rows=[];contacts=[];all_sweeps=[]
 try:
  floor=[(F(0),F(0),F(module['width']),F(module['depth']))];fs={k:q(v)for k,v in module['fixtures'].items()};seats=module['seating']['instances']
  occupied={s['fixture_id']:q(s['occupied_body'])for s in seats}
  for s in seats:
   fid=s['fixture_id'];r=s['rise_transfer'];segments=r['segments'];prev_a=occupied[fid];prev_c=q(s['closed_rect'])
   if len(segments)!=2 or not r.get('other_seats_remain_occupied'):raise ValueError('SCENARIO_INCOMPLETE')
   if [z.get('phase')for z in segments]!=['seated_pull','rise_and_side_exit_study']:raise ValueError('UNSUPPORTED_CONTACT_TASK')
   if not hit(prev_a,prev_c):raise ValueError('NOT_ACTUAL_SEATED_SUPPORT')
   if q(r['closed_occupied_body'])!=prev_a:raise ValueError('OCCUPIED_BINDING')
   for i,seg in enumerate(segments):
    a,b=q(seg['actor_start']),q(seg['actor_end']);c,d=q(seg['chair_start']),q(seg['chair_end'])
    if a!=prev_a or c!=prev_c:raise ValueError('DISCONTINUOUS_WITNESS')
    if (a[2]-a[0],a[3]-a[1])!=(F('.7'),F('.7')):raise ValueError('BODY_RESIZED')
    if i==0:
     de=tuple(F(v)for v in s['translation'])
     if tuple(b[j]-a[j]for j in(0,1))!=de or d!=q(s['pulled_rect']):raise ValueError('ACTOR_CHAIR_PULL_BINDING')
    elif c!=d or b!=q(r['standing_body']):raise ValueError('EXIT_BINDING')
    else:
     pull=tuple(F(v)for v in s['translation']);exit_delta=(b[0]-a[0],b[1]-a[1])
     if exit_delta==(0,0)or sum(pull[j]*exit_delta[j]for j in(0,1))!=0:raise ValueError('EXIT_NOT_SIDEWAYS_FROM_PULLED_SEAT')
    sa,sc=motion(a,b),motion(c,d);all_sweeps.extend([sa,sc])
    obstacles={**{k:v for k,v in fs.items()if k!=fid},**{'occupied:'+k:v for k,v in occupied.items()if k!=fid}}
    for kind,sweep in [('actor',sa),('chair',sc)]:
     if not covered(sweep,floor):errors.append({'code':'DINING_CONTINUOUS_OUTSIDE','seat':fid,'phase':i,'object':kind})
     for oid,ob in obstacles.items():
      if hit(sweep,ob):errors.append({'code':'DINING_CONTINUOUS_COLLISION','seat':fid,'phase':i,'object':kind,'obstacle':oid})
    if hit(sa,sc):contacts.append({'seat':fid,'phase':i,'kind':'SEATED_SUPPORT'if i==0 else'TASK_SPECIFIC_SEAT_EXIT_CONTACT','own_chair_intersection':True})
    if i==1 and hit(b,d):errors.append({'code':'STANDING_BODY_STILL_IN_OWN_CHAIR','seat':fid})
    rows.append({'seat':fid,'phase':i,'actor_sweep':list(map(str,sa)),'chair_sweep':list(map(str,sc)),'other_occupied_seats':len(occupied)-1})
    prev_a,prev_c=b,d
   if q(r['pulled_occupied_body'])!=q(segments[0]['actor_end']):raise ValueError('PULLED_BODY_BINDING')
  envelope=(min(s[0]for s in all_sweeps),min(s[1]for s in all_sweeps),max(s[2]for s in all_sweeps),max(s[3]for s in all_sweeps))
 except (KeyError,ValueError,TypeError,IndexError)as e:errors.append({'code':'DINING_MOTION_MALFORMED','detail':str(e)});envelope=None
 return {'errors':errors,'pending':['DINING_GUEST_DESTINATION_ROUTE_REQUIRED','DINING_SERVING_ROUTE_REQUIRED'],'evidence':{'model_hash':digest(module),'geometry_status':'FAIL_SCOPED'if errors else'PLANAR_SEAT_ACCESS_STUDY','scenario':'One seat pulls and exits while the other three stay occupied; reverse path is same planar witness. Not simultaneous four-seat movement.','continuous_witnesses':rows,'own_seat_contact':contacts,'actual_required_envelope':list(map(str,envelope))if envelope else None,'minimum_envelope_dimensions':[str(envelope[2]-envelope[0]),str(envelope[3]-envelope[1])]if envelope else None,'scope':'Exact orthogonal sweeps, tangency allowed. Minimum is only for these supplied trajectories, not global ergonomic minimum. Own-seat overlap is allowed only for this bound seated-pull/seat-exit task, never public walking. Vertical movement, support forces and ergonomic suitability are NOT_VERIFIED.','accepted':False}}

def examine_whole(model):
 """Bind every planar seat task into actual whole obstacles and ownership."""
 errors=[];pending=[];rows=[]
 try:
  walls={k:q(v)for k,v in model['walls'].items()}
  for u in model['units']:
   p=u['dining_module_placement'];m=p['module'];local=examine(m)
   if digest(m)!=p['module_hash']:raise ValueError('MODULE_HASH')
   errors.extend(local['errors']);mat=[[F(str(x))for x in r]for r in p['transform']['matrix']];t=list(map(F,p['transform']['translation']))
   from d4_contract125 import matrix as d4_matrix
   mat=d4_matrix(mat)
   def point(x,y):return(mat[0][0]*x+mat[0][1]*y+t[0],mat[1][0]*x+mat[1][1]*y+t[1])
   def rect(r):
    r=q(r);pts=[point(x,y)for x in(r[0],r[2])for y in(r[1],r[3])];return(min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts))
   fs={k:q(v)for k,v in u['fixtures'].items()};owner=list(map(q,u['ownership']));ids=p['id_map']
   if len(set(ids.values()))!=len(m['fixtures']):raise ValueError('FIXTURE_ID_MAP')
   for k,v in m['fixtures'].items():
    if rect(v)!=fs[ids[k]]:raise ValueError('ACTUAL_FIXTURE_BINDING')
   occupied={ids[s['fixture_id']]:rect(s['occupied_body'])for s in m['seating']['instances']}
   ops={o['fixture_id']:o for o in model['operations']['dining_chairs']if o['unit']==u['id']}
   if set(ops)!=set(occupied):raise ValueError('WHOLE_SEAT_INVENTORY')
   for s in m['seating']['instances']:
    fid=ids[s['fixture_id']];op=ops[fid];r=s['rise_transfer']
    if op['source_module_hash']!=p['module_hash']or q(op['closed_rect'])!=rect(s['closed_rect'])or q(op['open_rect'])!=rect(s['pulled_rect'])or q(op['occupied_body'])!=occupied[fid]:raise ValueError('WHOLE_OPERATION_BINDING')
    local_delta=list(map(F,s['translation']));expected_delta=tuple(sum(mat[i][j]*local_delta[j]for j in range(2))for i in range(2))
    if tuple(map(F,op['translation']))!=expected_delta:raise ValueError('WHOLE_PULL_VECTOR')
    a=rect(r['pulled_occupied_body']);b=rect(r['standing_body']);expected=[((z[0]+z[2])/2,(z[1]+z[3])/2)for z in(a,b)]
    if [tuple(map(F,v))for v in op['egress_route']]!=expected:raise ValueError('WHOLE_EGRESS_BINDING')
    obstacles={**walls,**{'fixture:'+k:v for k,v in fs.items()if k!=fid},**{'occupied:'+k:v for k,v in occupied.items()if k!=fid}}
    for i,seg in enumerate(r['segments']):
     for kind in('actor','chair'):
      sweep=motion(rect(seg[kind+'_start']),rect(seg[kind+'_end']))
      if not covered(sweep,owner):errors.append({'code':'WHOLE_DINING_OUTSIDE','unit':u['id'],'seat':fid,'phase':i,'object':kind})
      for key,ob in obstacles.items():
       if hit(sweep,ob):errors.append({'code':'WHOLE_DINING_COLLISION','unit':u['id'],'seat':fid,'phase':i,'object':kind,'obstacle':key})
    rows.append({'unit':u['id'],'seat':fid,'standing_body':list(map(str,b)),'source_module_hash':p['module_hash'],'other_occupied_seats':len(occupied)-1})
 except (KeyError,ValueError,TypeError,IndexError)as e:errors.append({'code':'WHOLE_DINING_MALFORMED','detail':str(e)})
 return {'errors':errors,'pending':pending,'evidence':{'status':'FAIL_SCOPED'if errors else'PLANAR_SEAT_ACCESS_STUDY','model_hash':digest(model),'seats':rows,'scope':'Sequential seating/pull/side-exit with three other seats occupied, rigid .7 body and .4 pull. Only own-seat task contact is allowed. Public walking has no chair exception. Height, support forces and real ergonomics NOT_VERIFIED; not whole-plan approval.','accepted':False}}
