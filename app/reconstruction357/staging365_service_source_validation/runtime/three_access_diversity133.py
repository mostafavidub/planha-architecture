"""Scoped three-source entry direction relation; not architectural quality."""
from fractions import Fraction as F
import twin_access_diversity132 as prior
from twin_access_diversity132 import require,point,normal
from diversity124 import describe_model,transform,digest,q
SCOPE='THREE_ROOM_ENTRY_DIRECTION133_V1'
def access_signature(model):
 m=model
 describe_model(m) # actual source room, fixture, wall, opening and D4 binding
 evidence=[]
 for rec in m['module_placements']:
  s=rec['module']
  if s['schema']not in('PRIVATE_TWIN_ROOM_MODULE118','PRIVATE_ROOM_MODULE116'):continue
  uid=rec['unit_id'];u=next(u for u in m['units']if u['id']==uid);rs=s['unit']['rooms']['bed1'];require(len(rs)==1,'SINGLE_RECT_TWIN_ROOM_REQUIRED')
  require(len(s['external_ports'])==1,'ONE_SOURCE_TWIN_PORT_REQUIRED');src=s['external_ports'][0];op=next(o for o in s['openings']if o['id']==src['opening_id']);ids=rec['id_map'];T=rec['transform'];tr=transform(rec)
  out=next(o for o in m['openings']if o['id']==ids[op['id']]);ports=[p for p in m['module_ports']if p['id']==ids[src['id']]];require(len(ports)==1,'ONE_ACTUAL_TWIN_PORT_REQUIRED');port=ports[0]
  require(q(port['rect'])==tr(src['rect'])and tuple(map(F,port['center']))==point(src['center'],T),'ACTUAL_PORT_BINDING')
  require(port['opening_id']==out['id'],'ACTUAL_PORT_OPENING_ID')
  n=normal(rs[0],op['rect'],src['center']);expected=tuple(sum(F(T['matrix'][i][j])*n[j]for j in(0,1))for i in(0,1));actual=normal(u['rooms'][rec['room_id']][0],out['rect'],port['center']);require(expected==actual,'SOURCE_NORMAL_D4_BINDING')
  evidence.append({'role':'twin'if s['schema']=='PRIVATE_TWIN_ROOM_MODULE118'else'double','unit':uid,'room':rec['room_id'],'module_hash':rec['module_hash'],'room_rect':u['rooms'][rec['room_id']][0],'opening':out['rect'],'port':port['center'],'normal':list(actual)})
 require({e['unit']for e in evidence}=={u['id']for u in m['units']} and bool(m['units']),'ALL_UNITS_REQUIRE_TWO_TWINS')
 signatures=[]
 for uid in sorted({e['unit']for e in evidence}):
  es=[e for e in evidence if e['unit']==uid];ts=[e for e in es if e['role']=='twin'];ds=[e for e in es if e['role']=='double'];require(len(es)==3 and len(ts)==2 and len(ds)==1,'EXACT_TWO_TWINS_ONE_DOUBLE_REQUIRED')
  dot=lambda a,b:sum(x*y for x,y in zip(a['normal'],b['normal']))
  signatures.append([dot(ts[0],ts[1]),*sorted(dot(ds[0],t)for t in ts)])
 return {'signature':sorted(signatures),'witness':evidence}

def describe(candidate):
 b=prior.describe(candidate);r={**b,'schema':SCOPE,'prior_descriptor':b,'applicable':False,'accepted':False,'scope':'Three source bedroom entry direction relations only, not architectural quality or whole admission.'}
 try:
  a=access_signature(candidate['model']);r.update(applicable=True,signature=a['signature'],witness=a['witness'])
 except (ValueError,KeyError,TypeError,IndexError,StopIteration)as e:r['not_applicable_reason']=str(e)
 return r

def compare(a,b):
 out={'distinct':False,'scope':SCOPE,'architectural_quality_verified':False,'accepted':False}
 if a.get('schema')!=SCOPE or b.get('schema')!=SCOPE:return dict(out,status='UNSUPPORTED_DESCRIPTOR')
 if a.get('program_key')!=b.get('program_key'):return dict(out,status='INCOMPARABLE_PROGRAM')
 old=prior.compare(a.get('prior_descriptor',{}),b.get('prior_descriptor',{}))
 if old.get('distinct'):return old
 out['base_comparison']=old
 if not a.get('applicable')or not b.get('applicable'):return dict(out,status='NOT_APPLICABLE_THREE_SOURCE_BEDROOMS_REQUIRED')
 sa,sb=a.get('signature'),b.get('signature')
 def valid(v):return isinstance(v,list)and bool(v)and all(isinstance(x,list)and len(x)==3 and all(type(t)is int and t in(-1,0,1)for t in x)for x in v)
 if not valid(sa)or not valid(sb)or len(sa)!=len(sb):return dict(out,status='INVALID_DIRECTION_SIGNATURE')
 if sorted(sa)==sorted(sb):return dict(out,status='SAME_THREE_ROOM_ENTRY_DIRECTION_ORGANIZATION')
 return dict(out,distinct=True,status='DISTINCT_THREE_ROOM_ENTRY_DIRECTION_ORGANIZATION_SCOPED',dimensions=['source_bound_twin_and_double_entry_direction_dots'],signatures=[sa,sb],meaning='Limited source entry-direction relationships, not overall architecture or quality.')
