"""Source-bound operational separation reservation, never added usable floor.
No area/width cutoff grants acceptance. Exact source selector slack, moving
assembly thickness/mount offset, functional source wall and host define cell.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import common
from common import digest,rows
from modules_spatial import rect,intersection,difference,union_area
from guest_closure import transformed_rect
from groups381 import build
from wall_origin381 import base
ROOT=Path(__file__).resolve().parents[1]
def require_registered_selection(policy):
 from family378 import enumerate_family,load_parent
 selected=enumerate_family(load_parent())[1]
 if policy['slide_direction']!={'A':-1,'B':1}or policy['selection']!='FINITE_INTERIOR_QUARTILE_SOURCE_SELECTION':raise ValueError('UNSUPPORTED_REGISTERED378_PROFILE')
 if any(policy.get(k)!=v for k,v in selected.items()):raise ValueError('EXACT_REGISTERED378_RANK1_REQUIRED')
 lo,hi=map(F,policy['selected_interval']);x=F(policy['entry_x']['A'])
 if not lo<x<hi:raise ValueError('STRICT_INTERIOR_COORDINATE_REQUIRED')
 return lo,hi,x

def derive(record,req):
 m=record['candidate']['model'];core=record['candidate']['packet']['core'];policy=core['balanced_portals365'];out=[];base_model,origin=base(record)
 for k in ('door_operation','bath_service_operation','opening_hosts','wall_network','partition_ledger'):
  if req[k]['status']!='PASS_LIMITED'or req[k].get('model_hash')!=digest(m):raise ValueError('CURRENT_SEPARATION_FUNCTION:'+k)
 # The producer currently defines one source-selected A-negative branch.
 lo,hi,x=require_registered_selection(policy)
 u=next(u for u in m['units']if u['id']=='A');op=next(o for o in m['operations']['doors']if o['opening_id']=='A.entry');opening=next(o for o in m['openings']if o['id']=='A.entry');host=rect(base_model['wall_hosts'][opening['host_wall_id']]);rail=rect(op['rail_envelope']);closed,opened=rect(op['closed_panel']),rect(op['open_panel']);span=F(opening['rect'][2])-F(opening['rect'][0]);thickness=F(op['mount']['panel_thickness_m']);offset=F(op['mount']['offset_m'])
 if op['mount']['face']!='min'or op['source_slide_direction365']!=-1 or list(map(F,op['translation']))!=[-span,F(0)]:raise ValueError('SOURCE_REVERSE_MOTION_BINDING')
 if opened!=(closed[0]-span,closed[1],closed[2]-span,closed[3])or rail!=(opened[0],opened[1],closed[2],closed[3]):raise ValueError('EXACT_LINEAR_SWEEP_RAIL')
 if closed[3]-closed[1]!=thickness or host[1]-closed[3]!=offset or rail[0]!=x-3*span/2:raise ValueError('SOURCE_MOUNT_PROFILE_GEOMETRY')
 wallface=lo-3*span/2;region=(wallface,rail[1],rail[0],host[1]);left=[]
 for p in m['module_placements']:
  if p['unit_id']!='A'or p['room_id']!='bath':continue
  if digest(p['module'])!=p['module_hash']:raise ValueError('MODULE_HASH')
  for sid,r in p['module']['walls'].items():
   wid=p['id_map'][sid];q=transformed_rect(r,p['transform'])
   if q!=rect(m['walls'][wid]):raise ValueError('SOURCE_MODULE_WALL_JOIN')
   if q[2]==wallface and q[1]<=region[1]and q[3]>=region[3]:left.append({'wall_id':wid,'source_module_hash':p['module_hash'],'source_id':sid,'world_geometry':list(map(str,q))})
 if not left or region[0]>=region[2]or region[3]-region[1]!=thickness+offset or region[2]-region[0]!=x-lo:raise ValueError('EXACT_OPERATIONAL_SEPARATION_BOUNDARIES')
 if region[0]<host[0]or region[2]>host[2]or difference([region],list(map(rect,u['ownership']))):raise ValueError('RESERVATION_OUTSIDE_SOURCE_OWNERSHIP_HOST')
 # Does not replace a required floor activity or aperture. Positive overlap is
 # forbidden; it is an exact non-usable separation sliver next to the assembly.
 protected=list(u['activities'].values())+[o['rect']for o in m['openings']]
 if any(intersection(region,rect(r))for r in protected):raise ValueError('RESERVATION_COVERS_REQUIRED_ACTIVITY_OR_PORTAL')
 out.append({'unit':'A','region':list(map(str,region)),'area_m2':str(union_area([region])),'classification':'ENGINEERING_OPERATIONAL_SEPARATION_RESERVATION_NOT_USABLE_LIVING','source_wall_binding':left,'source_host_id':opening['host_wall_id'],'source_host_origin':origin,'source_operation_digest':digest(op),'source_selector_interval':policy['selected_interval'],'coordinate_slack_m':str(x-lo),'source_panel_thickness_m':str(thickness),'source_mount_offset_m':str(offset),'usable_floor_capacity_increment':0,'engineering_assumption':'Actual positive registered rank1 interior separation (not midpoint/max-min slack) between rigid moving entry assembly and verified functional wall is an operational clearance reservation, including the source mount-offset depth; not a construction tolerance, furniture area, or added capacity. No arbitrary small-area cutoff.'})
 return out
def evaluate(record,review):
 build(record,review,source_profile='SOURCE_BALANCED365');old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_source365.json';req=rows(record['candidate']['model'],review['raw_report']);r=derive(record,req)
 finally:common.REGISTRY_NAME=old
 return {'schema':'BALANCED365_EXACT_ENTRY_SEPARATION_RESERVATION','model_hash':digest(record['candidate']['model']),'record_digest':digest(record),'fresh_result_digest':digest(review),'reservations':r,'parent_complete':False,'admission_allowed':False,'fresh_executed':False}
