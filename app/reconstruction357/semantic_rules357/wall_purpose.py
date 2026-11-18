"""Reconstructed357 constructive per-wall purpose subclaims; no parent approval.
No wall is presumed added, and no universal removal necessity is claimed.
"""
import ast,sys,types,time,hashlib
from pathlib import Path
from fractions import Fraction as F
from common import rows,digest
from modules_spatial import rect,intersection,difference,union_area
from guest_closure import transformed_rect
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'planha_general150_runtime_work'
def touches(a,b):
 return ((a[2]==b[0]or b[2]==a[0])and min(a[3],b[3])>max(a[1],b[1]))or((a[3]==b[1]or b[3]==a[1])and min(a[2],b[2])>max(a[0],b[0]))
def source_base(envelope):
 """Execute original fixed-envelope/core assembly prefix only, before modules/routes."""
 if envelope['packet']['family']!='FRONT_REAR':raise ValueError('BASE_WORLD_FRAME_UNSUPPORTED')
 p=SRC/'assemble114.py';data=p.read_bytes();pins=envelope['generation_context']['source_files']
 if hashlib.sha256(data).hexdigest()!=pins['assemble114.py']:raise ValueError('ASSEMBLY_SOURCE_PIN')
 tree=ast.parse(data);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='assemble');stop=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='uid'and any(isinstance(x,ast.FunctionDef)and x.name=='tr'for x in n.body));fn.body=fn.body[:stop]+[ast.Return(value=ast.Name(id='m',ctx=ast.Load()))]
 tree=ast.fix_missing_locations(tree);mod=types.ModuleType('_wall357_source');mod.__file__=str(p);sys.path.insert(0,str(SRC));exec(compile(tree,str(p),'exec'),mod.__dict__)
 proposal=envelope['generation_context']['construction_trace']['proposal'];base=mod.assemble(F(envelope['raw']['W']),F(envelope['raw']['L']),envelope['packet']['core'],proposal)
 return base,{'file':'assemble114.py','sha256':pins['assemble114.py'],'selector':'assemble: original prefix before per-unit module install; no solver/checker invoked'}
def source_hall(envelope):
 p=envelope['generation_context']['construction_trace']['proposal']
 if (p.get('ordered_macro')or{}).get('kind')!='PARAMETRIC_THREE_SOURCE_ROOMS_REAL_PRIVATE_HALL129':return None
 path=SRC/'private_hall_producer121.py';data=path.read_bytes();sha='7a8daecd2fa5b2dc1e6ddefc5f66e091b37a20e29930303a241d4fce18cc7229'
 if hashlib.sha256(data).hexdigest()!=sha:raise ValueError('HALL_SOURCE_PIN')
 tree=ast.parse(data);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='install');stop=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='gross'for t in n.targets));fn.body=fn.body[:stop]
 sys.path.insert(0,str(SRC));mod=types.ModuleType('_hall357_source');exec(compile(ast.fix_missing_locations(tree),str(path),'exec'),mod.__dict__);m={'walls':{},'wall_hosts':{},'source_wall_hosts':{}}
 for uid in ('A','B'):mod.install(m,{'id':uid},envelope['packet']['core'],p,F(envelope['raw']['L']))
 return m,{'file':path.name,'sha256':sha,'selector':'install prefix before floor and routing; exact same source constructor geometry'}
def material_boundary_support(source,wall_id):
 """Exact source-host material connectivity to a used source-room boundary.
 This is a constructive material/function claim, not minimum-wall necessity.
 Positive face contact required; corner-only and empty cavity are not material.
 """
 q=rect(source['walls'][wall_id]);domains=[(k,rect(r))for k,rs in source['unit']['rooms'].items()for r in rs]
 for hid,hraw in source['wall_hosts'].items():
  h=rect(hraw)
  if difference([q],[h]):continue
  pieces={k:z for k,r in source['walls'].items()if(z:=intersection(rect(r),h))}
  reached={wall_id};queue=[wall_id];parents={wall_id:None}
  while queue:
   k=queue.pop(0);a=pieces[k];adj=[name for name,b in domains if touches(a,b)]
   if adj:
    chain=[];cur=k
    while cur is not None:chain.append(cur);cur=parents[cur]
    return {'host_id':hid,'host_geometry':hraw,'source_material_chain':list(reversed(chain)),'material_rectangles':{n:source['walls'][n]for n in chain},'actual_adjacent_source_regions':adj,'source_host_thickness_m':str(min(h[2]-h[0],h[3]-h[1])),'proof':'Exact source wall lies within source host; positive-area material overlap or positive-length shared face connects it to an actually used source-region boundary. No empty cavity is material and no necessity claim is made.'}
   for j,b in pieces.items():
    if j not in reached and (intersection(a,b)or touches(a,b)):reached.add(j);parents[j]=k;queue.append(j)
 return None
