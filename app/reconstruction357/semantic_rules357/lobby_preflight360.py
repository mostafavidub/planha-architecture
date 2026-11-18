"""Read-only source360 junction evidence. No current-fresh or role acceptance."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,difference,intersection,union_area,source_sweeps
from supporting_floor import analyze
from geometry_support_preflight358 import evaluate as public_preflight
ROOT=Path(__file__).resolve().parents[1]
def evaluate(record):
 m=record['candidate']['model'];core=record['candidate']['packet']['core'];before=digest(record)
 if digest(m)!=record['candidate']['model_digest']:raise ValueError('MODEL_DIGEST')
 lobby=list(map(rect,m['common_spaces']['lobby']))
 if len(lobby)!=1 or lobby!=list(map(rect,core['lobby'])):raise ValueError('SINGLE_SOURCE_JUNCTION_REQUIRED')
 q=lobby[0];h=F(m['profile']['body_m'])/2;ports=[];anchors=[]
 for o in m['openings']:
  if 'lobby' not in o['connects']:continue
  a,b,c,d=rect(o['rect']);side=None
  if c==q[0] and b>=q[1] and d<=q[3]:side='left';anchor=[q[0]+h,(b+d)/2]
  elif a==q[2] and b>=q[1] and d<=q[3]:side='right';anchor=[q[2]-h,(b+d)/2]
  elif d==q[1] and a>=q[0] and c<=q[2]:side='bottom';anchor=[(a+c)/2,q[1]+h]
  elif b==q[3] and a>=q[0] and c<=q[2]:side='top';anchor=[(a+c)/2,q[3]-h]
  else:raise ValueError('PORTAL_NOT_SOURCE_JUNCTION_FACE')
  anchors.append(anchor);ports.append({'id':o['id'],'side':side,'rect':o['rect'],'connects':o['connects'],'scope':o.get('source_scope_reference','actual modeled sliding operation')})
 if {p['side'] for p in ports}!={'left','right','bottom','top'}:raise ValueError('FOUR_REQUIRED_SOURCE_PORTAL_FACES')
 obs=list(m['walls'].values())+[o['open_panel']for o in m['operations']['doors']]
 reach=analyze([list(map(str,q))],obs,anchors,m['profile']['body_m'],seconds=5)
 transfer=rect(core['notch360']['new_A_floor_ownership']);A=next(u for u in m['units']if u['id']=='A');public=public_preflight(m)
 transferred_roles=[{'role':k,'intersection_area_m2':str(union_area([i for r in rs if (i:=intersection(transfer,rect(r)))is not None]))}for k,rs in A['rooms'].items()if any(intersection(transfer,rect(r))for r in rs)]
 wallgap=difference(list(map(rect,m['walls'].values())),list(map(rect,m['physical_wall_network']['solids'].values())));extra=difference(list(map(rect,m['physical_wall_network']['solids'].values())),list(map(rect,m['walls'].values())))
 if before!=digest(record):raise ValueError('INPUT_MUTATION')
 return {'schema':'SOURCE360_LOBBY_PREFLIGHT_ONLY','model_hash':digest(m),'record_digest':digest(record),'lobby':{'region':list(map(str,q)),'area_m2':str(union_area(lobby)),'source_portals':ports,'body_junction_geometry':reach,'geometry_unsupported_area_m2':str(union_area(difference(lobby,list(map(rect,reach.get('support_regions',[])))))),'common_routes':m['common_routes'],'source_operation_ids':[o['opening_id']for o in m['operations']['doors']if o['opening_id']in[p['id']for p in ports]],'proposed_role_predicate':'ENGINEERING_ROLE_OPERATIONALIZATION: exact source-defined convex four-face required portal junction with current verified transfer/access/operations, not arbitrary standing/staging or technical core approval. Fresh prerequisite not yet supplied.'},'transferred_floor':{'region':list(map(str,transfer)),'area_m2':str(union_area([transfer])),'actual_named_role_intersections':transferred_roles,'functional_role':'UNKNOWN_CURRENT_FRESH_REQUIRED_NO_ROLE_FROM_LABEL'},'public_geometry_preflight':public,'physical_wall_union_difference_m2':{'missing':str(union_area(wallgap)),'extra':str(union_area(extra))},'fresh_execution':False,'source_use_verified':False,'whole_role_status':'UNKNOWN_CURRENT_FRESH_AND_SCOPE_AUDIT_REQUIRED','admission_allowed':False}
if __name__=='__main__':
 r=json.loads((ROOT/'staging360_core_notch/actual360.json').read_text());o=evaluate(r);Path(__file__).with_name('lobby_preflight_actual360.json').write_text(json.dumps(o,indent=2));print(o['lobby']['geometry_unsupported_area_m2'],o['transferred_floor'],[(u['unit'],u['unresolved_area_m2'])for u in o['public_geometry_preflight']['rows']])
