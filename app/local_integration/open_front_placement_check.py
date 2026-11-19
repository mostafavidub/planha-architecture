"""Independent new-schema placement adapter retaining historical placement obligations.
This is not a whole model or named-rule evaluator. No old errors are filtered.
"""
from checker114 import rect,F,BODY,intersects,covered,sweeps,digest,check_module,check_twin_module,check_bathroom_module,check_kitchen_module
from open_front_kitchen_check import assess as check_open_front_module
def check_module_placements(model):
 """Bind source components to actual whole-model geometry, then recheck local
 paths against ALL neighboring solids/fixtures. No placement receipt is trusted.
 """
 errors=[];pending=[];rows=[]
 def err(code,**kw):errors.append(dict(code=code,**kw))
 try:
  units={u['id']:u for u in model['units']};walls={k:rect(q)for k,q in model['walls'].items()};allfx=[(u['id'],k,rect(q))for u in model['units']for k,q in u['fixtures'].items()];seen=set();expected_ports=set()
  for rec in model.get('module_placements',[]):
   module=rec['module'];uid=rec['unit_id'];rid=rec['room_id'];key=(uid,rid);u=units[uid];mapping=rec['id_map'];t=rec['transform'];mat=[[F(x)for x in row]for row in t['matrix']];off=list(map(F,t['translation']))
   if key in seen:err('DUPLICATE_MODULE_PLACEMENT',unit=uid,room=rid)
   seen.add(key)
   from d4_contract125 import matrix as d4_matrix
   try:mat=d4_matrix(mat)
   except ValueError:err('MODULE_ISOMETRY_NOT_ALLOWED',unit=uid,room=rid);continue
   if rec['module_hash']!=digest(module):err('MODULE_SOURCE_HASH_MISMATCH',unit=uid,room=rid)
   if (model.get('ordered_macro')or{}).get('kind')in('TURN_T133','SIDECAR_T136','PARALLEL_TWINS_BRANCH146')and rid.startswith('bed'):
    from checker_source133 import examine as examine_rotation_source
    source=rec.get('rotation_source133',{});rr=examine_rotation_source(source)
    if rr['errors']or rr['pending']or source.get('base_module')!=module:err('ROTATION_SOURCE133_BINDING',unit=uid,room=rid)
   local=check_open_front_module(module)if module.get('schema')=='KITCHEN_OPEN_FRONT_STUDY_V1'else check_kitchen_module(module)if module.get('schema')in('KITCHEN_MODULE117','KITCHEN_OPEN_FRONT_STUDY_V1')else check_bathroom_module(module)if module.get('schema')=='BATHROOM_MODULE117'else check_twin_module(module)if module.get('schema')=='PRIVATE_TWIN_ROOM_MODULE118'else check_module(module);rows.append({'unit':uid,'room':rid,'module_hash':digest(module),'local_status':local['status']})
   if local['errors']:err('SOURCE_MODULE_RECHECK_FAILED',unit=uid,room=rid,errors=local['errors'])
   pending.extend('SOURCE_MODULE:'+str(p)for p in local['pending'])
   def pt(p):return tuple(sum(mat[i][j]*F(p[j])for j in(0,1))+off[i]for i in(0,1))
   def tr(q):
    q=rect(q);a=pt(q[:2]);b=pt(q[2:]);return(min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1]))
   def same(actual,expected,field):
    if actual!=expected:err('MODULE_PLACEMENT_PHYSICAL_BINDING',unit=uid,room=rid,field=field)
   for field in('walls','wall_hosts'):
    for k,q in module[field].items():
     target=mapping.get(k)
     same(rect(model[field][target])if target in model[field]else None,tr(q),field+'.'+k)
   same([rect(q)for q in u['rooms'][rid]],[tr(q)for q in module['unit']['rooms']['kitchen'if module.get('schema')in('KITCHEN_MODULE117','KITCHEN_OPEN_FRONT_STUDY_V1')else'bath'if module.get('schema')=='BATHROOM_MODULE117'else'bed1']],'component_floor')
   apron=model.get('module_aprons',{}).get(uid+'.'+rid,[])
   same([rect(q)for q in apron],[tr(q)for q in module['unit']['rooms']['public_access']],'public_apron')
   from open_front_typed_public import parts as typed_public_parts
   private_module=module.get('schema')in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118')
   public_role=mapping.get('K.public_access')if module.get('schema')in('KITCHEN_MODULE117','KITCHEN_OPEN_FRONT_STUDY_V1')else mapping.get('M.public_access',uid+'.public_access')if private_module else uid+'.public_access'
   allowed_roles={uid+'.public_access'}|({uid+'.kitchen_public_access'}if module.get('schema')in('KITCHEN_MODULE117','KITCHEN_OPEN_FRONT_STUDY_V1')else{uid+'.private_access',uid+'.bedroom_public_access'}if private_module else set())
   if public_role not in allowed_roles:err('MODULE_PUBLIC_TYPE_NOT_ALLOWED',unit=uid,room=rid);public_role='INVALID'
   try:public=typed_public_parts(model,u,public_role)
   except ValueError as ex:err('MODULE_TYPED_PUBLIC_ROLE',unit=uid,room=rid,detail=str(ex));public=[]
   apron_host=list(public)
   if private_module and public_role==uid+'.private_access':
    # The source apron includes its own physical door-threshold strip; no
    # bedroom floor or unrelated aperture is added to the private approach.
    for source_opening in module['openings']:
     target=mapping[source_opening['id']]
     matches=[o for o in model['openings']if o['id']==target and public_role in o['connects']]
     if len(matches)==1 and rect(matches[0]['rect'])==tr(source_opening['rect']):apron_host.append(rect(matches[0]['rect']))
   for q in apron:
    if not covered(rect(q),apron_host):err('MODULE_APRON_NOT_REAL_PUBLIC_FLOOR',unit=uid,room=rid)
   for source_port in module['external_ports']:
    portid=mapping.get(source_port['id']);expected_ports.add(portid);matches=[z for z in model.get('module_ports',[])if z['id']==portid]
    if len(matches)!=1:err('MODULE_PLACED_PORT_INVENTORY',unit=uid,room=rid);continue
    actual=matches[0];same(rect(actual['rect']),tr(source_port['rect']),'port.rect');same(tuple(map(F,actual['center'])),pt(source_port['center']),'port.center')
    if actual['opening_id']!=mapping[source_port['opening_id']]or actual['role_id']!=mapping[source_port['role_id']]:err('MODULE_PLACED_PORT_ROLE_OPENING_BINDING',unit=uid,room=rid)
    c=pt(source_port['center']);body=(c[0]-BODY/2,c[1]-BODY/2,c[0]+BODY/2,c[1]+BODY/2)
    if not covered(body,public):err('PLACED_PORT_BODY_NOT_ON_PUBLIC_FLOOR',unit=uid,room=rid)
    if module.get('schema')in('KITCHEN_MODULE117','KITCHEN_OPEN_FRONT_STUDY_V1'):
     obstacles=list(walls.values())+[q for _,_,q in allfx]
     for op in model.get('operations',{}).get('dining_chairs',[]):
      if op.get('unit')!=uid:continue
      if op.get('occupied_body'):obstacles.append(rect(op['occupied_body']))
      if op.get('closed_rect')and op.get('open_rect'):
       a,b=rect(op['closed_rect']),rect(op['open_rect']);obstacles.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
     if any(intersects(body,z)for z in obstacles):err('KITCHEN_PORT_BODY_ACTUAL_OCCUPIED_COLLISION',unit=uid)
     if any(intersects(rect(a),z)for a in apron for z in obstacles):err('KITCHEN_APRON_ACTUAL_OCCUPIED_COLLISION',unit=uid)


   for k,q in module['unit']['fixtures'].items():
    target=mapping.get(k);same(rect(u['fixtures'][target])if target in u['fixtures']else None,tr(q),'fixture.'+k)
    if target in u['fixture_metadata']:
     source_md=module['unit']['fixture_metadata'][k];actual_md=u['fixture_metadata'][target]
     if actual_md['kind']!=source_md['kind']:err('MODULE_FIXTURE_KIND_BINDING',unit=uid,room=rid,fixture=target)
   for k,q in module['unit']['activities'].items():
    target=k.replace('bed1.',rid+'.');same(rect(u['activities'][target])if target in u['activities']else None,tr(q),'activity.'+k)
   for opening in module['openings']:
    target=mapping[opening['id']];matches=[o for o in model['openings']if o['id']==target]
    if len(matches)!=1:err('MODULE_OPENING_INVENTORY',unit=uid,room=rid);continue
    actual=matches[0];same(rect(actual['rect']),tr(opening['rect']),'opening.'+target)
    if actual['host_wall_id']!=mapping[opening['host_wall_id']]or actual['connects']!=[mapping.get(k,k)for k in opening['connects']]:err('MODULE_OPENING_ROLE_HOST_BINDING',opening=target)
   def compare_motion(source,actual,label):
    for field in('closed_panel','open_panel','pocket','rail_envelope'):
     if field in source:same(rect(actual[field]),tr(source[field]),label+'.'+field)
    same(tuple(map(F,actual['translation'])),tuple(sum(mat[i][j]*F(source['translation'][j])for j in(0,1))for i in(0,1)),label+'.translation')
    if 'open_transfer_points'in source:same([tuple(map(F,p))for p in actual['open_transfer_points']],[pt(p)for p in source['open_transfer_points']],label+'.open_transfer_points')
    for field in('states','continuous_actor_segments'):
     aa=actual.get(field,[]);ss=source.get(field,[])
     if len(aa)!=len(ss):err('MODULE_OPERATION_STATE_INVENTORY',field=label+'.'+field);continue
     for a,s in zip(aa,ss):
      for k in('panel_rect','actor_rect','actor_start','actor_end'):
       if k in s:same(rect(a[k]),tr(s[k]),label+'.'+field+'.'+k)
      for k in('hand_point','hand_start','hand_end'):
       if k in s:same(tuple(map(F,a[k])),pt(s[k]),label+'.'+field+'.'+k)
      for k in('fraction','t0','t1'):
       if k in s:same(F(a[k]),F(s[k]),label+'.'+field+'.'+k)
      if a.get('unit')!=uid or a.get('role_id')!=mapping.get(s.get('role_id'),s.get('role_id'))or a.get('side')!=s.get('side'):err('MODULE_OPERATION_ROLE_BINDING',field=label+'.'+field)
   for door in module['operations'].get('doors',[]):
    target=mapping[door['opening_id']];aa=[d for d in model.get('operations',{}).get('doors',[])if d['opening_id']==target]
    if len(aa)!=1:err('MODULE_DOOR_OPERATION_INVENTORY',opening=target)
    else:compare_motion(door,aa[0],target)
   for closet in module['operations'].get('closets',[]):
    target=mapping[closet['fixture_id']];aa=[d for d in model.get('operations',{}).get('closets',[])if d['unit']==uid and d['fixture_id']==target]
    if len(aa)!=1:err('MODULE_CLOSET_OPERATION_INVENTORY',fixture=target);continue
    actual=aa[0];same([rect(q)for q in actual['shell_rects']],[tr(q)for q in closet['shell_rects']],'closet.shells')
    if len(actual['panels'])!=len(closet['panels']):err('MODULE_CLOSET_HALF_INVENTORY',fixture=target)
    else:
     for s,a in zip(closet['panels'],actual['panels']):compare_motion(s,a,target+'.panel')
   for source_op in module.get('operations',{}).get('kitchen',[]):
    aa=[op for op in model.get('operations',{}).get('kitchen',[])if op['unit']==uid]
    if len(aa)!=1:err('MODULE_KITCHEN_OPERATION_INVENTORY',unit=uid);continue
    actual=aa[0];source_transform=source_op['canonical_transform'];cm=[[F(x)for x in row]for row in source_transform['matrix']];co=list(map(F,source_transform['translation']));expected_matrix=[[sum(cm[i][k]*mat[j][k]for k in(0,1))for j in(0,1)]for i in(0,1)];expected_offset=[co[i]-sum(expected_matrix[i][j]*off[j]for j in(0,1))for i in(0,1)]
    same([[F(x)for x in row]for row in actual['canonical_transform']['matrix']],expected_matrix,'kitchen.canonical_matrix');same(list(map(F,actual['canonical_transform']['translation'])),expected_offset,'kitchen.canonical_offset')
    same(tuple(map(F,actual['access_point'])),pt(source_op['access_point']),'kitchen.access')
    if actual['assumptions']!=source_op['assumptions']:err('MODULE_KITCHEN_MOTION_PARAMETER_BINDING',unit=uid)
   for source_role,region in module.get('logical_regions',{}).items():
    if 'parts'in region:
     target_role=mapping.get(source_role);actual_region=model.get('logical_regions',{}).get(target_role,{})
     same([rect(q)for q in actual_region.get('parts',[])],[tr(q)for q in region['parts']],'logical_region.'+source_role)
     if actual_region.get('unit')!=uid:err('MODULE_SERVICE_REGION_OWNER_BINDING',role=target_role)
   # Retained component paths remain usable after neighbor placement, independently
   # of the separately recomputed core-to-activity routes checked in evaluate().
   for rk,path in module['unit']['routes'].items():
    actualpath=[list(pt(p))for p in path]
    for q in sweeps(actualpath):
     if not covered(q,[rect(r)for r in u['ownership']]):err('PLACED_MODULE_ROUTE_OUTSIDE_OWNER',room=rid,route=rk)
     for wid,w in walls.items():
      if intersects(q,w):err('PLACED_MODULE_ROUTE_WALL_COLLISION',room=rid,route=rk,wall=wid)
     for fu,fk,f in allfx:
      own_service_exception=module.get('schema')=='BATHROOM_MODULE117'and fu==uid and ((rk=='WC_use'and fk==mapping.get('WC_iranian'))or(rk=='shower_use'and fk==mapping.get('shower_floor')))
      if not own_service_exception and intersects(q,f):err('PLACED_MODULE_ROUTE_FIXTURE_COLLISION',room=rid,route=rk,fixture=fu+'.'+fk)
  expected={(u['id'],k)for u in model['units']for k in u['rooms']if k.startswith('bed')or k in('kitchen','bath')}
  if seen!=expected:err('WHOLE_MODULE_BEDROOM_INVENTORY',expected=sorted(expected),actual=sorted(seen))
  actual_ports=[p['id']for p in model.get('module_ports',[])]
  if set(actual_ports)!=expected_ports or len(actual_ports)!=len(expected_ports):err('WHOLE_MODULE_PORT_INVENTORY')
 except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as ex:err('MODULE_PLACEMENT_SCHEMA_OR_GEOMETRY',detail=str(ex))
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':rows,'status':'FAIL_PLACEMENT'if errors else'NOT_EVALUATED_PLACEMENT'if pending else'PASS_PLACEMENT_SCOPED','whole_model_pass':False}

