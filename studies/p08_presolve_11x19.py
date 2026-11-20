"""Historical case 17: static contradictions, not a solver rerun or an IIS extract."""
import hashlib,inspect,json,math,subprocess,sys
from pathlib import Path
from fractions import Fraction as Q
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
BASE='84022bd9ea5c3876a72911ed4dc1544d90957c67'
RUN=44628962106
JOB=135930395558
RECEIPT='5991884cfa007a334090e30521e2e25dc34bc5a78de71138bc5537d878cb4482'
RAW={'W':'11','L':'19','n':2}
PINS={
 "dining_module118.py":"313b9673e8efcb48e9fa61d0ca24b6b33507310f",
 "approach_contract123.py":"4b0b6c1ae2395e99854ce8f31228e91aac36dcb5",
 "fixture_catalog114.json":"df6ef667f54d7e577e7027d33fe320ec0d16ad07",
 "search114.py": "65e0f278c9f9ef480388d3ea8056161c0a938a36",
 "engine114.py": "f999904358705c96bc1b3a2cb832d102ed33cba6",
 "contract114.py": "a2631c6a38a43b8d423edf82ad8d526ced1b8196",
 "capacity_program118.py": "955bc2344d8f92ce403a278e01aa933c824f833d",
 "schedule123.py": "9dcbbe278bed69b36b915d8b30254ea12936799c"
}
ORDER=(('KITCHEN_BATH_SHARED_SIDE',1),('SIDE_ROOTED_SERVICES',2),
 ('SIDE_ROOTED_SERVICES',1),('KITCHEN_BATH_SHARED_SIDE',2),('SIDE_ROOTED_SERVICES',0),('KITCHEN_BATH_SHARED_SIDE',0))
def need(ok,code):
 if not ok:raise ValueError(code)
def check_sources():
 snap={}
 for n,h in PINS.items():
  p=ENGINE/n;data=p.read_bytes()
  need(not p.is_symlink() and hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==h,'P08_SOURCE_PIN')
  snap[n]=hashlib.sha256(data).hexdigest()
 return snap
def exact(v):return Q(str(v))
def serialized_same(value,expected):
 # Captured grid-scaled numbers are native float; permit only sub-nanometre serialization noise.
 return math.isfinite(value) and abs(exact(value)-expected)<=Q(1,10**9)
def prove_bed_pair(width,depth,demand_x,demand_y):
 # Gold state is absence of both permitted separating axes, not merely a failing placement.
 return {'x_deficit_m':str(max(Q(0),demand_x-width)),'y_deficit_m':str(max(Q(0),demand_y-depth)),
  'contradiction':width<demand_x and depth<demand_y}
def prove_shared_apron(left_cap,right_cap,shared_min,bath_min):
 return {'left_deficit_m':str(max(Q(0),shared_min-left_cap)),'right_deficit_m':str(max(Q(0),bath_min-right_cap)),
  'contradiction':left_cap<shared_min and right_cap<bath_min}
