"""Kitchen-only public dining interface, never a general private-access waiver."""
def parts(model,unit,role,opening_id=None):
 from checker114 import rect
 uid=unit['id'];logical=model.get('logical_regions',{}).get(role,{})
 if role==uid+'.bedroom_public_access':
  from bedroom_approach_audit123 import examine
  r=examine(model,unit,role,opening_id)
  if r['errors']:raise ValueError(';'.join(r['errors']))
  return r['parts']
 if role==uid+'.private_access':
  from private_domain121 import examine
  if logical.get('unit')!=uid or logical.get('kind')!='BOUND_PRIVATE_DOMAIN121'or 'source_roles'in logical:raise ValueError('PRIVATE_DOMAIN_ROLE_BINDING')
  ds=[d for d in model.get('private_domains',[])if d.get('unit')==uid]
  if len(ds)!=1 or logical.get('parts')!=ds[0].get('parts'):raise ValueError('PRIVATE_DOMAIN_EXACT_PARTS')
  checked=examine(model)
  if checked['errors']or checked['pending']:raise ValueError('PRIVATE_DOMAIN_NOT_VERIFIED')
  allowed_openings=set()
  for rec in model.get('module_placements',[]):
   if rec.get('unit_id')!=uid or uid+'.'+rec.get('room_id','')not in ds[0]['bedrooms']:continue
   if rec['module'].get('schema')not in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118'):raise ValueError('PRIVATE_DOMAIN_SOURCE_SCHEMA')
   mapping=rec['id_map']
   if mapping.get('M.public_access')!=role:raise ValueError('PRIVATE_DOMAIN_SOURCE_ROLE_MAP')
   allowed_openings.update(mapping[o['id']]for o in rec['module']['openings']if 'M.public_access'in o['connects'])
  if len(allowed_openings)!=len(ds[0]['bedrooms']):raise ValueError('PRIVATE_DOMAIN_SOURCE_OPENING_INVENTORY')
  if opening_id is not None and opening_id not in allowed_openings:raise ValueError('PRIVATE_DOMAIN_OTHER_OPENING_USE')
  for o in model['openings']:
   if role in o['connects']and(o['id']not in allowed_openings or len(set(o['connects'])&set(ds[0]['bedrooms']))!=1):raise ValueError('PRIVATE_DOMAIN_NONBEDROOM_CONNECTION')
  return [rect(q)for q in ds[0]['parts']]
 if role==uid+'.public_access':allowed=['living','entry_circulation']
 elif role==uid+'.kitchen_public_access':
  allowed=['living','entry_circulation','dining']
  recs=[p for p in model.get('module_placements',[])if p['unit_id']==uid and p['room_id']=='kitchen'and p['module'].get('schema')=='KITCHEN_MODULE117']
  if len(recs)!=1:raise ValueError('KITCHEN_PUBLIC_SOURCE_MODULE_MISSING')
  rec=recs[0];mapping=rec['id_map'];source=rec['module']
  if mapping.get('K.public_access')!=role:raise ValueError('KITCHEN_PUBLIC_SOURCE_ROLE_MAP')
  allowed_openings={mapping[o['id']]for o in source['openings']if 'K.public_access'in o['connects']}
  if opening_id is not None and opening_id not in allowed_openings:raise ValueError('KITCHEN_PUBLIC_USED_BY_OTHER_OPENING')
  for o in model['openings']:
   if role in o['connects']and(o['id']not in allowed_openings or set(o['connects'])!={role,uid+'.kitchen'}):raise ValueError('KITCHEN_PUBLIC_OTHER_ROLE_CONNECTION')
 else:raise ValueError('UNKNOWN_PUBLIC_ROLE_TYPE')
 if logical.get('unit')!=uid or logical.get('source_roles')!=allowed or 'parts'in logical:raise ValueError('UNAUTHORIZED_LOGICAL_ROLE_UNION')
 if any(not unit['rooms'].get(k)for k in allowed):raise ValueError('PUBLIC_SOURCE_ROOM_MISSING')
 return [rect(q)for k in allowed for q in unit['rooms'][k]]
