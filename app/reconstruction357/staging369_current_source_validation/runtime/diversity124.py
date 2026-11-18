"""Conservative functional-access diversity, not quality/admission certification.
No light/window/facade inputs. No solver or producer imports. Caller must first
freshly validate each candidate; this evaluator checks receipt/model binding and
independently derives a limited physical/source-bound relation description.
Contact-only changes, changed coordinates and altered programs are not counted
as six functional organizations. No actual positive pair has yet been validated
for this evaluator, so architectural diversity remains explicitly unverified.
"""
import json,hashlib,itertools
from copy import deepcopy
from fractions import Fraction as F

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def q(r):
 r=tuple(F(str(x))for x in r)
 if len(r)!=4 or r[0]>=r[2]or r[1]>=r[3]:raise ValueError('NONPOSITIVE_RECTANGLE')
 return r

def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def area(rs):
 rs=[q(r)for r in rs];ys=sorted({v for r in rs for v in(r[1],r[3])});s=F(0)
 for y,Y in zip(ys,ys[1:]):
  spans=sorted((r[0],r[2])for r in rs if r[1]<Y and r[3]>y);end=None;length=F(0)
  for x,X in spans:
   if end is None or x>end:length+=X-x;end=X
   elif X>end:length+=X-end;end=X
  s+=(Y-y)*length
 return s

def equal_union(a,b):
 # Exact area of symmetric difference; cell subdivision/order is irrelevant.
 inter=[(max(x[0],y[0]),max(x[1],y[1]),min(x[2],y[2]),min(x[3],y[3]))for x in map(q,a)for y in map(q,b)if max(x[0],y[0])<min(x[2],y[2])and max(x[1],y[1])<min(x[3],y[3])]
 return area(a)+area(b)==2*area(inter)

def transform(rec):
 mat=[[F(str(x))for x in row]for row in rec['transform']['matrix']];off=[F(str(x))for x in rec['transform']['translation']]
 if len(mat)!=2 or any(len(r)!=2 for r in mat)or any(x not in (F(-1),F(0),F(1))for r in mat for x in r)or any(sum(x!=0 for x in r)!=1 for r in mat)or any(sum(mat[i][j]!=0 for i in range(2))!=1 for j in range(2))or abs(mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0])!=1:raise ValueError('NONRIGID_SOURCE_TRANSFORM')
 def rect(r):
  x,y,X,Y=q(r);ps=[(mat[0][0]*a+mat[0][1]*b+off[0],mat[1][0]*a+mat[1][1]*b+off[1])for a in(x,X)for b in(y,Y)]
  return(min(a for a,b in ps),min(b for a,b in ps),max(a for a,b in ps),max(b for a,b in ps))
 return rect

def touch(a,b):
 a,b=q(a),q(b)
 return ((a[2]==b[0]or b[2]==a[0])and max(a[1],b[1])<min(a[3],b[3]))or((a[3]==b[1]or b[3]==a[1])and max(a[0],b[0])<min(a[2],b[2]))

