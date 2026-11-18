"""Independent exact common-core/frame contract audit; no producer import.
PASS here never licenses whole-model/world admission.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
from core_partition_audit125 import audit

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def point(p,T):
 a=T['matrix'];t=list(map(F,T['translation']));p=list(map(F,p))
 return [sum(F(a[i][j])*p[j] for j in range(2))+t[i]for i in range(2)]
def rectangle(r,T):
 x,y,X,Y=map(F,r);v=[point(p,T)for p in((x,y),(x,Y),(X,y),(X,Y))]
 return [min(p[0]for p in v),min(p[1]for p in v),max(p[0]for p in v),max(p[1]for p in v)]
def equal(a,b):
 if isinstance(a,dict):return isinstance(b,dict) and set(a)==set(b) and all(equal(a[k],b[k])for k in a)
 if isinstance(a,(list,tuple)):return isinstance(b,(list,tuple))and len(a)==len(b)and all(equal(x,y)for x,y in zip(a,b))
 try:return F(str(a))==F(str(b))
 except (ValueError,TypeError):return a==b

def evaluate_core(c):
 errors=[];evidence={}
 try:
  m=c['physical_core_model'];T=c['world_from_local'];a=T['matrix']
  if len(a)!=2 or any(len(r)!=2 for r in a) or any(x not in(-1,0,1)for r in a for x in r) or any(sum(a[k][i]*a[k][j]for k in range(2))!=(i==j)for i in range(2)for j in range(2)):raise ValueError('NOT_D4_ISOMETRY')
  # This adapter's actual frame is swapXY, not an arbitrary unbound D4 claim.
  if not equal(T,{'matrix':[[0,1],[1,0]],'translation':[0,0]}):errors.append('UNSUPPORTED_FRAME_BINDING')
  if digest(m)!=c['physical_core_hash']:errors.append('PHYSICAL_CORE_HASH')
  p=Path(__file__).parent/'references/core125_contract_source.py'
  if m['reference_contract_sha256']!=hashlib.sha256(p.read_bytes()).hexdigest():errors.append('SOURCE_CORE_CONTRACT')
  r=audit(m);errors+=r['errors'];evidence['common_partition']=r
  if not equal(c['solver_inputs'],[m['inputs'][1],m['inputs'][0],2]):errors.append('INPUT_FRAME')
  for k in ('stair','lift'):
   if not equal(rectangle(c[k],T),m[k]):errors.append('CORE_RECT:'+k)
  if not equal([rectangle(x,T)for x in c['lobby']],m['common_floor']):errors.append('COMMON_FLOOR')
  ops={o['id']:o for o in m['openings']}
  for u in ('A','B'):
   if not equal([rectangle(x,T)for x in c['unit_ownership'][u]],m['units'][u]):errors.append('OWNERSHIP:'+u)
   if not equal(rectangle(c['units'][u],T),m['units'][u][0]):errors.append('UNIT_BOUNDS:'+u)
   x,y,X,Y=map(F,ops[u+'.entry']['rect'])
   if not equal(point(c['entry_centers'][u],T),[(x+X)/2,(y+Y)/2]):errors.append('ENTRY_PORT:'+u)
 except (KeyError,ValueError,TypeError,IndexError)as ex:errors.append('FRAME_SCHEMA:'+str(ex))
 return {'status':'PASS_COMMON_FRAME_BINDING_ONLY'if not errors else'FAIL','errors':errors,'evidence':evidence,'contract_hash':digest(c),'whole_model_evaluated':False,'eligible_for_draft_export':False,'accepted':False,'release_allowed':False,'pending':['WHOLE_WORLD_GEOMETRY_OPERATIONS_AND_PLACEMENT_BINDING_NOT_EVALUATED']}
