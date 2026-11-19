"""Source-built component descriptor study, not a whole-model adapter.
Opaque reference labels belong to THIS projection contract. Frozen producer
room_id remains semantic: alpha-renamed whole models are not declared valid.
No admission gate, solver, private artifact, similarity threshold or quality score.
"""
import copy,hashlib,inspect,itertools,json,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
PINS={"kitchen_module117.py":"8ec837d51e724076d8b479763b132756137de61b","bedroom_module116.py":"289b23f25bafaa05281015b521affad5ab5a415d","geometry114.py":"09751a69ad7be1626a5462716837c2371a45815d","contract114.py":"a2631c6a38a43b8d423edf82ad8d526ced1b8196","fixture_catalog114.json":"df6ef667f54d7e577e7027d33fe320ec0d16ad07","diversity124.py":"4dd9de4f84bcd54c343afd17b55a15b0944c50e0","diversity_multidim126.py":"00268000d0a277dc3b9fd1e312419370d308e069"}
SCHEMA='SOURCE_COMPONENT_SEMANTIC_DESCRIPTOR301_V1'
ROLES={'KITCHEN_MODULE117':('kitchen','kitchen_module117','kitchen','K.kitchen','K.public_access'),
       'PRIVATE_ROOM_MODULE116':('bedroom:double','bedroom_module116','bed1','M.bed1','M.public_access')}
D4=[[[a,0],[0,b]]for a in(-1,1)for b in(-1,1)]+[[[0,a],[b,0]]for a in(-1,1)for b in(-1,1)]
def require(ok,why):
 if not ok:raise ValueError(why)
def strict(v):
 if type(v) in(str,int,bool,type(None)):return
 if type(v)is list:
  for x in v:strict(x)
 elif type(v)is dict:
  require(all(type(k)is str for k in v),'JSON_KEY')
  for x in v.values():strict(x)
 else:raise ValueError('EXACT_JSON_TYPES')
def digest(v):
 strict(v)
 return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def guard():
 for n,pin in PINS.items():
  b=(ENGINE/n).read_bytes()
  require(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==pin,'SOURCE_PIN')
 return dict(PINS)
def module(schema,width,depth):
 guard();require(schema in ROLES,'SOURCE_SCHEMA')
 name=ROLES[schema][1]
 if str(ENGINE)not in sys.path:sys.path.insert(0,str(ENGINE))
 mod=__import__(name)
 require(Path(mod.__file__).resolve()==(ENGINE/(name+'.py')).resolve(),'SOURCE_IMPORT')
 require(Path(inspect.getsourcefile(mod.build)).resolve()==(ENGINE/(name+'.py')).resolve(),'SOURCE_CALLABLE')
 for dependency in ('contract114','geometry114'):
  dep=__import__(dependency)
  require(Path(dep.__file__).resolve()==(ENGINE/(dependency+'.py')).resolve(),'DEPENDENCY_IMPORT')
 out=mod.build(width,depth);guard();return out
def rect(r):
 require(type(r)is list and len(r)==4 and all(type(x)is str for x in r),'RECT_STRINGS')
 q=list(map(F,r));require(q[0]<q[2]and q[1]<q[3],'POSITIVE_RECT')
 return q
def transform(r,t):
 require(type(t)is dict and set(t)=={'matrix','translation'},'TRANSFORM_FIELDS')
 M=t['matrix'];off=t['translation']
 require(type(M)is list and M in D4 and all(type(x)is int for row in M for x in row),'D4_MATRIX')
 require(type(off)is list and len(off)==2 and all(type(x)is str for x in off),'TRANSLATION')
 x,y,X,Y=rect(r);a,b=map(F,off)
 pts=[(M[0][0]*u+M[0][1]*v+a,M[1][0]*u+M[1][1]*v+b)for u in(x,X)for v in(y,Y)]
 return list(map(str,[min(p[0]for p in pts),min(p[1]for p in pts),max(p[0]for p in pts),max(p[1]for p in pts)]))
def placed(source,uid,ref,t):
 role,_,local,inside,outside=ROLES[source['schema']]
 rooms=source['unit']['rooms'][local]
 links={inside:ref,outside:uid+'.public'}
 return {'unit':uid,'reference':ref,'display_name':role,'color':'gray','source':copy.deepcopy(source),
  'source_digest':digest(source),'transform':copy.deepcopy(t),'room_parts':[transform(r,t)for r in rooms],
  'fixtures':{k:transform(r,t)for k,r in source['unit']['fixtures'].items()},
  'links':links,'openings':[{'source_id':o['id'],'rect':transform(o['rect'],t),'connects':[links[x]for x in o['connects']]}for o in source['openings']]}