def describe_model(m):
 """Lower-level geometry descriptor, NOT validation or proof of an admitted plan."""
 from core_wall_audit118 import opening_hosts
 doorview=deepcopy(m);doorview['concept_windows']=[]
 physical=opening_hosts(doorview)
 if physical.get('status')!='PASS_LIMITED':raise ValueError('ACTUAL_DOOR_HOST_CHECK_NOT_PASSED')
 units={u['id']:u for u in m['units']};roomlabels={};unitprogram={u:[]for u in units};bound_openings={};source_witness=[]
 schema_roles={'PRIVATE_ROOM_MODULE116':('bed1','bedroom:double'),'PRIVATE_TWIN_ROOM_MODULE118':('bed1','bedroom:twin'),'KITCHEN_MODULE117':('kitchen','kitchen'),'BATHROOM_MODULE117':('bath','bath')}
 for rec in m['module_placements']:
  uid,rid=rec['unit_id'],rec['room_id'];u=units[uid];s=rec['module'];schema=s['schema']
  if schema not in schema_roles:raise ValueError('UNSUPPORTED_SOURCE_SCHEMA:'+schema)
  if digest(s)!=rec['module_hash']:raise ValueError('SOURCE_HASH_BINDING')
  localrole,label=schema_roles[schema];tr=transform(rec);ids=rec['id_map'];key=uid+'.'+rid
  if key in roomlabels:raise ValueError('DUPLICATE_SOURCE_ROOM')
  if not equal_union(u['rooms'][rid],[tr(r)for r in s['unit']['rooms'][localrole]]):raise ValueError('ACTUAL_SOURCE_ROOM_BINDING')
  for k,r in s['unit']['fixtures'].items():
   if q(u['fixtures'][ids[k]])!=tr(r):raise ValueError('ACTUAL_SOURCE_FIXTURE_BINDING')
  for field in ('walls','wall_hosts'):
   for k,r in s[field].items():
    if q(m[field][ids[k]])!=tr(r):raise ValueError('ACTUAL_SOURCE_WALL_BINDING')
  roomlabels[key]=label;unitprogram[uid].append(label)
  for o in s['openings']:
   oid=ids[o['id']];matches=[z for z in m['openings']if z['id']==oid]
   if len(matches)!=1:raise ValueError('ACTUAL_SOURCE_OPENING_INVENTORY')
   a=matches[0]
   if q(a['rect'])!=tr(o['rect'])or a['host_wall_id']!=ids[o['host_wall_id']]or a['connects']!=[ids.get(x,x)for x in o['connects']]:raise ValueError('ACTUAL_SOURCE_OPENING_BINDING')
   bound_openings[oid]=key
  source_witness.append({'unit':uid,'room':rid,'functional_label':label,'module_hash':rec['module_hash']})
 # Actual dining source/placement isometry, rather than caller program label.
 for uid,u in units.items():
  rec=u['dining_module_placement'];s=rec['module'];tr=transform(rec)
  if digest(s)!=rec['module_hash']:raise ValueError('DINING_SOURCE_HASH')
  for k,r in s['fixtures'].items():
   if q(u['fixtures'][rec['id_map'][k]])!=tr(r):raise ValueError('DINING_FIXTURE_BINDING')
  unitprogram[uid].append('dining_seats:'+str(len(s['seating']['instances'])))
  seats={}
  for k,md in u['fixture_metadata'].items():
   kind=md.get('kind','')
   if kind.startswith(('sofa','armchair')):
    r=q(u['fixtures'][k]);dims=sorted([str(r[2]-r[0]),str(r[3]-r[1])]);tag=canonical([kind,dims]);seats[tag]=seats.get(tag,0)+1
  unitprogram[uid].append('seating_inventory:'+canonical(seats))
 private_nodes={}
 if m.get('private_domains'):
  from private_domain121 import examine
  d=examine(m)
  if d['errors']or d['pending']:raise ValueError('PRIVATE_DOMAIN_UNBOUND')
  for v in m['private_domains']:
   uid=v['unit'];private_nodes[uid+'.private_access']='private_approach'
 def role(uid,name):
  if name in roomlabels:return roomlabels[name]
  if name in private_nodes:return private_nodes[name]
  if name=='lobby':return 'common_lobby'
  if not name.startswith(uid+'.'):raise ValueError('CROSS_UNIT_OR_UNKNOWN_ROLE')
  suffix=name[len(uid)+1:]
  if suffix in ('public_access','kitchen_public_access','bedroom_public_access'):
   logical=m['logical_regions'].get(name,{})
   permitted=['living','entry_circulation']if suffix=='public_access'else['living','entry_circulation','dining']
   if logical.get('unit')!=uid or logical.get('source_roles')!=permitted or 'parts'in logical:raise ValueError('PUBLIC_ROLE_BINDING')
   return 'open_public' # typed aliases do not create new organization.
  if suffix in ('vanity','WC','shower'):return 'bath:'+suffix
  raise ValueError('UNRESOLVED_ROLE:'+suffix)
 desc=[];witness=[]
 for uid,u in units.items():
  edges=[];entries=[]
  for o in m['openings']:
   con=o['connects']
   if not any(x.startswith(uid+'.')for x in con):continue
   if len(con)!=2:raise ValueError('PORTAL_ROLE_ARITY')
   if o['id']not in bound_openings:
    if set(con)!={'lobby',uid+'.public_access'}:raise ValueError('UNBOUND_NONMODULE_PORTAL')
    entries.append(o['id'])
   r=q(o['rect']) # physical aperture/pocket host checked freshly above; not all pocket apertures lie within the named pocket-host rectangle.
   edge=sorted(role(uid,k)for k in con);edges.append(edge)
   witness.append({'opening':o['id'],'unit':uid,'roles':edge,'host':o['host_wall_id'],'rect':list(map(str,r))})
  if len(entries)!=1:raise ValueError('ENTRY_INVENTORY_UNSUPPORTED')
  # Physical positive-length floor contacts; not used alone to count diversity.
  regions={}
  for k,rs in u['rooms'].items():
   label=roomlabels.get(uid+'.'+k,'open_public'if k in('living','entry_circulation','dining')else'private_approach'if k=='private_circulation'and uid+'.private_access'in private_nodes else None)
   if label is None:raise ValueError('UNRESOLVED_FLOOR_ROLE:'+k)
   regions.setdefault(label,[]).extend(rs)
  contacts=[]
  for a,b in itertools.combinations(sorted(regions),2):
   if any(touch(x,y)for x in regions[a]for y in regions[b]):contacts.append([a,b])
  desc.append({'program':sorted(unitprogram[uid]),'access_edges':sorted(edges),'physical_floor_contacts':contacts})
 # Coarse role multisets conservatively collapse permutations and all rigid
 # transforms. They may undercount organizations, never claim completeness.
 pkey=canonical({'frame':[str(F(str(v)))for v in m['inputs']],'units':sorted(canonical(v['program'])for v in desc),'core_program':sorted(k for k in m['common_spaces']if k in ('stair','lift','lobby'))})
 sig=canonical(sorted(canonical({'program':d['program'],'access_edges':d['access_edges']})for d in desc))
 return {'program_key':pkey,'access_signature':sig,'units':desc,'witness':{'source_rooms':source_witness,'actual_portals':witness},'scope':'Coarse source-bound functional access graph; repeated compatible bedrooms are unlabelled. Contact changes alone are unresolved. Spatial ordering/core arrangement beyond access graph is not proved.'}

