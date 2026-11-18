"""Source-bound twin entry-direction diversity only; never admission/quality.
No raw room relations or distance threshold. Existing diversity remains separate.
"""
from fractions import Fraction as F
import diversity_multidim126 as base_diversity
from diversity124 import describe_model,describe_candidate,transform,digest,q
SCOPE='TWIN_ENTRY_DIRECTION_ORGANIZATION132_V1'
def require(ok,reason):
 if not ok:raise ValueError(reason)
def point(v,T):return tuple(sum(F(T['matrix'][i][j])*F(v[j])for j in(0,1))+F(T['translation'][i])for i in(0,1))
def normal(room,opening,port):
 r=q(room);o=q(opening);p=tuple(map(F,port));options=[]
 # Aperture lies outside a clear room and ends exactly on its boundary;
 # positive tangent overlap and external actual body port prove which side.
 for axis in (0,1):
  j=1-axis
  if min(r[j+2],o[j+2])<=max(r[j],o[j]):continue
  if o[axis+2]==r[axis] and p[axis]<r[axis]:options.append(tuple(-1 if i==axis else 0 for i in(0,1)))
  if o[axis]==r[axis+2] and p[axis]>r[axis+2]:options.append(tuple(1 if i==axis else 0 for i in(0,1)))
 if len(options)!=1:raise ValueError('NO_UNIQUE_ACTUAL_OUTWARD_PORT_NORMAL')
 return options[0]
def access_signature(model):
 m=model
 describe_model(m) # actual source room, fixture, wall, opening and D4 binding
 evidence=[]
 for rec in m['module_placements']:
  s=rec['module']
  if s['schema']!='PRIVATE_TWIN_ROOM_MODULE118':continue
  uid=rec['unit_id'];u=next(u for u in m['units']if u['id']==uid);rs=s['unit']['rooms']['bed1'];require(len(rs)==1,'SINGLE_RECT_TWIN_ROOM_REQUIRED')
  require(len(s['external_ports'])==1,'ONE_SOURCE_TWIN_PORT_REQUIRED');src=s['external_ports'][0];op=next(o for o in s['openings']if o['id']==src['opening_id']);ids=rec['id_map'];T=rec['transform'];tr=transform(rec)
  out=next(o for o in m['openings']if o['id']==ids[op['id']]);ports=[p for p in m['module_ports']if p['id']==ids[src['id']]];require(len(ports)==1,'ONE_ACTUAL_TWIN_PORT_REQUIRED');port=ports[0]
  require(q(port['rect'])==tr(src['rect'])and tuple(map(F,port['center']))==point(src['center'],T),'ACTUAL_PORT_BINDING')
  require(port['opening_id']==out['id'],'ACTUAL_PORT_OPENING_ID')
  n=normal(rs[0],op['rect'],src['center']);expected=tuple(sum(F(T['matrix'][i][j])*n[j]for j in(0,1))for i in(0,1));actual=normal(u['rooms'][rec['room_id']][0],out['rect'],port['center']);require(expected==actual,'SOURCE_NORMAL_D4_BINDING')
  evidence.append({'unit':uid,'room':rec['room_id'],'module_hash':rec['module_hash'],'room_rect':u['rooms'][rec['room_id']][0],'opening':out['rect'],'port':port['center'],'normal':list(actual)})
 require({e['unit']for e in evidence}=={u['id']for u in m['units']} and bool(m['units']),'ALL_UNITS_REQUIRE_TWO_TWINS')
 dots=[]
 for uid in sorted({e['unit']for e in evidence}):
  es=[e for e in evidence if e['unit']==uid];require(len(es)==2,'EXACTLY_TWO_TWINS_PER_UNIT_REQUIRED')
  dots.append(sum(a*b for a,b in zip(es[0]['normal'],es[1]['normal'])))
 return {'signature':sorted(dots),'witness':evidence}

def describe(candidate):
 # Requires actual preserved whole-gate/model hash before this new dimension.
 base=base_diversity.describe(candidate)
 result={**base,'schema':SCOPE,'program_key':base['program_key'],'model_hash':digest(candidate['model']),'gate_hash':digest(candidate['gate']),'applicable':False,'accepted':False,'whole_gate_reexecuted':False,'scope':'Difference of actual twin entry directions only; not whole architectural diversity, quality or admission.'}
 try:
  witness=access_signature(candidate['model'])
  result.update(applicable=True,signature=witness['signature'],witness=witness['witness'])
 except (ValueError,KeyError,TypeError,IndexError,StopIteration)as ex:
  result['not_applicable_reason']=str(ex)
 return result

def compare(a,b):
 out={'distinct':False,'scope':SCOPE,'architectural_quality_verified':False,'accepted':False}
 if a.get('schema')!=SCOPE or b.get('schema')!=SCOPE:return dict(out,status='UNSUPPORTED_DESCRIPTOR')
 if a.get('program_key')!=b.get('program_key'):return dict(out,status='INCOMPARABLE_PROGRAM')
 prior=base_diversity.compare(a,b)
 if prior.get('distinct'):return prior
 out['base_comparison']=prior
 if not a.get('applicable')or not b.get('applicable'):return dict(out,status='NOT_APPLICABLE_TWO_SOURCE_TWINS_REQUIRED')
 sa,sb=a.get('signature'),b.get('signature')
 if not isinstance(sa,list)or not isinstance(sb,list)or not sa or len(sa)!=len(sb)or any(type(x)is not int or x not in(-1,0,1)for x in sa+sb):return dict(out,status='INVALID_DIRECTION_SIGNATURE')
 if sorted(sa)==sorted(sb):return dict(out,status='SAME_TWIN_ENTRY_DIRECTION_ORGANIZATION')
 return dict(out,distinct=True,status='DISTINCT_TWIN_ENTRY_DIRECTION_ORGANIZATION_SCOPED',dimensions=['source_bound_twin_entry_direction_dot'],signatures=[sorted(sa),sorted(sb)],meaning='Different organization of twin access directions, not proof doors face one another, overall quality or six plans.')