class Rows:
 def __init__(self,m,grid):
  self.m=m;self.mat=m['matrix'];self.grid=grid;self.specs={s[0]:4*i for i,s in enumerate(m['specs'])}
  need(len(self.specs)==len(m['specs']) and len(m['row_metadata'])==self.mat.shape[0],'P08_CAPTURE_SHAPE')
 def coeff(self,i):
  row=self.mat.getrow(i)
  return {int(k):exact(v) for k,v in zip(row.indices,row.data,strict=True)}
 def eq(self,line,group,cols,rhs):
  matches=[i for i,r in enumerate(self.m['row_metadata']) if r=={'group':group,'source_line':line} and self.coeff(i)==cols]
  need(len(matches)==1,'P08_NAMED_EQUALITY_ROW')
  i=matches[0];need(serialized_same(self.m['lower'][i],rhs) and serialized_same(self.m['upper'][i],rhs),'P08_NAMED_EQUALITY_VALUE')
 def limit(self,line,cols,rhs):
  matches=[i for i,r in enumerate(self.m['row_metadata']) if r=={'group':'room_bounds','source_line':line} and self.coeff(i)==cols]
  need(len(matches)==1,'P08_NAMED_BOUND_ROW')
  i=matches[0];need(self.m['lower'][i]==float('-inf') and serialized_same(self.m['upper'][i],rhs),'P08_NAMED_BOUND_VALUE')
 def bounds(self,col):
  return tuple(exact(x[col])*self.grid for x in (self.m['bounds'].lb,self.m['bounds'].ub))
 def pair(self,a,b,sep):
  u,v=self.specs[a],self.specs[b];selected=[]
  directions=({u:1,u+2:1,v:-1},{v:1,v+2:1,u:-1},{u+1:1,u+3:1,v+1:-1},{v+1:1,v+3:1,u+1:-1})
  for line,cols in zip((146,147,148,149),directions,strict=True):
   matches=[]
   for i,r in enumerate(self.m['row_metadata']):
    if r!={'group':'physical_rectangle_separation','source_line':line}:continue
    row=self.coeff(i)
    if len(row)==4 and all(row.get(k)==v for k,v in cols.items()):
     selector,=set(row)-set(cols)
     if row[selector]<0:matches.append((i,selector))
   need(len(matches)==1,'P08_SEPARATION_ROW')
   i,selector=matches[0];selected.append(selector)
   need(self.m['lower'][i]==float('-inf') and serialized_same(self.m['upper'][i],-sep/self.grid),'P08_SEPARATION_GAP')
   need(self.bounds(selector)==(Q(0),self.grid) and self.m['integrality'][selector]==1,'P08_BINARY_SELECTOR')
  terms=dict.fromkeys(selected,1)
  need(len(terms)==4,'P08_SELECTOR_INVENTORY')
  matches=[i for i,r in enumerate(self.m['row_metadata']) if r=={'group':'physical_rectangle_separation','source_line':145} and self.coeff(i)==terms]
  need(len(matches)==1 and exact(self.m['upper'][matches[0]])==3,'P08_REQUIRED_SEPARATING_AXIS')

def inspect_capture(master,core,beds,topology,grid):
 q=Rows(master,grid);x,y,X,Y=map(Q,core['units']['A']);width,depth=X-x,Y-y
 gap=Q('.15');proof={'case':'11x19_n2','programme_bedrooms_per_unit':beds,'topology':topology,
  'box_width_m':str(width),'box_depth_m':str(depth),'named_violation':'UNKNOWN','contradiction':False}
 if beds==2:
  a,b=q.specs['bed1'],q.specs['bed2'];q.pair('bed1','bed2',gap)
  for k in (a,b):
   need(q.bounds(k)[0]>=x and q.bounds(k+1)[0]>=y,'P08_BED_LOWER_FRAME')
   q.limit(41,{k:1,k+2:1},X/grid);q.limit(41,{k+1:1,k+3:1},Y/grid)
  dx=q.bounds(a+2)[0]+q.bounds(b+2)[0]+gap
  dy=q.bounds(a+3)[0]+q.bounds(b+3)[0]+gap
  proof.update(demand_x_m=str(dx),demand_y_m=str(dy),**prove_bed_pair(width,depth,dx,dy))
  need(proof['contradiction'],'P08_EXPECTED_BED_CONTRADICTION')
  proof['named_violation']='BED_PAIR_RECTANGULAR_SEPARATION_IMPOSSIBLE_IN_SOURCE_BOX'
 elif topology=='KITCHEN_BATH_SHARED_SIDE':
  a,b,c=(q.specs[n] for n in ('bath','kitchen','entry_apron'))
  q.eq(59,'room_bounds',{a+1:1,a+3:1},Y/grid)
  q.eq(108,'kitchen_functional_boundary_attachment',{b:1,b+2:1,a:-1},-gap/grid)
  q.eq(109,'kitchen_functional_boundary_attachment',{b+1:1,b+3:1,a+1:-1,a+3:-1},Q())
  q.pair('bath','entry_apron',gap)
  q.limit(41,{a:1,a+2:1},X/grid)
  ex,ex2=q.bounds(c); ey,ey2=q.bounds(c+1); aw0,aw1=q.bounds(c+2); ah0,ah1=q.bounds(c+3)
  need(ex==ex2 and ey==ey2 and aw0==aw1 and ah0==ah1,'P08_ENTRY_APRON_FIXED')
  # Bath's top is within the verified serializer tolerance; use interior overlap with positive margin.
  need(ey<Y-Q(1,10**8) and ey+ah0>Y-q.bounds(a+3)[0]+Q(1,10**8),'P08_APRON_BATH_VERTICAL_OVERLAP')
  left_cap=ex-gap-q.bounds(b)[0];right_cap=X-(ex+aw0+gap)
  bath_min=q.bounds(a+2)[0];shared_min=q.bounds(b+2)[0]+gap+bath_min
  proof.update(left_max_m=str(left_cap),right_max_m=str(right_cap),shared_min_m=str(shared_min),bath_min_m=str(bath_min),
   **prove_shared_apron(left_cap,right_cap,shared_min,bath_min))
  need(proof['contradiction'],'P08_EXPECTED_SHARED_APRON_CONTRADICTION')
  proof['named_violation']='SHARED_SERVICE_PAIR_CANNOT_CLEAR_FIXED_ENTRY_APRON'
 return proof