def validate(s):
 strict(s);pin=guard()
 require(set(s)=={'schema','input','programme','frame','core','records'},'ROOT_FIELDS')
 require(s['schema']==SCHEMA and s['programme']=='SOURCE_COMPONENT_FIXTURE_NOT_WHOLE_PROGRAM','SCOPE')
 require(s['input']=={'W':'18','L':'20','n':2}and type(s['input']['n'])is int,'INPUT_SCOPE')
 require(s['frame']=='WORLD_XY_METRES','FRAME')
 require(set(s['core'])=={'stair','lift'},'CORE_ANCHORS')
 for r in s['core'].values():rect(r)
 require(type(s['records'])is list and len(s['records'])==4,'COMPONENT_INVENTORY')
 seen=set();inventory={}
 for r in s['records']:
  require(set(r)=={'unit','reference','display_name','color','source','source_digest','transform','room_parts','fixtures','links','openings'},'RECORD_FIELDS')
  uid,ref=r['unit'],r['reference'];require(uid in('A','B')and type(ref)is str and bool(ref)and ref!=uid+'.public','REFERENCE')
  require((uid,ref)not in seen,'DUPLICATE_REFERENCE');seen.add((uid,ref))
  require(type(r['display_name'])is str and type(r['color'])is str,'PRESENTATION_TYPES')
  source=r['source'];require(source['schema']in ROLES,'SOURCE_SCHEMA')
  role,_,local,inside,outside=ROLES[source['schema']]
  p=source['input_program'];rebuilt=module(source['schema'],p['width'],p['depth'])
  require(digest(source)==r['source_digest']==digest(rebuilt),'SOURCE_REBUILD_BINDING')
  inventory.setdefault(uid,[]).append(role)
  expected=placed(rebuilt,uid,ref,r['transform'])
  for k in('room_parts','fixtures','links','openings'):
   require(digest(r[k])==digest(expected[k]),'SOURCE_REFERENCE_OR_GEOMETRY:'+k)
 require(set(inventory)=={'A','B'}and all(sorted(v)==['bedroom:double','kitchen']for v in inventory.values()),'PROGRAMME_INVENTORY')
 require(guard()==pin,'SOURCE_CHANGED')
 return pin
def box(rs):
 qs=[rect(r)for r in rs]
 return list(map(str,[min(q[0]for q in qs),min(q[1]for q in qs),max(q[2]for q in qs),max(q[3]for q in qs)]))
def relation(a,b):
 a,b=rect(a),rect(b);out=[]
 for axis in(0,1):
  out.append('BEFORE'if a[axis+2]<b[axis]else'AFTER'if b[axis+2]<a[axis]else'OVERLAP'if max(a[axis],b[axis])<min(a[axis+2],b[axis+2])else'CONTACT')
 return out
def describe(s):
 pins=validate(s);variants=[];access=[]
 for uid in('A','B'):
  edges=[]
  for r in s['records']:
   if r['unit']!=uid:continue
   role,_,_,inside,outside=ROLES[r['source']['schema']]
   labels={r['links'][inside]:role,r['links'][outside]:'open_public'}
   edges.extend(sorted(labels[x]for x in o['connects'])for o in r['openings'])
  access.append(sorted(edges))
 for M in D4:
  units=[]
  for uid in('A','B'):
   regions={ROLES[r['source']['schema']][0]:box(r['room_parts'])for r in s['records']if r['unit']==uid}
   regions.update({'common_'+k:v for k,v in s['core'].items()})
   regions={k:transform(v,{'matrix':M,'translation':['0','0']})for k,v in regions.items()}
   units.append([[a,b,relation(regions[a],regions[b])]for a,b in itertools.combinations(sorted(regions),2)])
  variants.append(sorted(units,key=lambda x:json.dumps(x,sort_keys=True)))
 canonical=min(variants,key=lambda x:json.dumps(x,sort_keys=True))
 return {'schema':SCHEMA,'input':copy.deepcopy(s['input']),'programme':s['programme'],'frame':s['frame'],
  'source_pins':pins,'source_fixture_digest':digest(s),'access':sorted(access,key=lambda x:json.dumps(x)),
  'relations':canonical,'signature':digest({'access':sorted(access,key=lambda x:json.dumps(x)),'relations':canonical}),
  'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
  'whole_model_validated':False,'origin_authenticated':False,
  'equivalence_basis':{'reference':'Opaque label in projection only; all source opening links validated before removal','semantic_role':'Pinned source schema; producer room_id not renamed','geometry_scope':'Source component rectangles plus synthetic core anchors; no inter-component route proof'},
  'scope':'Exact source-component projection only; box order is not useful area/accessibility. Core rectangles are synthetic anchors, not a validated stair/lift/lobby. No threshold, quality, producer rename validity or current admission.'}
def compare(a,b):
 strict(a);strict(b)
 if any(digest(a[k])!=digest(b[k])for k in('input','programme','frame')):
  return {'state':'NOT_COMPARABLE','descriptor_comparison_performed':False,'input_validation_performed':False,'qualified':False,'delivery_allowed':False}
 x,y=describe(a),describe(b)
 same=x['signature']==y['signature']
 return {'state':'EXACT_DESCRIPTOR_EQUIVALENT'if same else'COMPONENT_ORGANIZATION_DESCRIPTOR_DIFFERENCE',
  'same_descriptor':same,'architectural_diversity_verified':False,'qualified':False,'delivery_allowed':False}
def fixture():
 k=module('KITCHEN_MODULE117','2.35','3.05');b=module('PRIVATE_ROOM_MODULE116','5.45','3.6')
 records=[]
 for uid,dy in(('A',0),('B',10)):
  for ref,source,x,y in(('cooking',k,2,2),('sleeping',b,8,2)):
   records.append(placed(source,uid,uid+'.'+ref,{'matrix':[[1,0],[0,1]],'translation':[str(x),str(y+dy)]}))
 return {'schema':SCHEMA,'input':{'W':'18','L':'20','n':2},'programme':'SOURCE_COMPONENT_FIXTURE_NOT_WHOLE_PROGRAM','frame':'WORLD_XY_METRES',
  'core':{'stair':['1','7','3','9'],'lift':['4','7','6','9']},'records':records}
