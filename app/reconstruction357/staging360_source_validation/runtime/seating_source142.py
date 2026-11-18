"""Fixed source D4 compact group. No ergonomic/full-gate approval."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from contract114 import S,BODY
ROOT=Path(__file__).parent
MARKER='SIDECAR_COMPACT_D4_GROUP142_LOCAL_WORLD_PENDING'
IDS=('sofa1','sofa2','armchair1','armchair2','armchair3','armchair4')
PLACEMENTS={'sofa1':(270,'0','0'),'sofa2':(0,'1.6','0'),'armchair1':(90,'0','2.3'),'armchair2':(90,'0','3.1'),'armchair3':(270,'2.7','1.6'),'armchair4':(270,'2.7','2.4')}
MATRICES=(((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)))
CAT=json.loads((ROOT/'fixture_catalog114.json').read_text());RAW=(ROOT/CAT['source_file']).read_bytes()
if hashlib.sha256(RAW).hexdigest()!='2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4':raise ValueError('REFERENCE_CHANGED')
SRC=json.loads(RAW)['units'][0]
def transform(q,m,t=(0,0)):
 a,b,c,d=map(F,q);ps=[tuple(sum(m[i][j]*p[j]for j in range(2))+t[i]for i in range(2))for p in((a,b),(a,d),(c,b),(c,d))]
 return(min(p[0]for p in ps),min(p[1]for p in ps),max(p[0]for p in ps),max(p[1]for p in ps))
def instance(name,placement):
 angle,x,y=placement;x,y=F(x),F(y)
 if angle not in(0,90,180,270):raise ValueError('ROTATION_NOT_D4')
 key=name if name.startswith('sofa')else('armchair1'if name in('armchair1','armchair3')else'armchair2')
 fx=tuple(F(str(v))for v in SRC['fixtures'][key]);ac=tuple(F(str(v))for v in SRC['activities'][key+'_front'])
 # Retain the current wider chair activity reservation. Source geometry stays separate.
 reserved=ac if name.startswith('sofa')else(fx[0],ac[1],fx[2],ac[3])
 union=(min(fx[0],reserved[0]),min(fx[1],reserved[1]),max(fx[2],reserved[2]),max(fx[3],reserved[3]));m=MATRICES[angle//90];q=transform(union,m);t=(x-q[0],y-q[1])
 out={'id':name,'source_key':key,'source_sha256':CAT['source_file_sha256'],'matrix':m,'translation':t,'rotation':angle,'fixture':transform(fx,m,t),'source_activity':transform(ac,m,t),'reserved_activity':transform(reserved,m,t),'use':transform(union,m,t)}
 a,b,c,d=out['source_activity'];out['target']=((a+c)/2,(b+d)/2)
 return out

def records(origin):
 x,y=map(F,origin)
 return {k:instance(k,(angle,S(x+F(a)),S(y+F(b))))for k,(angle,a,b)in PLACEMENTS.items()}
def serialized_records(origin):
 return json.loads(json.dumps(records(origin),default=S))
def validate_proposal(p):
 if p.get('generation_method')!=MARKER:raise ValueError('COMPACT142_MARKER')
 if any(k in p for k in('rooted_service_study','opposing_group_study')):raise ValueError('COMPACT142_UNRELATED_GROUP_OR_ROOT_CLAIM')
 rs=p['rectangles'];x,y=map(F,rs['sofa1_use'][:2]);expected=records((x,y))
 for k,v in expected.items():
  key=k+'_use'if k.startswith('sofa')else'chair'+k[-1]+'_use'
  if tuple(map(F,rs[key]))!=v['use']:raise ValueError('COMPACT142_EXACT_USE:'+k)
 if p['compact_d4_sources142']!=serialized_records((x,y)):raise ValueError('COMPACT142_SOURCE_RECORD')
 if tuple(map(F,p['shared_body_witness']))!=(x+F('1.6'),y+F('1.6'),x+F('2.3'),y+F('2.3')):raise ValueError('COMPACT142_WITNESS')
 return expected
