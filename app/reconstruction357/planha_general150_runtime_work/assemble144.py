"""Actual geometry assembly from variable solved rectangles, not picture lookup.
Operations not yet witnessed remain explicit pending; geometry is not admission.
"""
from copy import deepcopy
import json
from pathlib import Path
from fractions import Fraction as F
from geometry114 import Q,cells,route,hit
from contract114 import S,BODY,WALL,digest
CATALOG={'bed':[2,1.6],'closet':[.6,2.05],'WC_iranian':[.7,.7],'shower_floor':[.9,.9],'basin':[.45,.45],'fridge':[.7,.7],'sink':[.6,.7],'prep':[.6,.7],'cooker':[.6,.7],'sofa':[2.2,.9],'armchair':[.8,.8],'dining_table':[.8,1.2],'dining_chair':[.5,.5]}

def assemble(W,L,core,p,unit_proposals=None):
 from nonseating144 import require,route_obstacles
 require(p)
 base_proposal=p
 if unit_proposals is not None:
  if set(unit_proposals)!={"A","B"}:raise ValueError("UNIT_PROPOSAL_KEYS")
  for up in unit_proposals.values():
   if (up["bedrooms"],up.get("sleep_roles"))!=(p["bedrooms"],p.get("sleep_roles")):raise ValueError("MIXED_PROGRAM_PAIR_NOT_SUPPORTED")
 R={k:Q(v)for k,v in p['rectangles'].items()};T=WALL;quarter=F('.25');m={'schema':'GENERAL117_HIERARCHICAL_STUDY','contract_version':'114-provisional-v1','inputs':[S(W),S(L),2],
 'scope_declaration':{'kind':'CONCEPT_DRAFT_ONLY','technical_approval':False,'legal_approval':False,'daylight_ventilation_scope':'EXCLUDED_FROM_MVP_NOT_EVALUATED','vertical_core_certified':False,'opening_rights':'UNVERIFIED','execution_ready':False},
 'ordered_macro':p.get('ordered_macro'),
 'status':'QA_ONLY_PENDING_INDEPENDENT_GATE','accepted':False,'release_allowed':False,'profile':{'body_m':'.7'},'program':{'bedrooms_per_unit':p['bedrooms'],'sleep_roles':p.get('sleep_roles',['double']*p['bedrooms']),'capacity_profile':p.get('capacity_profile','LEGACY_SOURCE_PROGRAM'),'design_occupants_per_unit':sum(2 for _ in p.get('sleep_roles',['double']*p['bedrooms'])),'capacity_basis':'Sum actual double(2) or twin(two single instances of1) study program; not inference from room area or names','units':2,'provisional':True},
 'walls':{},'wall_hosts':{},'source_wall_hosts':{},'common_spaces':{k:core[k]for k in('stair','lift','lobby')},'openings':[],'concept_windows':[],'units':[],'room_metadata':{},'common_routes':{},
 'fixture_catalog_hash':digest(json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text())),'fixture_catalog':CATALOG,'fixture_catalog_digest':digest(CATALOG),'openedge_assumptions':{'open_edges':['y=0','y=L'],'closed_edges':['x=0','x=W'],'rights':'UNVERIFIED'},'route_failures':[],
 'proposal_network_paths':p.get('network_paths',{}),'network_scope':p.get('network_scope'),'logical_regions':{u+'.public_access':{'unit':u,'source_roles':['living','entry_circulation']}for u in('A','B')},'operations':{},'pending':['DOOR_OPERATION_WITNESSES','CLOSET_OPERATION_WITNESSES','KITCHEN_OPERATION_WITNESSES','PRIVACY_WITNESSES','CORE_STAIR_LIFT_HARDWARE_AND_EXTERNAL_ENTRY_NOT_CERTIFIED']}
 from approach_contract123 import bedroom_role
 for uid in ('A','B'):m['logical_regions'][uid+'.bedroom_public_access']=bedroom_role(uid)
 def seq(r):return[S(x)for x in r]
 def wall(key,r,openings=()):
  r=Q(r);m['wall_hosts'][key]=seq(r);m['source_wall_hosts'][key]=seq(r);pieces=cells([r],[z['rect']for z in openings])if openings else[seq(r)]
  for i,q in enumerate(pieces):m['walls'][key if len(pieces)==1 else key+'.solid'+str(i)]=[S(F(str(x)))for x in q]
  for o in openings:m['openings'].append(dict(o,host_wall_id=key))
 def op(key,r,connects):return {'id':key,'rect':seq(r),'connects':connects,'operation_kind':'sliding_study','operation_witness_status':'NOT_EVALUATED'}
 wall('left',[0,0,quarter,L]);wall('right',[W-quarter,0,W,L]);wall('front',[quarter,0,W-quarter,quarter]);wall('back',[quarter,L-quarter,W-quarter,L])
 y=F(core['band'][1]);yt=F(core['band'][3]);entry_cx=F(core['entry_centers']['A'][0]);door=(entry_cx-F('.65'),entry_cx+F('.65'))
 coreleft,coreright=map(F,core.get('core_extent_x',[S(quarter),S(W-quarter)]))
 for uid,lo,hi in [('A',y-T,y),('B',yt,yt+T)]:wall(uid+'.unit_boundary',[coreleft,lo,coreright,hi],[op(uid+'.entry',[door[0],lo,door[1],hi],['lobby',uid+'.entry_circulation'])])
 if 'outside_band_unit_separator_y'in core:
  slo,shi=map(F,core['outside_band_unit_separator_y'])
  for side,a,b in [('left',quarter,coreleft),('right',coreright,W-quarter)]:
   if a<b:wall('unit_shared_wing_'+side,[a,slo,b,shi])
  wall('core.lobby.outer_right',[coreright-T,y,coreright,yt])
 for name,door_side,dw in [('stair','right',F('.9')),('lift','left',F('1.1'))]:
  a,b,c,d=Q(core[name]);cy=(b+d)/2
  if core.get('physical_core_model'):
   source=next(o for o in core['physical_core_model']['openings']if o['id']==name+'.entry')
   sx,sy,sX,sY=Q(source['rect']);cy=(sx+sX)/2;dw=sX-sx
   # Actual world horizontal core aperture becomes local vertical aperture.
   # No old fixed1.1m lift opening is substituted for source contract geometry.
  for side,r in [('left',[a-T,b-T,a,d+T]),('right',[c,b-T,c+T,d+T]),('bottom',[a,b-T,c,b]),('top',[a,d,c,d+T])]:
   oo=[]
   if side==door_side:oo=[dict(op(name+'.entry',[r[0],cy-dw/2,r[2],cy+dw/2],[name,'lobby']),kind='core_access_interface',leaf_modeled=False,source_scope_reference='doors102.py: explicit stair/lift operations unmodeled; Concept core-route interface only',operation_witness_status='NOT_MODELED_HARDWARE_OUTSIDE_CONCEPT_INTERFACE')]
   wall('core.'+name+'.'+side,r,oo)
 for uid in ('A','B'):
  p=unit_proposals[uid] if unit_proposals is not None else base_proposal
  R={k:Q(v) for k,v in p['rectangles'].items()}
  def tr(r):
   a,b,c,d=Q(r);return[a,b,c,d]if uid=='A'else[a,L-d,c,L-b]
  def pt(q):a,b=map(lambda v:F(str(v)),q);return[S(a),S(b if uid=='A'else L-b)]
  u={'id':uid,'ownership':core.get('unit_ownership',{}).get(uid,[core['units'][uid]]),'rooms':{},'fixtures':{},'fixture_metadata':{},'activities':{},'routes':{},'scenario_routes':{},'route_targets':{}}
  def room(name,r,private=False):u['rooms'][name]=[seq(tr(r))];m['room_metadata'][uid+'.'+name]={'role':'bedroom'if name.startswith('bed')else name,'private':private,'source':'variable_rectangle_with_fixed_fixture_program'}
  def fixture(name,kind,r,rotation=0,walkable=False):u['fixtures'][name]=seq(tr(r));u['fixture_metadata'][name]={'kind':({'sofa':name,'armchair':('armchair1'if name in('armchair1','armchair3')else'armchair2'),'dining_chair':{'dining_chair_left':'dining_chair_front','dining_chair_right':'dining_chair_back'}.get(name,name)}.get(kind,kind)),'source_size_m':CATALOG[kind],'rotation_deg':rotation,'walkable':walkable}
  def activity(name,r):u['activities'][name]=seq(tr(r))
  def wwall(name,r,opening=None):
   z=[]
   if opening:
    rr,connects=opening;z=[op(uid+'.'+name, tr(rr),[uid+'.'+x for x in connects])]
   wall(uid+'.'+name, tr(r),z)
  for i in range(p['bedrooms']):
   name='bed'+str(i+1);a,b,c,d=R[name];rw=c-a;room(name,R[name],True)
   if p.get('sleep_roles',['double']*p['bedrooms'])[i]=='twin':
    from twin_module118 import build as build_module
   else:
    from bedroom_module116 import build as build_module
   from place_module116 import install
   side=p.get('bed_door_sides',{}).get(name,'left')
   if (p.get('ordered_macro')or{}).get('kind')in('TURN_T133','SIDECAR_T136'):
    from source_rotation133 import build as source133
    from place_module133 import install
    local=source133(p['sleep_roles'][i])
   else:local=build_module(S(c-a),S(d-b))
   install(local,m,u,uid,name,R[name],L,side)
   # Window spans a real continuous room-front interval, not old rectangular bounds.
   frontedge=quarter if uid=='A'else L-quarter
   intervals=sorted((Q(q)[0],Q(q)[2])for q in u['rooms'][name]if (Q(q)[1]if uid=='A'else Q(q)[3])==frontedge)
   merged=[]
   for xx,zz in intervals:
    if merged and xx<=merged[-1][1]:merged[-1]=(merged[-1][0],max(zz,merged[-1][1]))
    else:merged.append((xx,zz))
   if merged:
    xx,zz=next(((a,b)for a,b in merged if b-a>=F('.9')),merged[0]);available=zz-xx-F('.2')
    if available>=F('.7'):
     ww=min(F(2),available);x0=(xx+zz-ww)/2;x1=x0+ww;wr=[x0,0,x1,quarter]if uid=='A'else[x0,L-quarter,x1,L]
     m['concept_windows'].append({'id':uid+'.'+name+'.window','unit':uid,'room':uid+'.'+name,'plan_rect':seq(wr),'host_wall_id':'front'if uid=='A'else'back','destination':{'edge':'bottom'if uid=='A'else'top'},'sill_m':'1.1','head_m':'2.1','floor_portal':False,'assumed_open_edge':True,'available_width_m':S(available),'geometry_only_optional_opening':True})
  a,b,c,d=R['bath']
  from bathroom_module117 import build as build_bath
  from place_bathroom117 import install as install_bath
  install_bath(build_bath(S(c-a),S(d-b)),m,u,uid,R['bath'],L)
  a,b,c,d=R['kitchen']
  from kitchen_module117 import build as build_kitchen
  from place_kitchen117 import install as install_kitchen
  install_kitchen(build_kitchen(S(c-a),S(d-b)),m,u,uid,R['kitchen'],L)
  a,b,c,d=R['dining'];room('dining',R['dining'])
  six_person=p.get('capacity_profile')=='SIX_PERSON_INTERNAL_PROGRAM121'
  if six_person:
   from dining_module121 import build as build_dining
  else:
   from dining_module118 import build as build_dining
  dm=build_dining(S(c-a),S(d-b))
  def dr(q):x,y,xx,yy=Q(q);return[a+x,b+y,a+xx,b+yy]
  dmap={key:('dining_table'if key=='table'else'dining_'+key)for key in dm['fixtures']}
  for key,q in dm['fixtures'].items():
   name=dmap[key];u['fixtures'][name]=seq(tr(dr(q)));u['fixture_metadata'][name]={'kind':('dining_table6'if six_person else'dining_table')if key=='table'else'dining_chair_front'if key in(('chair_front_left','chair_front_right','chair_left')if six_person else('chair_west','chair_front'))else'dining_chair_back','rotation_deg':0,'source_size_m':([2.2,1.0]if six_person else[.8,1.2])if key=='table'else[.5,.5]}
  for seat in dm['seating']['instances']:
   side=seat['id']if six_person else seat['id'][5:];ar=seat['rise_transfer']['standing_body'];activity('dining_'+side,dr(ar))
  u['activities']['dining_left']=u['activities']['dining_left'if six_person else'dining_west'];u['activities']['dining_right']=u['activities']['dining_right'if six_person else'dining_east']
  u['dining_module_placement']={'module':dm,'module_hash':digest(dm),'transform':{'matrix':[[1,0],[0,1 if uid=='A'else-1]],'translation':[S(a),S(b if uid=='A'else L-b)]},'id_map':dmap,'capacity_status':'NOT_EVALUATED_OCCUPIED_RISE_PENDING'}
  from seating_source142 import validate_proposal
  seats142=validate_proposal(p)
  for name,rec in seats142.items():
   u['fixtures'][name]=seq(tr(rec['fixture']))
   u['fixture_metadata'][name]={'kind':rec['source_key'],'source_size_m':CATALOG['sofa'if name.startswith('sofa')else'armchair'],'rotation_deg':rec['rotation'],'walkable':False}
   # Keep the existing wider activity reservation; exact source target is its center.
   u['activities'][name+'_front']=seq(tr(rec['reserved_activity']))
  from private_hall_producer121 import install as install_private_hall
  if (p.get('ordered_macro') or {}).get('kind')=='L3_EXPERIMENTAL131':
   from private_l3_hall131 import install as install_private_hall
  if (p.get('ordered_macro')or{}).get('kind')=='L3_MIXED132':
   from private_mixed_hall132 import install as install_private_hall
  if (p.get('ordered_macro')or{}).get('kind')in('STAGGER132','STAGGER_ACCESS132'):
   from private_stagger_hall132 import install as install_private_hall
  if (p.get('ordered_macro')or{}).get('kind')=='TURN_T133':
   from private_t_hall133 import install as install_private_hall
  if (p.get('ordered_macro')or{}).get('kind')=='SIDECAR_T136':
   from private_sidecar_hall136 import install as install_private_hall
  install_private_hall(m,u,core,p,L)
  m['units'].append(u)
 from entry117 import install as install_entry
 install_entry(m)
 # Route against complete actual walls and fixtures, not reserved rectangles alone.
 allwalls=list(m['walls'].values())+[op['open_panel']for op in m.get('operations',{}).get('doors',[])];allfx={v['id']+'.'+k:r for v in m['units']for k,r in v['fixtures'].items()if not v['fixture_metadata'][k].get('walkable')}
 for u in m['units']:
  uid=u['id'];box=Q(u['ownership'][0]);entry=[entry_cx,box[3]-F('.4')]if uid=='A'else[entry_cx,box[1]+F('.4')]
  targets={k:[(Q(r)[0]+Q(r)[2])/2,(Q(r)[1]+Q(r)[3])/2]for k,r in u['activities'].items()}
  for name,target in targets.items():
   excluded=(uid+'.WC_iranian')if name=='WC_use'else(uid+'.shower_floor')if name=='shower_use'else None
   obs=allwalls+[q for key,q in allfx.items()if key!=excluded]+([]if name.startswith('bed')else u['rooms'].get('private_circulation',[]))+route_obstacles(u,name);path,reason=route(entry,target,box,obs)
   u['route_targets'][name]=[S(v)for v in target]
   if path:u['routes'][name]=path
   else:m['route_failures'].append({'unit':uid,'route':name,'reason':reason})
  if 'kitchen_work'in targets and'dining_right'in targets:
   path,reason=route(targets['kitchen_work'],targets['dining_right'],box,allwalls+list(allfx.values())+route_obstacles(u,'kitchen_to_dining_floor'))
   if path:u['scenario_routes']['kitchen_to_dining_floor']=path
   else:m['route_failures'].append({'unit':uid,'route':'kitchen_to_dining_floor','reason':reason})
  for source in ('stair','lift'):
   a,b,c,d=Q(core[source]);cy=(b+d)/2;start=[c-F('.4'),cy]if source=='stair'else[a+F('.4'),cy]
   m['common_routes'][source+'_'+uid]=[[S(v)for v in q]for q in[start,[entry_cx,cy],entry]]
 m['quality_unverified']=['Unallocated residual labelled living is not a verified spatial program.','Living connectivity, fragmentation, long circulation and functional capacity require separate assessment.']
 m['source_geometry_contract']={'catalog_digest':digest(CATALOG),'body_m':'.7','room_dimensions_variable':True,'immutable_furniture_dimensions':True,'doors_constructed_from_actual_room_edges':True,'not_a_proof_of_door_operation':True}
 from operations115 import construct_bedroom_motion_studies
 from public_witness144 import install as install_public
 from wall_union118 import bind_physical_wall_union
 from spatial_roles118 import attach as attach_spatial_roles
 from face_threshold118 import attach as attach_faces_thresholds
 from final_public_floor120 import rebuild as rebuild_public_floor
 if m.get('module_placements'):
  for unit in m['units']:
   if 'kitchen_work'in unit['routes']:unit['routes']['kitchen']=unit['routes']['kitchen_work']
  return attach_spatial_roles(attach_faces_thresholds(bind_physical_wall_union(rebuild_public_floor(install_public(m)))))
 from public_witness144 import install as install_public
 from wall_union118 import bind_physical_wall_union
 from spatial_roles118 import attach as attach_spatial_roles
 from face_threshold118 import attach as attach_faces_thresholds
 from final_public_floor120 import rebuild as rebuild_public_floor
 return attach_spatial_roles(attach_faces_thresholds(bind_physical_wall_union(rebuild_public_floor(install_public(construct_bedroom_motion_studies(m))))))