def module_claims(m,requirements):
 claims={};units={u['id']:u for u in m['units']}
 for p in m['module_placements']:
  source=p['module'];uid=p['unit_id'];u=units[uid];room=p['room_id'];schema=source['schema'];kind={'PRIVATE_ROOM_MODULE116':'BEDROOM','PRIVATE_TWIN_ROOM_MODULE118':'BEDROOM','BATHROOM_MODULE117':'BATH','KITCHEN_MODULE117':'KITCHEN'}.get(schema)
  if kind is None:continue
  if digest(source)!=p['module_hash']:raise ValueError('MODULE_HASH')
  deps=['fixture_inventory_use','body_route_sweeps','door_operation']+({'BEDROOM':['closet_operation'],'BATH':['bath_service_operation'],'KITCHEN':['kitchen_essential_operation']}[kind])
  if any(requirements[d]['status']!='PASS_LIMITED'for d in deps):raise ValueError('MODULE_FUNCTION_UNVERIFIED')
  domains=[]
  for name,rs in source['unit']['rooms'].items():
   for r in rs:domains.append((name,transformed_rect(r,p['transform'])))
  for name,r in source['unit']['fixtures'].items():
   if rect(u['fixtures'][p['id_map'][name]])!=transformed_rect(r,p['transform']):raise ValueError('SOURCE_FIXTURE_JOIN')
  for name,r in source['unit']['activities'].items():
   if rect(u['activities'][p['id_map'][name]])!=transformed_rect(r,p['transform']):raise ValueError('SOURCE_ACTIVITY_JOIN')
  for name,r in source['walls'].items():
   wid=p['id_map'][name];q=transformed_rect(r,p['transform'])
   if rect(m['walls'][wid])!=q:raise ValueError('SOURCE_WALL_JOIN')
   adjacent=[name for name,r in domains if touches(q,r)];material=material_boundary_support(source,name) if not adjacent else None
   # Entrance/access walls can serve the actual source module but remain a
   # narrower subclaim, not independent proof of circulation necessity.
   claims[wid]={'verdict':'PASS_SOURCE_FUNCTIONAL_MODULE_BOUNDARY'if adjacent else'PASS_SOURCE_HOST_MATERIAL_FUNCTIONAL_BOUNDARY'if material else'UNKNOWN_NO_DIRECT_SOURCE_FUNCTIONAL_BOUNDARY','kind':kind,'unit':uid,'room':room,'source_module_hash':p['module_hash'],'source_wall_id':name,'transform':p['transform'],'actual_adjacent_source_regions':adjacent,'source_material_boundary_proof':material,'function_evidence':{d:digest(requirements[d])for d in deps},'purpose':'SOURCE_REQUIRED_ROOM_ENCLOSURE_OR_ACTUAL_MODULE_ACCESS_INTERFACE','necessity_or_counterfactual_claimed':False}
 return claims
