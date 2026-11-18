"""Exact swap-XY of actual model geometry, with immutable embedded sources.
Producer only. Independent frame/whole gates decide eligibility.
"""
from copy import deepcopy
from fractions import Fraction as F
from contract114 import S,digest
from d4_contract125 import matrix

RECT_KEYS={'rect','plan_rect','closed_panel','open_panel','pocket','rail_envelope','panel_rect','actor_rect','actor_start','actor_end','closed_rect','open_rect','occupied_body','standing_body','closed_tray','open_tray','body_rect','front_rect','region'}
POINT_KEYS={'hand_point','hand_start','hand_end','center','hinge','closed_actor','open_actor','open_access','shelf_target','held_target','grip_closed','grip_open','storage_target','workpoint','access_point','point','target','actor','hand'}
VECTOR_KEYS={'translation','actor_offset_m','normal','front_normal'}
RECT_LIST_KEYS={'shell_rects','motion_envelopes','regions','parts'}
PATH_KEYS={'path','egress_route','route','open_transfer_points'}

def point(p):return [S(F(str(p[1]))),S(F(str(p[0])))]
def rect(r):x,y,X,Y=map(lambda v:F(str(v)),r);return list(map(S,(y,x,Y,X)))
def placement(t):
 a=matrix(t['matrix']);return {'matrix':[[int(x)for x in a[1]],[int(x)for x in a[0]]],'translation':point(t['translation'])}
def canonical(t):
 a=matrix(t['matrix']);return {'matrix':[[int(a[0][1]),int(a[0][0])],[int(a[1][1]),int(a[1][0])]],'translation':deepcopy(t['translation'])}
def geometry(x,key=''):
 if key in ('module','source_contract'):return deepcopy(x)
 if isinstance(x,dict):
  if key in ('canonical_isometry','canonical_transform'):return canonical(x)
  z={k:geometry(v,k)for k,v in x.items()}
  for k in ('axis','front_axis'):
   if z.get(k)in ('x','y'):z[k]='y'if z[k]=='x'else'x'
  if z.get('orientation')in ('horizontal','vertical'):z['orientation']='vertical'if z['orientation']=='horizontal'else'horizontal'
  return z
 if isinstance(x,list):
  if key in RECT_KEYS and len(x)==4 and not isinstance(x[0],(list,dict)):return rect(x)
  if key in POINT_KEYS|VECTOR_KEYS and len(x)==2 and not isinstance(x[0],(list,dict)):return point(x)
  if key in RECT_LIST_KEYS and x and isinstance(x[0],list):return[rect(r)for r in x]
  if key in PATH_KEYS and x and isinstance(x[0],list):return[point(p)for p in x]
  return[geometry(v)for v in x]
 return deepcopy(x)

def to_world(local,core):
 matrix(core['world_from_local']['matrix'])
 if core['world_from_local']!={'matrix':[[0,1],[1,0]],'translation':['0','0']}:raise ValueError('UNSUPPORTED_WORLD_FRAME125')
 m=deepcopy(local);m['inputs']=[S(F(str(v))) for v in core['physical_core_model']['inputs'][:2]]+[2];m['schema']='GENERAL125_WORLD_FRAME_STUDY'
 for key in ('walls','wall_hosts','source_wall_hosts'):m[key]={k:rect(v)for k,v in local[key].items()}
 m['common_spaces']={k:([rect(q)for q in v]if isinstance(v[0],list)else rect(v))for k,v in local['common_spaces'].items()}
 m['common_routes']={k:[point(q)for q in v]for k,v in local['common_routes'].items()}
 m['proposal_network_paths']={k:[point(q)for q in v]for k,v in local['proposal_network_paths'].items()}
 m['openings']=geometry(local['openings']);m['concept_windows']=geometry(local['concept_windows'])
 for w in m['concept_windows']:
  if 'destination'in w:w['destination']['edge']={'bottom':'left','top':'right','left':'bottom','right':'top'}.get(w['destination']['edge'],w['destination']['edge'])
 m['operations']=geometry(local['operations']);m['module_ports']=geometry(local['module_ports'])
 m['module_aprons']={k:[rect(q)for q in v]for k,v in local['module_aprons'].items()}
 m['module_placements']=deepcopy(local['module_placements'])
 for rec in m['module_placements']:rec['transform']=placement(rec['transform'])
 m['logical_regions']=geometry(local['logical_regions'])
 if 'private_domains'in local:
  m['private_domains']=deepcopy(local['private_domains'])
  for dst,src in zip(m['private_domains'],local['private_domains']):
   dst['parts']=[rect(q)for q in src['parts']]
   dst['public_interface']['rect']=rect(src['public_interface']['rect'])
   dst['public_interface']['open_side']={'top':'right','bottom':'left','left':'bottom','right':'top'}[src['public_interface']['open_side']]
   dst['paths']={k:[point(q)for q in path]for k,path in src['paths'].items()}
 # ordered_macro records source-local proposal geometry, not world geometry.
 if local.get('ordered_macro'):m['ordered_macro_coordinate_frame']='IMMUTABLE_LOCAL_CONSTRUCTION_PROPOSAL'
 for u,src in zip(m['units'],local['units']):
  u['ownership']=[rect(r)for r in src['ownership']]
  u['rooms']={k:[rect(r)for r in rs]for k,rs in src['rooms'].items()}
  for key in ('fixtures','activities'):u[key]={k:rect(r)for k,r in src[key].items()}
  for key in ('routes','scenario_routes'):u[key]={k:[point(q)for q in p]for k,p in src[key].items()}
  u['route_targets']={k:point(q)for k,q in src['route_targets'].items()};u['entry_point']=point(src['entry_point'])
  for md in u['fixture_metadata'].values():md['rotation_deg']=(90-md.get('rotation_deg',0))%180
  u['dining_module_placement']['transform']=placement(src['dining_module_placement']['transform'])
  u['public_program']=geometry(src['public_program'])
  u['public_floor_classification']['route_geometry_hash']=digest({**u['routes'],**{'scenario:'+k:v for k,v in u['scenario_routes'].items()}})
 m['wall_finish_profile']=geometry(local['wall_finish_profile']);m['threshold_ownership']=geometry(local['threshold_ownership'])
 m['openedge_assumptions']={'rights':'UNVERIFIED','assessment':'LIGHT_VENTILATION_EXCLUDED','geometric_frame_transform':'swapXY; optional opening physical hosts retained'}
 from wall_union118 import bind_physical_wall_union
 from spatial_roles118 import attach
 m=attach(bind_physical_wall_union(m))
 m['quality_unverified']=[s for s in m['quality_unverified']if 'ventilation'not in s and 'daylight'not in s]
 m['frame_binding125']={'schema':'ACTUAL_LOCAL_TO_WORLD_D4_V1','local_model_hash':digest(local),'core_contract_hash':digest(core),'world_from_local':deepcopy(core['world_from_local']),'not_a_receipt_of_whole_acceptance':True,'rotation_deg_scope':'Axis footprint only, not a world-facing heading; full source module placement D4 retains orientation binding.','operation_angle_scope':'Kitchen angle ranges are source canonical study parameters, not world polar angles; canonical_transform binds their physical geometry.'}
 return m
