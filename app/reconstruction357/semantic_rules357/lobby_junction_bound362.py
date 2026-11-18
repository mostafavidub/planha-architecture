"""Engineering lower bound for fixed-portal axis-aligned rectangular junctions.
No whole-role, motion, global necessity, or acceptance authority.
"""
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,difference,union_area

def analyze(record):
 out={'verdict':'UNKNOWN','parent_complete':False,'delivery_allowed':False,'live_authority':False,'missing':[]}
 try:
  m=record['candidate']['model'];core=record['candidate']['packet']['core']
  if digest(m)!=record['candidate']['model_digest']:raise ValueError('MODEL_DIGEST')
  qs=[rect(r)for r in m['common_spaces']['lobby']]
  if len(qs)!=1 or qs!=[rect(r)for r in core['lobby']]:raise ValueError('EXACT_SINGLE_SOURCE_RECTANGLE')
  q=qs[0];body=F(m['profile']['body_m']);h=body/2
  if body<=0:raise ValueError('SOURCE_BODY_POSITIVE')
  openings=[o for o in m['openings']if 'lobby'in o['connects']]
  if len({o['id']for o in openings})!=len(openings):raise ValueError('DUPLICATE_PORTAL')
  approaches=[];ports=[]
  for o in openings:
   if len(o['connects'])!=2 or o['connects'].count('lobby')!=1:raise ValueError('PORTAL_CONNECTIONS')
   a,b,c,d=rect(o['rect'])
   if c==q[0]and q[1]<=b<d<=q[3]:side='left';x,y=q[0]+h,(b+d)/2;width=d-b
   elif a==q[2]and q[1]<=b<d<=q[3]:side='right';x,y=q[2]-h,(b+d)/2;width=d-b
   elif d==q[1]and q[0]<=a<c<=q[2]:side='bottom';x,y=(a+c)/2,q[1]+h;width=c-a
   elif b==q[3]and q[0]<=a<c<=q[2]:side='top';x,y=(a+c)/2,q[3]-h;width=c-a
   else:raise ValueError('UNBOUND_PORTAL_FACE')
   r=(x-h,y-h,x+h,y+h)
   if width<body or difference([r],[q]):raise ValueError('APPROACH_DOES_NOT_FIT_SOURCE_BODY')
   approaches.append(r);ports.append({'id':o['id'],'side':side,'connects':o['connects'],'opening_rect':o['rect'],'body_approach':list(map(str,r))})
  if {p['side']for p in ports}!={'left','right','bottom','top'}:raise ValueError('FOUR_FACE_INVENTORY_REQUIRED')
  bound=(min(r[0]for r in approaches),min(r[1]for r in approaches),max(r[2]for r in approaches),max(r[3]for r in approaches))
  if bound!=q:raise ValueError('RECTANGULAR_BOUND_NOT_TIGHT')
  out.update(verdict='PASS_RECTANGULAR_FIXED_PORTAL_BOUND_ONLY',model_digest=digest(m),record_digest=digest(record),ports=ports,rectangle=list(map(str,q)),minimum_rectangle=list(map(str,bound)),area_m2=str(union_area([q])),engineering_assumption='Axis-aligned single rectangle with immutable portal faces and centered inboard source-body approach poses. No moved-portal or other-topology claim.',missing=['CURRENT_SOURCE_REQUIRED_ARRIVAL_TRANSFER_ONWARD_USE','WHOLE_JUNCTION_ROLE_SCOPE_REVIEW','ELIGIBLE_FINITE_COMPARISON_PROTECTED_VECTOR'])
 except (ValueError,KeyError,TypeError,ZeroDivisionError)as e:out['missing']=[str(e)]
 return out
