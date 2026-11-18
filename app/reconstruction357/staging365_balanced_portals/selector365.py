"""Restricted source-profile selector, exact obstacle domains and balanced equations."""
from fractions import Fraction as F
from operation_domain365 import domains

def select(record):
 c=record['candidate']['packet']['core'];m=record['candidate']['model']
 if [u['id']for u in m['units']]!=['A','B']or F(m['profile']['body_m'])!=F('.7'):raise ValueError('SOURCE_TWO_UNIT_BODY_PROFILE_ONLY')
 ops={o['id']:o for o in m['openings']};openingwidths={u:F(ops[u+'.entry']['rect'][2])-F(ops[u+'.entry']['rect'][0])for u in('A','B')}
 if set(openingwidths.values())!={F('1.3')}:raise ValueError('SOURCE_ENTRY_WIDTH_PROFILE_ONLY')
 d=domains(record);b=d['B:1']
 if b['feasible_open_cells']or len(b['feasible_points'])!=1:raise ValueError('SINGLE_FIXED_B_POSITIVE_BRANCH_REQUIRED')
 xb=F(b['feasible_points'][0]);roots={u:F(m['common_routes']['stair_'+u][-1][1])for u in('A','B')};mid=(roots['A']+roots['B'])/2
 def portal(name):
  r=list(map(F,c[name]));o=list(map(F,ops[name+'.entry']['rect']));width=o[3]-o[1]
  if o[0]!=F(m['wall_hosts'][ops[name+'.entry']['host_wall_id']][0])or width<=0:raise ValueError('SOURCE_VERTICAL_PORTAL_HOST_REQUIRED')
  return r[1]+width/2,r[3]-width/2
 sl,su=portal('stair');ll,lu=portal('lift');dlo=max(F(0),2*(ll-mid),2*(mid-su));dhi=min(2*(lu-mid),2*(mid-sl))
 cells=[];points=set(map(F,d['A:-1']['feasible_points']))
 for a,z in d['A:-1']['feasible_open_cells']:
  a,z=F(a),F(z)
  if cells and a==cells[-1][1]and a in points:cells[-1]=(cells[-1][0],z)
  else:cells.append((a,z))
 viable=[]
 for a,z in cells:
  a=max(a,xb+dlo);z=min(z,xb+dhi)
  if a<z:viable.append((a,z))
 if not viable:raise ValueError('EMPTY_SOURCE_BALANCED_OPERATION_DOMAIN')
 a,z=sorted(viable,key=lambda p:(-(p[1]-p[0]),p[0]))[0];xa=(a+z)/2;delta=xa-xb;ps=mid-delta/2;pl=mid+delta/2
 return {'entry_x':{'A':str(xa),'B':str(xb)},'portal_y':{'stair':str(ps),'lift':str(pl)},'slide_direction':{'A':-1,'B':1},'selected_interval':list(map(str,(a,z))),'selection':'MIDPOINT_MAXIMIZES_MIN_COORDINATE_SLACK_WITHIN_WIDEST_FEASIBLE_COMPONENT','engineering_assumption':'Coordinate slack is a deterministic search choice, not a construction tolerance or clearance standard. Exact physical reviews remain required.','operation_domains':d,'portal_intervals':{'stair':list(map(str,(sl,su))),'lift':list(map(str,(ll,lu)))},'candidate_policy':'INDEPENDENT_BALANCED_TRADEOFF_NOT_PARETO_REPAIR','accepted':False}
