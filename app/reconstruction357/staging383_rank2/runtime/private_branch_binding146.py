"""Independent restricted BRANCH146 source/frame/wall/private-use binding. No producer calls.
Only reviewed fixed-size rotated double/twin/twin method; never whole-plan acceptance.
"""
from fractions import Fraction as F
from frame_audit125 import digest,evaluate_core,equal,rectangle,point
from frame_circulation125 import same_union
from private_domain121 import examine as topology
from checker_source133 import examine as source_contract
from geometry114 import cells
PIN_TWIN='82e66b18d79b2b5ad3eb8aebff1ac3625ee4ac11279d44cec8950b712df901f8'
PIN_DOUBLE='c876cb026c2f227a10ed6a36ba6e49f0dc9c92fcf2c7ab300d42236ed2bf3fc1'
FIELDS={'unit','bedrooms','parts','public_interface','paths','route_failures','topology_scope'}
OPTIONAL={'functional_wall_purpose','quality_comparison'}
def rigid(r,T):
 a=T['matrix']
 if len(a)!=2 or any(len(v)!=2 for v in a) or any(F(str(v))not in(-1,0,1)for row in a for v in row)or any(sum(F(str(a[k][i]))*F(str(a[k][j]))for k in(0,1))!=int(i==j)for i in(0,1)for j in(0,1)):raise ValueError('NON_D4_SOURCE')
 return rectangle(r,T)
def interface_side(T,uid):
 n=[0,1 if uid=='A'else -1];v=[sum(F(str(T['matrix'][i][j]))*n[j]for j in(0,1))for i in(0,1)]
 return 'right'if v[0]==1 else'left'if v[0]==-1 else'top'if v[1]==1 else'bottom'