def evaluate(envelope,result,origin_record=None):
 start=time.monotonic();m=envelope['packet']['world_model'];out={'schema':'WALL_PURPOSE357_RECONSTRUCTED','parent_complete':False,'admission_allowed':False,'model_hash':digest(m),'base_fresh_digest':digest(result),'rows':[]}
 try:
  if result['candidate_digest']!=digest(envelope):raise ValueError('CANDIDATE_BINDING')
  req=rows(m,result['raw_fresh_report']);origin_envelope=envelope
  if origin_record is not None:
   if envelope.get('input_record_digest')!=digest(origin_record)or envelope.get('outer_trace_digest')!=digest(origin_record['trace'])or digest(origin_record['candidate']['packet'])!=digest(envelope['packet']):raise ValueError('EXPLICIT357_ORIGIN_RECORD_BINDING')
   c=origin_record['candidate'];origin_envelope={'raw':c['request'],'packet':c['packet'],'generation_context':c['generation_context']}
   out['source_origin_record_digest']=digest(origin_record);out['artifact_reassessment_only']=True
  base,origin=source_base(origin_envelope);claims=module_claims(m,req)
  for d in('core_concept','unit_independence','partition_ledger','opening_hosts','wall_network','body_route_sweeps'):
   if req[d]['status']!='PASS_LIMITED':raise ValueError('BASE_FUNCTION:'+d)
  for wid,q0 in base['walls'].items():
   if rect(q0)!=rect(m['walls'][wid]):raise ValueError('CONSTRUCTOR_BASE_WALL_JOIN')
   # Role is taken from executed source emission and exact role-region boundary,
   # not inferred solely from the final wall ID.
   q=rect(q0);adj=[]
   for u in m['units']:
    if any(touches(q,rect(r))for r in u['ownership']):adj.append('unit:'+u['id'])
   for name,rs in m['common_spaces'].items():
    rs=rs if type(rs[0])is list else[rs]
    if any(touches(q,rect(r))for r in rs):adj.append('core:'+name)
   envelope_face=q[0]==0 or q[1]==0 or q[2]==F(origin_envelope['raw']['W'])or q[3]==F(origin_envelope['raw']['L'])
   claims[wid]={'verdict':'PASS_CONSTRUCTOR_BOUNDARY_WITH_ACTUAL_PROTECTED_USE'if adj else'UNKNOWN_NO_ADJACENT_ROLE','kind':'ENVELOPE'if envelope_face else'UNIT_OR_CONCEPT_CORE_INTERFACE','source_origin':origin,'actual_adjacent_roles':adj,'function_evidence':{d:digest(req[d])for d in('core_concept','unit_independence','partition_ledger','body_route_sweeps')},'technical_core_approval':False,'necessity_or_counterfactual_claimed':False}
  # Every host is bound to an actual module transform or original prefix.
  hosts={k:rect(v)for k,v in base['wall_hosts'].items()}
  for p in m['module_placements']:
   for k,v in p['module'].get('wall_hosts',{}).items():hosts[p['id_map'][k]]=transformed_rect(v,p['transform'])
  for k,v in hosts.items():
   if rect(m['wall_hosts'][k])!=v:raise ValueError('SOURCE_HOST_JOIN')
  hall=source_hall(origin_envelope)
  if hall:
   h,horigin=hall
   for wid,q in h['walls'].items():
    if rect(m['walls'][wid])!=rect(q)or rect(m['wall_hosts'][wid])!=rect(h['wall_hosts'][wid]):raise ValueError('HALL_SOURCE_JOIN')
    hosts[wid]=rect(q);claims[wid]={'verdict':'UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY','kind':'EXECUTED_SOURCE_PRIVATE_ACCESS_BOUNDARY','source_origin':horigin,'source_private_grouping_digest':digest(req['private_grouping']),'purpose_scope':'Actual access geometry and use exist; no necessity or alternative comparison claimed','missing':['Q04_EXCLUSIVE_CIRCULATION_NECESSITY']}
  if origin_record is not None and origin_record['trace'].get('schema')=='TRANSLATED_PRIVATE357_SOURCE_TRACE_V1':
   path=ROOT/'staging357_comparative/translated_validator.py';sha=hashlib.sha256(path.read_bytes()).hexdigest()
   if origin_record['trace']['source_inventory'].get(str(path.relative_to(ROOT)))!=sha:raise ValueError('TRANSLATED_BINDER_SOURCE_PIN')
   sys.path.insert(0,str(path.parent));mod=types.ModuleType('_wall357_translated_binder');mod.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),mod.__dict__);binding=mod.verify(m,origin_record['trace'])
   if binding['errors']:raise ValueError('TRANSLATED_SOURCE_BINDING:'+str(binding['errors']))
   for uid in ('A','B'):
    for key,r in mod.HALL.items():
     wid=uid+'.private_sidecar.'+key;hosts[wid]=rect(m['wall_hosts'][wid]);claims[wid]={'verdict':'UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY','kind':'EXACT_TRANSLATED_SOURCE136_HALL_BOUNDARY','source_origin':{'file':str(path.relative_to(ROOT)),'sha256':sha,'selector':'verify: source HALL constant + exact rigid transform + source room/domain/ports'},'source_binding':binding,'origin':origin_record['trace']['proposal']['ordered_macro']['origin'],'source_geometry':r,'source_private_grouping_digest':digest(req['private_grouping']),'missing':['Q04_EXCLUSIVE_CIRCULATION_NECESSITY'],'necessity_or_counterfactual_claimed':False}
  for wid,r in m['walls'].items():
   claim=claims.get(wid,{'verdict':'UNKNOWN_CONSTRUCTOR_HALL_PURPOSE_AND_Q04_REQUIRED','kind':'UNJOINED_SOURCE_WALL','missing':['EXACT_EXECUTED_HALL_ORIGIN','CIRCULATION_NECESSITY_IF_EXCLUSIVE']})
   out['rows'].append({'wall_id':wid,'geometry':r,'geometry_digest':digest(r),**claim})
  out.update(status='MEASURED_CONSTRUCTIVE_SUBCLAIMS_NOT_FULL_Q11_OR_Q05',source_joined_host_count=len(hosts),unjoined_host_ids=sorted(set(m['wall_hosts'])-set(hosts)),counts={v:sum(r['verdict']==v for r in out['rows'])for v in sorted({r['verdict']for r in out['rows']})},scope='Current immutable candidate. Q05 visibility separate; whole Q11 functional floor and Q04 exclusive circulation not settled. No redesign/removal alternatives were constructed, so none are falsely declared rechecked.')
 except (ValueError,KeyError,TypeError,IndexError,StopIteration)as e:out.update(status='UNKNOWN',missing=[str(e)])
 out['elapsed_seconds']=time.monotonic()-start;return out
if __name__=='__main__':
 import json
 r=json.loads((ROOT/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0];o=evaluate(r['central_envelope'],r['central_fresh_review']);Path(__file__).with_name('wall_purpose_actual357.json').write_text(json.dumps(o,indent=2));print(o.get('counts',o))
