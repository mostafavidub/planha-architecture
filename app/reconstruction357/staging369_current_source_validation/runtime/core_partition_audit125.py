"""Independent cell partition/body check. Does not import constructor."""
from fractions import Fraction as F
from pathlib import Path
import json,copy,hashlib

def q(r):return tuple(F(str(x))for x in r)
def hit(a,b):return max(a[0],b[0])<min(a[2],b[2])and max(a[1],b[1])<min(a[3],b[3])
def inside(a,b):return b[0]<=a[0]<=a[2]<=b[2]and b[1]<=a[1]<=a[3]<=b[3]
def area(r):return(r[2]-r[0])*(r[3]-r[1])
def audit(m):
 W,L=map(F,m['inputs'][:2]);frame=(0,0,W,L);err=[];walls={k:q(v)for k,v in m['walls'].items()};ops={o['id']:q(o['rect'])for o in m['openings']};parts=[('wall',r)for r in walls.values()]+[('aperture',r)for r in ops.values()]+[('common',q(r))for r in m['common_floor']]+[(uid,q(r))for uid,rs in m['units'].items()for r in rs]+[(k,q(m[k]))for k in ('stair','lift')]
 for k,r in parts:
  if not inside(r,frame)or area(r)<=0:err.append('OUTSIDE_OR_NONPOSITIVE:'+k)
 xs=sorted({F(0),W}|{r[i]for k,r in parts for i in(0,2)});ys=sorted({F(0),L}|{r[i]for k,r in parts for i in(1,3)})
 for x,X in zip(xs,xs[1:]):
  for y,Y in zip(ys,ys[1:]):
   cell=(x,y,X,Y);n=sum(inside(cell,r)for k,r in parts)
   if n!=1:err.append('PARTITION_GAP_OR_OVERLAP:'+str(cell))
 for k,size in [('stair',(F('4.55'),F('2.45'))),('lift',(F('1.65'),F('1.65')))]:
  r=q(m[k]);
  if(r[2]-r[0],r[3]-r[1])!=size:err.append('SOURCE_CORE_SIZE:'+k)
 for o in m['openings']:
  r=q(o['rect']);host=q(m['wall_hosts'][o['host']])
  if not inside(r,host):err.append('APERTURE_HOST:'+o['id'])
  if any(hit(r,w)for w in walls.values()):err.append('APERTURE_BLOCKED:'+o['id'])
 if set(m['routes'])!={'stair_A','stair_B','lift_A','lift_B'}:err.append('ROUTE_INVENTORY')
 h=F('.35');stats={}
 for k,path in m['routes'].items():
  ps=list(map(q,path));src,uid=k.split('_')
  if not inside((ps[0][0]-h,ps[0][1]-h,ps[0][0]+h,ps[0][1]+h),q(m[src])):err.append('SOURCE_BODY:'+k)
  end=(ps[-1][0]-h,ps[-1][1]-h,ps[-1][0]+h,ps[-1][1]+h)
  if not any(inside(end,q(r))for r in m['units'][uid]):err.append('DESTINATION_BODY:'+k)
  length=0
  for a,b in zip(ps,ps[1:]):
   if a[0]!=b[0]and a[1]!=b[1]:err.append('DIAGONAL:'+k)
   sw=(min(a[0],b[0])-h,min(a[1],b[1])-h,max(a[0],b[0])+h,max(a[1],b[1])+h)
   if not inside(sw,frame)or any(hit(sw,r)for r in walls.values()):err.append('BODY_WALL:'+k)
   forbidden=[q(m['lift'if src=='stair'else'stair'])]+[q(r)for other,rs in m['units'].items()if other!=uid for r in rs]
   if any(hit(sw,r)for r in forbidden):err.append('BODY_WRONG_REGION:'+k)
   length+=abs(a[0]-b[0])+abs(a[1]-b[1])
  stats[k]=str(length)
 return {'status':'PASS_COMMON_OWNERSHIP_GEOMETRY_ONLY'if not err else'FAIL','errors':sorted(set(err)),'areas_m2':{k:str(sum(area(r)for name,r in parts if name==k))for k in sorted({k for k,r in parts})},'frame_m2':str(W*L),'route_lengths_m':stats,'accepted':False,'whole_unit_layout_evaluated':False}
if __name__=='__main__':
 p=Path(__file__).with_name('case39x7.07.json');m=json.loads(p.read_text());r=audit(m);assert not r['errors'],r
 neg=[]
 for name in ('blocked_entry','ownership_overlap','resized_lift'):
  n=copy.deepcopy(m)
  if name=='blocked_entry':n['walls']['bad']=n['openings'][0]['rect']
  elif name=='ownership_overlap':n['units']['B']=n['units']['A']
  else:n['lift'][2]=str(F(n['lift'][2])+F('.1'))
  a=audit(n);assert a['errors'];neg.append({'name':name,'errors':a['errors'][:3]})
 r.update(model_file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),negatives=neg);p.with_name('audit_result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