def execute():
 before=check_sources()
 sys.path.insert(0,str(ENGINE))
 import contract114,capacity_program118,schedule123,search114,scipy.optimize,dining_module118,approach_contract123
 for f,n in ((contract114.core_first,'contract114.py'),(capacity_program118.proposed_program,'capacity_program118.py'),
             (schedule123.schedule,'schedule123.py'),(search114.propose,'search114.py'),
             (dining_module118.build,'dining_module118.py'),(approach_contract123.dining_actor_sweeps,'approach_contract123.py')):
  need(Path(inspect.getsourcefile(f)).resolve()==ENGINE/n,'P08_CALLABLE_SOURCE')
 W,L,n=contract114.parse(RAW);core=contract114.core_first(W,L)
 need(core['kind']=='COMPACT_CONNECTED_CENTRAL_CORE118','P08_CORE')
 programme=capacity_program118.proposed_program(core,RAW)
 ordered=tuple((b,top,v) for top,v in ORDER for b in (2,1))
 actual=schedule123.schedule(programme)
 need(tuple((r['bedrooms'],r['topology'],r['variant'])for r in actual)==ordered,'P08_HISTORICAL_SCHEDULE')
 rows=[]
 with patch.object(search114,'milp',side_effect=AssertionError('P08_NO_SOLVER')) as milp, \
      patch.object(scipy.optimize,'milp',side_effect=AssertionError('P08_NO_SCIPY_MILP')) as public_milp, \
      patch.object(scipy.optimize,'linprog',side_effect=AssertionError('P08_NO_LINPROG')) as lp, \
      patch.object(subprocess,'Popen',side_effect=AssertionError('P08_NO_SPAWN')) as proc:
  for b,top,v in ordered:
   captured=[]
   def observe(master):
    captured.append(inspect_capture(master,core,b,top,contract114.GRID))
    return 'P08_CAPTURED'
   status=search114.propose(core,b,3,variant=v,sleep_roles=programme['sleep_roles_by_count'][str(b)],
    ordered_macro=False,topology=top,diagnostic_capture=observe)
   need(status=='P08_CAPTURED' and len(captured)==1,'P08_CAPTURE_REQUIRED')
   rows.append({**captured[0],'variant':v,'witness_scope':'CURRENT_RECONSTRUCTION_OF_PINNED_HISTORICAL_CONSTRAINTS_NOT_ARCHIVED_CSR'})
  for sentinel in (milp,public_milp,lp,proc):sentinel.assert_not_called()
 need(check_sources()==before,'P08_SOURCE_CHANGED')
 return {'schema':'P08_CASE17_PRESOLVE_DIAGNOSTIC_V1','input':RAW.copy(),'historical_baseline_commit':BASE,
  'historical_run':RUN,'historical_job':JOB,'historical_safe_receipt_digest':RECEIPT,
  'historical_solver_status2_count':12,'historical_gate_calls':0,'historical_matrix_durable':False,
  'reconstructed_attempt_rows':len(rows),'proof_rows':sum(r['contradiction'] for r in rows),
  'unresolved_rows':sum(not r['contradiction'] for r in rows),'current_solver_calls':0,'rows':rows,
  'arithmetic_scope':'Exact source dimensions in Fractions. Emitted floating rows checked against exact coefficients/bounds with 1e-9 grid-unit serialization tolerance; no archived matrix or solver certificate.',
  'global_infeasibility_proven':False,'iis_extracted':False,'product_constraints_changed':False,'qualified':False}
if __name__=='__main__':print(json.dumps(execute(),sort_keys=True,allow_nan=False))
