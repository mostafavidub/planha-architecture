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
from group_readsets362 import build
from lobby_junction_bound362 import analyze
ROOT=Path(__file__).resolve().parents[1]
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
 q=rect(bound['rectangle']);portal={o['id']:o for o in m['openings']};clips=[];routeproof=[]
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
 return {'verdict':'PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE','model_hash':mh,'record_digest':digest(record),'whole_junction_region':bound['rectangle'],'whole_junction_area_m2':bound['area_m2'],'actual_transfer_extent':list(map(str,actualextent)),'actual_required_transfers':routeproof,'actual_entry_operation_use':operationproof,'source_row_digests':{k:digest(req[k])for k in ('core_concept','door_operation','opening_hosts','wall_network','partition_ledger','unit_independence')},'fixed_portal_family_bound':bound,'engineering_assumption':'Whole exact source single rectangular four-face required transfer junction includes legitimate inter-path turning/access margins; no new waiting/staging program, no extension beyond actual required traversal extent, and no need for footprint tiling. Scope is this Concept source profile, not other topology or relocated portals.','missing':[],'not_claimed':['Q04_COMPARATIVE_NECESSITY','GLOBAL_MINIMUM','TECHNICAL_CORE_CERTIFICATION','WHOLE_PLAN_ACCEPTANCE'],'parent_complete':False,'admission_allowed':False}
def evaluate(record,review):
 before=digest([record,review]);build(record,review,source_profile='SOURCE362');old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_source362.json';req=rows(record['candidate']['model'],review['raw_report']);out=intrinsic(record,req)
 finally:common.REGISTRY_NAME=old
 out.update(raw_review_digest=digest(review),new_fresh_execution=False,live_authority=False,source_files={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest()for n in ('common_role_closure362.py','lobby_junction_bound362.py')})
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return out
if __name__=='__main__':
 r=json.loads((ROOT/'staging362_core_notch/actual362.json').read_text());v=json.loads((ROOT/'review362_source_validation/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('common_role_closure_actual362.json').write_text(json.dumps(o,indent=2));print(o['verdict'],o['whole_junction_area_m2'])
