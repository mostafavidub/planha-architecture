"""Exact branch146 portal-support margin; bounded pre-construction trim diagnostic.
No fresh, model modification, uselessness proof, or whole-parent admission.
"""
import json
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,intersection,difference,union_area,source_sweeps
from branch_margin_inventory_service365 import evaluate as inventory
from circulation_role_service365 import evaluate as circulation
ROOT=Path(__file__).resolve().parents[1]
def transverse_port_support(private,source_ports,body):
 """Extend a checked source port transversely across its actual corridor cell.
 No longitudinal extension beyond the source approach interval is permitted.
 """
 allowed=[];joins=[]
 for p in source_ports:
  q=rect(p['source_port_region']);dims=(q[2]-q[0],q[3]-q[1]);axis=0 if dims[0]>dims[1]else 1
  for c in private:
   normal=1-axis
   if not intersection(c,q) or c[normal+2]-c[normal]<F(body):continue
   # Source branch146 corridors are one metre clear; verify geometry rather
   # than granting arbitrary wide-room margins.
   if c[normal+2]-c[normal]!=1:continue
   lo=max(q[axis],c[axis]);hi=min(q[axis+2],c[axis+2]);z=list(c);z[axis]=lo;z[axis+2]=hi
   if lo<hi:
    allowed.append(tuple(z));joins.append({'opening_id':p['opening_id'],'source_port_digest':p['source_port_digest'],'actual_port_digest':p['actual_port_digest'],'source_corridor_cell':list(map(str,c)),'supporting_cross_section':list(map(str,z))})
 return allowed,joins

def evaluate(record,review):
 inv=inventory(record,review);circ=circulation(record,review);m=record['candidate']['model'];units=[]
 for ui in inv['units']:
  uid=ui['unit'];u=next(u for u in m['units']if u['id']==uid);cu=next(u for u in circ['units']if u['unit']==uid);private=list(map(rect,u['rooms']['private_circulation']));allowed,joins=transverse_port_support(private,ui['source_ports'],m['profile']['body_m']);res=[rect(q)for q in ui['outside_regions']];left=difference(res,allowed)
  # No removal is performed. Required source approaches, all actual body
  # routes, and actor continuous motion are retained in the proposed bound.
  protected=[rect(p['source_port_region'])for p in ui['source_ports']]
  protected +=[s for path in u['routes'].values()for s in source_sweeps(path,m['profile']['body_m'])]
  for op in m['operations']['doors']:
   if not op['opening_id'].startswith(uid+'.bed'):continue
   protected +=[rect(s['actor_rect'])for s in op['states']]
   for s in op['continuous_actor_segments']:
    a,b=rect(s['actor_start']),rect(s['actor_end']);protected.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
  collisions=[{'residual':list(map(str,q)),'protected_overlap':list(map(str,z))}for q in left for p in protected if(z:=intersection(q,p))]
  units.append({'unit':uid,'source_port_margin_joins':joins,'legitimate_port_cross_section_scope':'Engineering operationalization: actual checked source approach plus full source corridor transverse clearance. No invented longitudinal tail or standing activity.','remaining_m2':str(union_area(left)),'remaining_regions':[list(map(str,q))for q in left],'remaining_protected_domain_intersections':collisions,'whole_role_complete':False,'trim_preconditions':['Recompute constructor source boundary, floor partition and all module hosting; preserve every source approach and complete operation, not just this diagnostic subset.','Rebuild/replay and own fresh all applicable functions before any comparative or role acceptance.'],'remaining_status':'UNKNOWN_SOURCE_BRANCH_END_BEYOND_CURRENT_REQUIRED_DOMAINS_NOT_PROVEN_USELESS'})
 return {'schema':'SERVICE365_BRANCH_PORT_MARGIN_V2','model_digest':digest(m),'record_digest':digest(record),'fresh_result_digest':digest(review),'source_inventory_digest':digest(inv),'units':units,'source_cause':'private_branch_hall146 uses fixed macro end 10.65 for branch floor and 10.65..10.8 wall, rather than deriving end from last protected portal/domain.','source_file':'planha_general150_runtime_work/private_branch_hall146.py','source_sha256':record['trace']['source_inventory']['planha_general150_runtime_work/private_branch_hall146.py'],'engineering_assumption':'Source approach corridor transverse margins can support checked passage without footprint tiling; longitudinal excess is not covered by that assumption.','admission_allowed':False,'fresh_execution':False}
if __name__=='__main__':
 r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());v=json.loads((ROOT/'review365_service_source_validation/result.json').read_text());print(json.dumps(evaluate(r,v),indent=2))
