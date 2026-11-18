"""Same-fresh conceptual lobby transfer role, not compactness or delivery.
Engineering interpretation: the exact source rectangular junction of four actual
required portal traversals supports its transfer/turning margins. Fixed-portal
minimum rectangle alone is insufficient; actual checked traversal and door use
are mandatory. No new staging occupants or technical core use is invented.
"""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
import common
from common import digest,rows
from modules_spatial import rect,intersection,difference,union_area,source_sweeps
from groups390 import build
from lobby_junction_bound362 import analyze
ROOT=Path(__file__).resolve().parents[1]
def interior_clearance(model,junction):
 # Fixed source inventory, not caller-provided obstacle omissions. Actor use in
 # COMMON is functional activity, not a simultaneously stationary obstacle.
 if set(model['operations'])!={'doors','closets','kitchen','dining_chairs'}:raise ValueError('UNSUPPORTED_OPERATION_INVENTORY')
 blocked=[]
 def add(name,r):blocked.append((name,rect(r)))
 for k,r in model['walls'].items():add('wall/'+k,r)
 for u in model['units']:
  for k,r in u['fixtures'].items():add('fixture/'+u['id']+'/'+k,r)
 for op in model['operations']['doors']:
  if op['kind']not in ('sliding_linear','pocket_source113'):raise ValueError('UNSUPPORTED_DOOR_BLOCKED_PROFILE')
  for k in ('closed_panel','open_panel'):add('door/'+op['opening_id']+'/'+k,op[k])
  add('door/'+op['opening_id']+'/rail_or_pocket',op['rail_envelope']if op['kind']=='sliding_linear'else op['pocket'])
  a,b=rect(op['closed_panel']),rect(op['open_panel']);add('door/'+op['opening_id']+'/linear_motion',list(map(str,(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))))
 for i,op in enumerate(model['operations']['closets']):
  for j,r in enumerate(op['shell_rects']):add('closet_shell/'+str(i)+'/'+str(j),r)
  for panel in op['panels']:
   for k in ('closed_panel','open_panel','rail_envelope'):add('closet/'+str(i)+'/'+panel['id']+'/'+k,panel[k])
   a,b=rect(panel['closed_panel']),rect(panel['open_panel'])
   if not(a[0]==b[0]or a[1]==b[1]):raise ValueError('UNSUPPORTED_CLOSET_NONLINEAR_PROFILE')
   add('closet/'+str(i)+'/'+panel['id']+'/linear_motion',list(map(str,(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))))
 for i,op in enumerate(model['operations']['kitchen']):
  if 'motion_envelopes'not in op:raise ValueError('KITCHEN_BLOCKED_ENVELOPES_MISSING')
  for j,r in enumerate(op['motion_envelopes']):add('kitchen_motion/'+str(i)+'/'+str(j),r)
 for i,op in enumerate(model['operations']['dining_chairs']):
  for k in ('closed_rect','open_rect','occupied_body'):add('chair/'+str(i)+'/'+k,op[k])
  a,b=rect(op['closed_rect']),rect(op['open_rect']);add('chair_motion/'+str(i),list(map(str,(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))))
 hits=[{'source':name,'intersection':list(map(str,hit))}for name,r in blocked if(hit:=intersection(junction,r))is not None]
 if hits:raise ValueError('INTERIOR_OBSTACLE_OR_OPERATION_ISLAND:'+hits[0]['source'])
 return {'predicate':'EXACT_SOURCE_SINGLE_RECTANGLE_WITH_NO_POSITIVE_AREA_INTERIOR_BLOCKED_INTERSECTION','blocked_inventory_digest':digest([[n,list(map(str,r))]for n,r in blocked]),'blocked_inventory_count':len(blocked),'blocked_inventory_ids':[n for n,r in blocked],'positive_interior_intersections':hits,'source_body_m':model['profile']['body_m'],'connectedness_basis':'Single source rectangle minus zero positive-area blocked inventory is a connected convex junction. Actual traversal/operation checks remain separate mandatory prerequisites.','not_inferred_from_bounding_box_alone':True}

