"""Own SERVICE365 common-role inventory. No single-rectangle365 role transfer."""
import json
from pathlib import Path
import common
from common import digest,rows
from group_readsets_service365 import build
from modules_spatial import rect,intersection,union_area,difference,source_sweeps
ROOT=Path(__file__).resolve().parents[1]
def evaluate(record,review):
 build(record,review,source_profile='SOURCE_SERVICE365');m=record['candidate']['model'];old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_service365.json';req=rows(m,review['raw_report'])
 finally:common.REGISTRY_NAME=old
 for k in ('core_concept','door_operation','opening_hosts','wall_network','partition_ledger'):
  if req[k]['status']!='PASS_LIMITED':raise ValueError('COMMON_SERVICE_FRESH_PREREQUISITE')
 regions=[]
 for raw in m['common_spaces']['lobby']:
  q=rect(raw);routecover=[];routeids=[]
  for name,path in m['common_routes'].items():
   clips=[r for s in source_sweeps(path,m['profile']['body_m'])if(r:=intersection(s,q))]
   if clips:routeids.append(name);routecover+=clips
  actual_use=[]
  for op in m['operations']['doors']:
   if op['opening_id']not in ('A.entry','B.entry'):continue
   actual_use +=[rect(s['actor_rect'])for s in op['states']if s['role_id']=='lobby']
   for seg in op['continuous_actor_segments']:
    if seg['role_id']=='lobby':
     a,b=rect(seg['actor_start']),rect(seg['actor_end']);actual_use.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
  clipped=[r for a in actual_use if(r:=intersection(a,q))];remaining=difference([q],routecover+clipped)
  regions.append({'region':raw,'area_m2':str(union_area([q])),'required_routes_traversing':routeids,'actual_source_route_or_actor_extent_m2':str(union_area(routecover+clipped)),'outside_measured_footprints_m2':str(union_area(remaining)),'outside_measured_footprints_regions':[list(map(str,r))for r in remaining],'not_uselessness_proof':True})
 return {'schema':'SERVICE365_OWN_COMMON_SOURCE_INVENTORY','verdict':'UNKNOWN_WHOLE_MULTI_REGION_COMMON_ROLE_NOT_ESTABLISHED','model_hash':digest(m),'record_digest':digest(record),'fresh_result_digest':digest(review),'regions':regions,'actual_common_routes':m['common_routes'],'fresh_source_row_digests':{k:digest(req[k])for k in ('core_concept','door_operation','opening_hosts','wall_network','partition_ledger')},'missing':['WHOLE_TWO_REGION_SOURCE_JUNCTION_AND_TAIL_FUNCTION_OR_VALID_MARGIN_PROOF'],'scope':'Current source conceptual access/operation checks present; source two-region lobby is not balanced365 single-rectangle junction. Uncovered footprints do not prove uselessness; legitimate margins may qualify only with own source-functional evidence.','parent_complete':False,'admission_allowed':False,'fresh_execution':False}