def examine(world,local,core):
 errors=[];pending=[];verified={};witness={}
 def need(ok,label):
  if not ok:errors.append(label)
 try:
  fr=evaluate_core(core);errors.extend('CORE:'+e for e in fr['errors']);T=core['world_from_local'];rigid([0,0,1,1],T)
  b=world['frame_binding125'];need(b['local_model_hash']==digest(local)and b['core_contract_hash']==digest(core)and equal(b['world_from_local'],T),'BRANCH146_FRAME_HASH')
  need(equal(local['inputs'],core['solver_inputs'])and equal(world['inputs'],core['physical_core_model']['inputs']),'BRANCH146_INPUT_FRAME')
  need({u['id']for u in local['units']}=={'A','B'}and len(local['units'])==2,'BRANCH146_UNIT_INVENTORY')
  need({u['id']for u in world['units']}=={'A','B'}and len(world['units'])==2,'BRANCH146_WORLD_UNIT_INVENTORY')
  L=F(str(local['inputs'][1]));ox=F(str(core['entry_centers']['A'][0]))-F('6.25');oy=F(str(core['units']['A'][1]))
  templates={'bed1':[F(x)for x in('6.9','.15','10.5','5.6')],'bed2':[F(x)for x in('.15','.15','5.6','4.65')],'bed3':[F(x)for x in('.15','4.8','5.6','9.3')]}
  def loc(r,uid):
   a,b,c,d=map(F,r);v=[ox+a,oy+b,ox+c,oy+d]
   return v if uid=='A'else[v[0],L-v[3],v[2],L-v[1]]
  # Immutable construction metadata is not trusted merely because both frames copy it.
  for label,m in (('local',local),('world',world)):
   macro=m['ordered_macro'];need(set(macro)=={'kind','origin','rectangles','bed_door_sides','private_interface_center_x','scope'},'BRANCH146_MACRO_SCHEMA:'+label)
   need(macro['kind']=='PARALLEL_TWINS_BRANCH146','BRANCH146_MACRO_KIND:'+label)
   need(macro['scope']=='Parallel source twins and perpendicular rotated double with actual branch hall; independent admission required','BRANCH146_MACRO_SCOPE:'+label)
   need(equal(macro['origin'],[ox,oy]),'BRANCH146_MACRO_ORIGIN:'+label)
   need(equal(macro['private_interface_center_x'],ox+F('6.25')),'BRANCH146_MACRO_CENTER:'+label)
   need(equal(macro['rectangles'],{k:loc(r,'A')for k,r in templates.items()}),'BRANCH146_MACRO_RECTANGLES:'+label)
   need(macro['bed_door_sides']=={'bed1':'top','bed2':'right','bed3':'right'},'BRANCH146_MACRO_DOOR_SIDES:'+label)
  for uid in ('A','B'):
   u=next(u for u in local['units']if u['id']==uid)
   for name,r in templates.items():
    ps=[p for p in local['module_placements']if p['unit_id']==uid and p['room_id']==name];need(len(ps)==1,'BRANCH146_BED_SOURCE_INVENTORY')
    if len(ps)!=1:continue
    p=ps[0];s=p['module'];pin=PIN_DOUBLE if name=='bed1'else PIN_TWIN
    need(digest(s)==p['module_hash']==pin,'BRANCH146_REVIEWED_SOURCE:'+uid+'.'+name)
    wrapper=p.get('rotation_source133',{});sr=source_contract(wrapper)
    need(not sr['errors']and not sr['pending']and equal(wrapper.get('base_module'),s),'BRANCH146_WRAPPER:'+uid+'.'+name)
    # Bind the actual orientation, not merely the rotated rectangular footprint.
    a,b,c,d=loc(r,'A');A={'bed1':[[0,1],[-1,0]],'bed2':[[-1,0],[0,1]],'bed3':[[-1,0],[0,1]]}[name]
    shift={'bed1':[a,d],'bed2':[c,b],'bed3':[c,b]}[name]
    if uid=='B':A=[A[0],[-v for v in A[1]]];shift=[shift[0],L-shift[1]]
    need(equal(p['transform'],{'matrix':A,'translation':shift}),'BRANCH146_EXACT_TEMPLATE_TRANSFORM:'+uid+'.'+name)
    expect=[rigid(z,p['transform'])for z in s['unit']['rooms']['bed1']]
    need(same_union(expect,[loc(r,uid)])and same_union(u['rooms'][name],expect),'BRANCH146_SOURCE_FLOOR:'+uid+'.'+name)
   for suffix,r in {'bottom':['5.6','0','6.9','.15'],'upper_stem_right':['6.75','6.75','6.9','9.45'],'branch_top':['6.75','6.75','10.8','6.9'],'branch_end':['10.65','5.6','10.8','6.9']}.items():
    key=uid+'.private_branch146.'+suffix;lr=loc(r,uid);wr=rigid(lr,T)
    for fld in('walls','wall_hosts','source_wall_hosts'):
     need(equal(local[fld].get(key),lr),'BRANCH146_LOCAL_BOUNDARY:'+fld+':'+key);need(equal(world[fld].get(key),wr),'BRANCH146_WORLD_BOUNDARY:'+fld+':'+key)
    verified[key]=list(map(str,wr))
  # Bind full module inventory/transform, not just beds or conveniently named walls.
  def records(m):
   ps=m['module_placements'];keys=[(p['unit_id'],p['room_id'])for p in ps];need(len(keys)==len(set(keys)),'DUPLICATE_MODULE_OWNER');return dict(zip(keys,ps))
  lp,wp=records(local),records(world);need(set(lp)==set(wp),'BRANCH146_WORLD_MODULE_INVENTORY');mapped=set();hostmapped=set()
  for key,p in lp.items():
   z=wp[key];need(equal(p['module'],z['module'])and p['module_hash']==z['module_hash']==digest(p['module'])and p['id_map']==z['id_map'],'BRANCH146_WORLD_MODULE_SOURCE')
   need(equal(p.get('rotation_source133'),z.get('rotation_source133')),'BRANCH146_WRAPPER_FRAME')
   # Affine composition checked on independent basis points, even symmetric modules.
   for v in([0,0],[1,0],[0,1]):need(equal(point(point(v,p['transform']),T),point(v,z['transform'])),'BRANCH146_MODULE_D4_COMPOSITION')
   for k,r in p['module']['walls'].items():
    target=p['id_map'][k];need(target not in mapped and target not in verified,'BRANCH146_DUPLICATE_WALL_OWNER');mapped.add(target)
    lr=rigid(r,p['transform']);wr=rigid(lr,T)
    for fld in('walls',):
     need(equal(local[fld].get(target),lr),'BRANCH146_LOCAL_MODULE_WALL:'+fld+':'+target);need(equal(world[fld].get(target),wr),'BRANCH146_WORLD_MODULE_WALL:'+fld+':'+target)
   for k,r in p['module']['wall_hosts'].items():
    target=p['id_map'][k];need(target not in hostmapped and target not in verified,'BRANCH146_DUPLICATE_HOST_OWNER');hostmapped.add(target)
    lr=rigid(r,p['transform']);wr=rigid(lr,T)
    for fld in ('wall_hosts','source_wall_hosts'):
     need(equal(local[fld].get(target),lr),'BRANCH146_LOCAL_MODULE_HOST:'+target);need(equal(world[fld].get(target),wr),'BRANCH146_WORLD_MODULE_HOST:'+target)
  for label,m in(('local',local),('world',world)):
   # Every residual wall contributes to exact core union. No name exemption.
   for fld in('walls','wall_hosts','source_wall_hosts'):
    residual=[r if label=='world'else rigid(r,T)for k,r in m[fld].items()if k not in (mapped if fld=='walls'else hostmapped) and k not in verified]
    need(same_union(residual,list(core['physical_core_model']['walls'if fld=='walls'else'wall_hosts'].values())),'BRANCH146_RESIDUAL_CORE:'+label+':'+fld)
   r=topology(m);errors.extend(label+':'+v for v in r['errors']);pending.extend(label+':'+v for v in r['pending']);witness[label+'_topology']=r
   need(len(m['private_domains'])==2,'BRANCH146_DOMAIN_COUNT')
   for d in m['private_domains']:
    uid=d['unit'];u=next(u for u in m['units']if u['id']==uid);role=m['logical_regions'][uid+'.private_access']
    need(role['kind']=='BOUND_PRIVATE_DOMAIN121'and role['unit']==uid and equal(role['parts'],d['parts'])and equal(u['rooms']['private_circulation'],d['parts']),'BRANCH146_PRIVATE_ROLE:'+label+':'+uid)
    for o in m['openings']:
     if any(v in o['connects']for v in d['bedrooms']):need(uid+'.private_access'in o['connects'],'BRANCH146_PRIVATE_OPENING_ROLE')
  wd={d['unit']:d for d in world['private_domains']}
  for d in local['private_domains']:
   gross=[loc(r,d['unit'])for r in (['5.75','.15','6.75','9.3'],['6.75','5.75','10.65','6.75'])]
   expected_parts=cells(gross,list(local['walls'].values()))
   need(same_union(expected_parts,d['parts']),'BRANCH146_EXACT_PRIVATE_FLOOR')
   need(d['topology_scope']=='PARALLEL_TWINS_BRANCH146_NOT_ADMITTED'and d['route_failures']==[],'BRANCH146_DOMAIN_SCOPE_AND_ROUTES')
  for d in local['private_domains']:
   z=wd[d['unit']];need(FIELDS<=set(d)<=FIELDS|OPTIONAL and set(z)==set(d),'BRANCH146_DOMAIN_SCHEMA')
   need(set(d['public_interface'])=={'rect','open_side'}and set(z['public_interface'])=={'rect','open_side'},'BRANCH146_INTERFACE_SCHEMA')
   for k in set(d)-{'parts','paths','public_interface'}:need(equal(d[k],z[k]),'BRANCH146_DOMAIN_METADATA:'+k)
   need(equal([rigid(r,T)for r in d['parts']],z['parts']),'BRANCH146_DOMAIN_FRAME')
   expected=loc(['5.75','8.95','6.75','9.65'],d['unit']);need(equal(d['public_interface']['rect'],expected),'BRANCH146_INTERFACE_SOURCE')
   need(d['public_interface']['open_side']==('top'if d['unit']=='A'else'bottom'),'BRANCH146_INTERFACE_LOCAL_SIDE')
   need(equal(rigid(expected,T),z['public_interface']['rect'])and z['public_interface']['open_side']==interface_side(T,d['unit']),'BRANCH146_INTERFACE_FRAME')
   need(set(d['paths'])==set(z['paths'])==set(d['bedrooms']),'BRANCH146_PATH_INVENTORY')
   for k,path in d['paths'].items():need(equal([point(v,T)for v in path],z['paths'][k]),'BRANCH146_PATH_FRAME')
 except(KeyError,ValueError,TypeError,IndexError,StopIteration,ZeroDivisionError)as e:errors.append('BRANCH146_BINDING_SCHEMA:'+str(e))
 ok=not errors and not pending
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_SOURCE_BOUND_ACTUAL_PRIVATE_BRANCH146_ONLY','errors':sorted(set(errors)),'pending':sorted(set(pending)),'boundary_wall_ids':sorted(verified)if ok else[],'verified_wall_rects':verified if ok else{},'witness':witness,'source_sha256':{'twin':PIN_TWIN,'double':PIN_DOUBLE},'accepted':False,'scope':'Restricted reviewed BRANCH146 source/module wall inventory, residual core union, actual D4, fresh topology and private role. Not whole-plan, operational, visibility or quality approval.'}