def intrinsic(record,req):
 m=record['candidate']['model'];mh=digest(m);bound=analyze(record)
 if bound['verdict']!='PASS_RECTANGULAR_FIXED_PORTAL_BOUND_ONLY':raise ValueError('SOURCE_FIXED_PORTAL_BOUND_UNESTABLISHED')
 for k in ('core_concept','door_operation','opening_hosts','wall_network','partition_ledger','unit_independence'):
  if req[k]['status']!='PASS_LIMITED' or req[k].get('model_hash')!=mh:raise ValueError('CURRENT_FRESH_PREREQUISITE:'+k)
 core=req['core_concept']['evidence']['witness'];doors=req['door_operation']['evidence']['witness']
 required={'stair_A':('stair','A'),'lift_A':('lift','A'),'stair_B':('stair','B'),'lift_B':('lift','B')}
 if core.get('errors') or core.get('pending') or doors.get('errors') or doors.get('pending'):raise ValueError('FRESH_FUNCTION_NOT_CLOSED')
 if {r['route']:(r['source'],r['destination'])for r in core['routes']}!=required or set(m['common_routes'])!=set(required):raise ValueError('REQUIRED_TRANSFER_INVENTORY')
 if F(core['body_m'])!=F(m['profile']['body_m']):raise ValueError('CORE_BODY_PROFILE')
 if not {'A.entry','B.entry'}<=set(doors['actual_operation_ids']):raise ValueError('ENTRY_OPERATION_INVENTORY')
 q=rect(bound['rectangle']);clearance=interior_clearance(m,q);portal={o['id']:o for o in m['openings']};clips=[];routeproof=[]
 for name,(source,uid)in required.items():
  path=m['common_routes'][name];sweeps=source_sweeps(path,m['profile']['body_m']);start=portal[source+'.entry'];end=portal[uid+'.entry']
  if not any(intersection(s,rect(start['rect']))for s in sweeps)or not any(intersection(s,rect(end['rect']))for s in sweeps):raise ValueError('REQUIRED_TRAVERSAL_PORTAL_BINDING')
  clipped=[i for s in sweeps if(i:=intersection(q,s))]
  if not clipped:raise ValueError('NO_ACTUAL_JUNCTION_TRAVERSAL')
  clips+=clipped;routeproof.append({'route':name,'path':path,'source_opening':start['id'],'destination_opening':end['id'],'junction_sweeps':[list(map(str,r))for r in clipped]})
 # All four required portal faces must be reached by actual checked route bodies,
 # not merely hypothetical centered approaches from the bounded-family helper.
 actualextent=(min(r[0]for r in clips),min(r[1]for r in clips),max(r[2]for r in clips),max(r[3]for r in clips))
 if actualextent!=q:raise ValueError('ACTUAL_TRANSFER_EXTENT_DOES_NOT_BIND_WHOLE_SOURCE_JUNCTION')
 operationproof=[]
 for uid in ('A','B'):
  ops=[o for o in m['operations']['doors']if o['opening_id']==uid+'.entry']
  if len(ops)!=1:raise ValueError('ACTUAL_ENTRY_OPERATION_UNIQUE')
  op=ops[0];states=[s for s in op['states']if s['role_id']=='lobby'];segments=[s for s in op.get('continuous_actor_segments',[])if s['role_id']=='lobby'and s['unit']=='COMMON']
  if len(states)<2 or not segments:raise ValueError('CURRENT_LOBBY_ACTOR_CONTINUOUS_USE_MISSING')
  poses=[rect(s['actor_rect'])for s in states];continuous=[]
  for seg in segments:
   a,b=rect(seg['actor_start']),rect(seg['actor_end'])
   if a not in poses or b not in poses or not(a[0]==b[0]or a[1]==b[1]):raise ValueError('ENTRY_ACTOR_SEGMENT_BINDING')
   continuous.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
  if difference(poses+continuous,[q]):raise ValueError('REQUIRED_ENTRY_ACTIVITY_OUTSIDE_JUNCTION')
  if not any(intersection(a,b)for a in continuous for b in clips):raise ValueError('ENTRY_OPERATION_NOT_CONNECTED_TO_TRANSFER')
  operationproof.append({'opening_id':op['opening_id'],'source_operation_digest':digest(op),'poses':[list(map(str,r))for r in poses],'continuous_actor_sweeps':[list(map(str,r))for r in continuous]})
 # Deliberately no point-by-point footprint tiling test. The whole source-defined
 # rectangle is the four-face transfer junction; inter-path floor is legitimate
 # maneuver margin under this explicit engineering role interpretation.
 return {'verdict':'PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE','model_hash':mh,'record_digest':digest(record),'whole_junction_region':bound['rectangle'],'whole_junction_area_m2':bound['area_m2'],'actual_transfer_extent':list(map(str,actualextent)),'connected_source_domain_witness':clearance,'actual_required_transfers':routeproof,'actual_entry_operation_use':operationproof,'source_row_digests':{k:digest(req[k])for k in ('core_concept','door_operation','opening_hosts','wall_network','partition_ledger','unit_independence')},'fixed_portal_family_bound':bound,'engineering_assumption':'Whole exact source single rectangular four-face required transfer junction includes legitimate inter-path turning/access margins; no new waiting/staging program, no extension beyond actual required traversal extent, and no need for footprint tiling. Scope is this Concept source profile, not other topology or relocated portals.','missing':[],'not_claimed':['Q04_COMPARATIVE_NECESSITY','GLOBAL_MINIMUM','TECHNICAL_CORE_CERTIFICATION','WHOLE_PLAN_ACCEPTANCE'],'parent_complete':False,'admission_allowed':False}
def evaluate(record,review):
 before=digest([record,review]);build(record,review,source_profile='SOURCE_BALANCED365');old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_source365.json';req=rows(record['candidate']['model'],review['raw_report']);out=intrinsic(record,req)
 finally:common.REGISTRY_NAME=old
 out.update(raw_review_digest=digest(review),new_fresh_execution=False,live_authority=False,source_files={n:hashlib.sha256((ROOT/'semantic_rules357'/n).read_bytes()).hexdigest()for n in ('common_role_closure365.py','lobby_junction_bound362.py')})
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return out