def describe_candidate(c):
 m,g=c['model'],c['gate']
 if g.get('model_hash')!=digest(m):raise ValueError('GATE_MODEL_BINDING')
 if g.get('status')!='PASS_CONCEPT_SCOPED_REVIEW'or g.get('gate_scope')!='CONCEPT117_SOURCE_COMPAT_V1'or g.get('errors')or g.get('pending')or not g.get('eligible_for_draft_export'):raise ValueError('WHOLE_GATE_NOT_ELIGIBLE')
 return describe_model(m)

def compare(a,b):
 if a['program_key']!=b['program_key']:return {'status':'INCOMPARABLE_PROGRAM','distinct':False}
 if a['access_signature']==b['access_signature']:return {'status':'UNRESOLVED_SAME_COARSE_ACCESS_ORGANIZATION','distinct':False,'reason':'No demonstrated functional-access difference; coordinate/contact/route-only changes do not establish organization diversity.'}
 return {'status':'DISTINCT_ACCESS_GRAPH_SCOPED','distinct':True,'reason':'Different actual source-bound role access graph, not centroid/seed/hash/window difference. Architectural quality and full organization diversity remain unverified.'}

def audit_batch(candidates,requested_count=6):
 if not isinstance(requested_count,int)or requested_count<1:raise ValueError('INVALID_REQUESTED_COUNT')
 ds=[];errors=[]
 for i,c in enumerate(candidates):
  try:ds.append(describe_candidate(c))
  except(KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as e:ds.append(None);errors.append({'index':i,'reason':str(e)})
 groups={};pairs=[]
 for i,a in enumerate(ds):
  if a is None:continue
  groups.setdefault(a['program_key'],[]).append(i)
  for j in range(i):
   if ds[j]is not None:pairs.append({'a':j,'b':i,**compare(ds[j],a)})
 result=[]
 for key,indices in groups.items():
  chosen=[]
  for i in indices:
   if all(compare(ds[j],ds[i])['distinct']for j in chosen):chosen.append(i)
  result.append({'program_key':key,'supplied_indices':indices,'representative_indices':chosen,'distinct_count':len(chosen),'shortfall':max(0,requested_count-len(chosen))})
 # Different capacities never sum to six organizations of one program.
 count=max((g['distinct_count']for g in result),default=0)
 return {'schema':'FUNCTIONAL_DIVERSITY124_SCOPED_V1','status':'NOT_EVALUATED'if errors else'DIVERSITY_SCOPE_ONLY','requested_count':requested_count,'supplied_count':len(candidates),'distinct_count':count,'shortfall':max(0,requested_count-count),'program_groups':result,'pairs':pairs,'errors':errors,'descriptions':ds,'verified_architectural_diversity':False,'actual_positive_distinct_pair_validation':'NOT_YET_ESTABLISHED','individual_gates_reexecuted':False,'gate_binding_checked':True,'accepted':False,'limits':['Caller must freshly validate whole candidates; this checks binding, not authenticity of arbitrary external receipts.','Singleton is one representative, not proof of diversity. Different programs are not aggregated.','Graph collisions undercount; contact/coordinate-only differences remain unresolved.','No light/ventilation evaluation; no quality score or guarantee of six.']}
