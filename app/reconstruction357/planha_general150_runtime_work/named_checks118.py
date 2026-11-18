"""Criterion-specific fresh independent adapters. Missing rules remain missing."""
from checker114 import rect,F,covered,encloses,digest

def response(errors,pending,witness,scope):
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','witness':dict(witness,errors=errors,pending=pending),'scope':scope}

def _operations(m,component):
 from operation_check114 import check_operations
 owners={u['id']:[rect(q)for q in u['ownership']]for u in m['units']};owners['COMMON']=[rect(q)for q in m['common_spaces']['lobby']]
 walls={k:rect(q)for k,q in m['walls'].items()};fixtures=[(u['id'],k,rect(q))for u in m['units']for k,q in u['fixtures'].items()]
 e,p=check_operations(m,owners,walls,fixtures,components=(component,))
 return response(e,p,{'model_hash':digest(m),'operation_component':component,'actual_operation_ids':[o.get('opening_id',o.get('fixture_id',o.get('unit')))for o in m['operations'].get(component,[])]},'Actual continuous source-sized body/panel/hand and obstacle checks, with explicit hardware assumptions; not installation approval')
def door_operation(m):return _operations(m,'doors')
def closet_operation(m):return _operations(m,'closets')
def kitchen_essential_operation(m):return _operations(m,'kitchen')
def bath_service_operation(m):
 from checker114 import check_bathroom_module,check_module_placements
 rows=[];e=[];p=[]
 for pl in m.get('module_placements',[]):
  if pl['module'].get('schema')!='BATHROOM_MODULE117':continue
  r=check_bathroom_module(pl['module']);rows.append(r);e.extend(r['errors']);p.extend(r['pending'])
 if len(rows)!=len(m['units']):p.append('EVERY_UNIT_BATH_SOURCE_MODULE_MISSING')
 binding=check_module_placements(m);e.extend(binding['errors']);p.extend(binding['pending'])
 return response(e,p,{'modules':rows,'placement':binding},'Source-backed wet equipment/operations and exact placed-neighbor binding, not complete H07 private-node deletion test')
def q11_functional_boundary(m):
 from q11_boundary118 import examine
 r=examine(m);return response(r['errors'],r['pending'],r['evidence'],'Source-sized usable closet boundary replacing sight-only screen; fresh operations/privacy/placement and exact before-after comparison; no general residual-space quality claim')
def window_opportunities(m):
 # Historical API retained solely to prevent accidental reactivation.
 return {'status':'NOT_EVALUATED','witness':{'scope_status':'EXCLUDED_BY_OWNER_SCOPE','executed':False},'scope':'Lighting and ventilation are not evaluated in MVP121. This is not PASS and not remaining work.'}

ADAPTERS={fn.__name__:fn for fn in(door_operation,closet_operation,kitchen_essential_operation,bath_service_operation,q11_functional_boundary,window_opportunities)}

def containment_all_entities(m):
 frame=(F(0),F(0),F(m['inputs'][0]),F(m['inputs'][1]));errors=[];rows=[]
 for k,q in m['walls'].items():rows.append(('wall:'+k,rect(q),[frame]))
 for u in m['units']:
  own=[rect(q)for q in u['ownership']]
  rows +=[(u['id']+'.ownership',q,[frame])for q in own]
  rows +=[(u['id']+'.room.'+k,rect(q),own)for k,rs in u['rooms'].items()for q in rs]
  rows +=[(u['id']+'.'+group+'.'+k,rect(q),own)for group in('fixtures','activities')for k,q in u[group].items()]
 for group,key in [('openings','rect'),('concept_windows','plan_rect')]:rows +=[(group+':'+o['id'],rect(o[key]),[frame])for o in m[group]]
 for k,v in m['common_spaces'].items():rows +=[('common:'+k,rect(q),[frame])for q in(v if isinstance(v[0],list)else[v])]
 for name,q,owners in rows:
  if not covered(q,owners):errors.append({'entity':name,'code':'OUTSIDE_ACTUAL_FRAME_OR_OWNER'})
 return response(errors,[],{'checked_entities':len(rows),'frame':list(map(str,frame))},'Every represented wall, ownership, room floor, fixture, activity, aperture, window and core rectangle against actual frame/owner; semantic roles separately reviewed')
def unit_independence(m):
 from checker114 import intersects
 errors=[];rows=[]
 for i,a in enumerate(m['units']):
  for b in m['units'][i+1:]:
   overlaps=[(ra,rb)for ra in a['ownership']for rb in b['ownership']if intersects(rect(ra),rect(rb))]
   if overlaps:errors.append({'units':[a['id'],b['id']],'overlaps':overlaps})
   rows.append([a['id'],b['id']])
 return response(errors,[],{'pairs':rows},'Disjoint actual unit ownership; independent access and private paths are separate mandatory criteria')
def body_route_sweeps(m):
 from checker114 import sweeps,intersects
 errors=[];rows=[];walls=[rect(v)for v in m['walls'].values()];panels=[rect(o['open_panel'])for o in m['operations']['doors']]
 for u in m['units']:
  own=[rect(q)for q in u['ownership']]
  if not set(u['activities'])<=set(u['routes'])or not set(u['route_targets'])<=set(u['routes']):errors.append({'unit':u['id'],'code':'ACTUAL_ACTIVITY_ROUTE_INVENTORY'})
  for name,path in u['routes'].items():
   if not path or (name in u['route_targets']and tuple(map(F,path[-1]))!=tuple(map(F,u['route_targets'][name]))):errors.append({'route':name,'code':'TARGET_BINDING'});continue
   obstacles=walls+panels
   for v in m['units']:
    for fid,q in v['fixtures'].items():
     kind=v['fixture_metadata'][fid]['kind'];exception=v['id']==u['id']and((name=='WC_use'and kind=='WC_iranian')or(name in('shower','shower_use')and kind=='shower_floor'))
     if not exception:obstacles.append(rect(q))
   for sweep in sweeps(path):
    if not covered(sweep,own):errors.append({'route':name,'code':'BODY_OUTSIDE_OWNER'})
    if any(intersects(sweep,q)for q in obstacles):errors.append({'route':name,'code':'BODY_WALL_PANEL_FIXTURE_COLLISION'})
   rows.append({'unit':u['id'],'route':name,'points':len(path),'body_m':'.7'})
 return response(errors,[],{'routes':rows},'All declared activity route swept bodies against actual owners/walls/all open panels/fixtures; required named guest/chair/service inventory separately remains mandatory')
ADAPTERS.update({fn.__name__:fn for fn in(containment_all_entities,unit_independence,body_route_sweeps)})

# Independent source auditors owned by other reviewers, not producer receipts.
from core_wall_audit118 import ADAPTERS as CORE_ADAPTERS
from access_accounting118 import bath_nonprivate_access
ADAPTERS.update(CORE_ADAPTERS)
ADAPTERS['bath_nonprivate_access']=bath_nonprivate_access

def public_named_scenarios(m):
 from public_program_audit118 import examine
 r=examine(m)
 return response(r['errors'],r['pending'],r['evidence'],'Combined named public guest/chair/capacity/service scenario audit. Missing any applicable witness is retained; no blanket capacity PASS or reduction of occupant count.')
for key in('guest_living_route','guest_dining_route','serving_route','chair_capacity_movement','program_functional_roles'):
 ADAPTERS[key]=public_named_scenarios

def privacy_scenarios(m):
 from checker114 import check_whole_privacy117,check_module_placements
 r=check_whole_privacy117(m);b=check_module_placements(m)
 errors=list(r['errors'])+b['errors'];pending=list(r['pending'])+b['pending']
 expected_rooms={(u['id'],k)for u in m['units']for k in u['rooms']if k.startswith('bed')or k=='bath'}
 observed={(x['unit'],x['room'])for x in r['evidence']['targets']}
 if observed!=expected_rooms:errors.append({'code':'PRIVACY_ALL_PRIVATE_ROOM_INVENTORY'})
 return response(errors,pending,{'privacy':r,'placement':b,'actual_private_rooms':[list(x)for x in sorted(expected_rooms)],'observer_implication':'Under actual closed opaque floor-plan boundaries, every public/entry/guest sightline entering a private room crosses one of the fully enumerated apertures; the certificates span each entire aperture and entire target, not a sample observer point.','state_coverage':'Static actual wall/cabinet skins establish the certificates independently of a shut moving leaf. Fully-open aperture is the conservative entry condition.','conditions':['Planar opaque-height hypothesis, not visual privacy through facade windows or above partitions','Wet source uses necessary inner face; conditional_closed_boundary is non-strict tangency, never a closed door','No cultural/ergonomic approval or two-person dynamic occupancy proof']},'All actual closed bedroom boundaries with every bed instance and changing target, and source-required wet targets; public/threshold/guest aperture visibility under stated opacity and boundary assumptions')
ADAPTERS['privacy_scenarios']=privacy_scenarios

def chair_capacity_movement(m):
 from dining_motion_audit118 import examine
 from checker114 import intersects
 errors=[];pending=[];rows=[]
 for u in m['units']:
  rec=u.get('dining_module_placement')
  if not rec:pending.append('DINING_SOURCE_MODULE_PLACEMENT_MISSING:'+u['id']);continue
  mod=rec['module'];mhash=digest(mod);mapping=rec['id_map'];mat=rec['transform']['matrix'];delta=list(map(F,rec['transform']['translation']))
  if rec.get('module_hash')!=mhash:errors.append({'code':'DINING_MODULE_HASH'})
  if mat[0][1]!=0 or mat[1][0]!=0 or mat[0][0]not in(-1,1)or mat[1][1]not in(-1,1):errors.append({'code':'DINING_RIGID_TRANSFORM'});continue
  def tr(r):
   r=rect(r);xs=[F(mat[0][0])*r[i]+delta[0]for i in(0,2)];ys=[F(mat[1][1])*r[i]+delta[1]for i in(1,3)];return(min(xs),min(ys),max(xs),max(ys))
  for k,r in mod['fixtures'].items():
   if k not in mapping or mapping[k]not in u['fixtures']or rect(u['fixtures'][mapping[k]])!=tr(r):errors.append({'code':'DINING_ACTUAL_FIXTURE_SOURCE_BINDING','fixture':k})
  local=examine(mod);errors.extend(local['errors']);pending.extend(local['pending'])
  obstacles=[rect(q)for q in m['walls'].values()]+[rect(o[k])for o in m['operations']['doors']for k in('closed_panel','open_panel')]
  obstacles +=[rect(q)for v in m['units']for k,q in v['fixtures'].items()if v['id']!=u['id']or k not in set(mapping.values())]
  owner=[rect(q)for q in u['ownership']]
  for witness in local['evidence'].get('continuous_witnesses',[]):
   for key in('actor_sweep','chair_sweep'):
    sweep=tr(witness[key])
    if not covered(sweep,owner):errors.append({'code':'DINING_PLACED_MOTION_OUTSIDE_OWNER','unit':u['id'],'seat':witness['seat']})
    if any(intersects(sweep,q)for q in obstacles):errors.append({'code':'DINING_PLACED_MOTION_NEIGHBOR_COLLISION','unit':u['id'],'seat':witness['seat']})
  actual_ops={o['fixture_id']:o for o in m['operations'].get('dining_chairs',[])if o.get('unit')==u['id']}
  for seat in mod['seating']['instances']:
   fid=mapping[seat['fixture_id']];op=actual_ops.get(fid)
   if not op:pending.append('DINING_WORLD_MOTION_WITNESS_MISSING:'+u['id']+'.'+fid);continue
   for actual,source in [('closed_rect','closed_rect'),('open_rect','pulled_rect'),('occupied_body','occupied_body')]:
    if rect(op[actual])!=tr(seat[source]):errors.append({'code':'DINING_WORLD_OPERATION_SOURCE_BINDING','fixture':fid,'field':actual})
   if op.get('source_module_hash')!=mhash:errors.append({'code':'DINING_WORLD_OPERATION_MODULE_HASH','fixture':fid})
  rows.append({'unit':u['id'],'module_hash':mhash,'local_motion':local,'global_neighbors_tested':len(obstacles)})
 return response(errors,sorted(set(pending)),{'placed_dining':rows},'Actual four-seat source fixtures and exact occupied pull/exit sweeps with neighbors; own-seat vertical support/rise remains NOT_EVALUATED, never silently collision-exempt')
ADAPTERS['chair_capacity_movement']=chair_capacity_movement
from claim_audit118 import claim_boundary
ADAPTERS['claim_boundary']=claim_boundary


def adapters_for_workflow(workflow_context=None):
 callbacks=dict(ADAPTERS)
 def q11_for_current_workflow(m):
  from q11_boundary118 import examine
  r=examine(m,workflow_context=workflow_context)
  return response(r['errors'],r['pending'],r['evidence'],'Actual functional cabinet boundary with source-bound placement/privacy/operations. Current-state impact for trusted dimensions-only construction, real predecessor comparison for a revision. No producer flags trusted.')
 callbacks['q11_functional_boundary']=q11_for_current_workflow
 callbacks['long_corridor_necessity']=lambda m:circulation_evaluate(m,workflow_context=workflow_context)


 if workflow_context and workflow_context.get('construction_trace',{}).get('schema')in('CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1','CONSTRUCTION_TRACE125_WORLD_V1','CONSTRUCTION_TRACE126_PAIR_V1','CONSTRUCTION_TRACE127_PAIR_V1'):
  callbacks['circulation_functional_integrity']=lambda m:circulation_functional_integrity120(m,frame_core=workflow_context.get('frame_core125'),frame_local=workflow_context.get('frame_local129'))
 return callbacks
from project_input_audit118 import no_hidden_project_inputs
ADAPTERS['no_hidden_project_inputs']=no_hidden_project_inputs

def chair_capacity_movement(m):
 from dining_motion_audit118 import examine_whole
 r=examine_whole(m)
 return response(r['errors'],r['pending'],r['evidence'],'Fresh source-bound planar sequential seat pull and side-exit with three occupied neighbors; own-seat contact only for this task, never public walking. Height/support forces/real ergonomics NOT_VERIFIED.')
ADAPTERS['chair_capacity_movement']=chair_capacity_movement

def fixture_inventory_use(m):
 from program_capacity_audit118 import examine
 from checker114 import check_module_placements
 cap=examine(m);place=check_module_placements(m)
 errors=list(cap['errors'])+place['errors'];pending=list(cap['pending'])+place['pending'];sub=[]
 for fn in(door_operation,closet_operation,kitchen_essential_operation,bath_service_operation,chair_capacity_movement):
  r=fn(m);sub.append(r);errors.extend(r['witness'].get('errors',[]));pending.extend(r['witness'].get('pending',[]))
 return response(errors,sorted(set(pending)),{'capacity':cap,'source_placement':place,'fresh_functional_components':sub},'Actual source-sized sleeping/living/dining instances and required module/source operational use; no inferred population from area or sofa length, no external/vertical installation approval')
ADAPTERS['fixture_inventory_use']=fixture_inventory_use

def program_functional_roles(m):
 from program_capacity_audit118 import examine
 from public_program_audit118 import examine as public
 cap=examine(m);pub=public(m);wet=bath_service_operation(m);access=bath_nonprivate_access(m)
 errors=list(cap['errors'])+pub['errors']+wet['witness']['errors']+access['witness']['errors'];pending=list(cap['pending'])+pub['pending']+wet['witness']['pending']+access['witness']['pending']
 return response(errors,sorted(set(pending)),{'actual_capacity':cap,'public_scenarios':pub,'wet_service':wet,'nonprivate_wet_access':access},'Named program roles from real bed/seat instances, occupied planar use, independent guest/service paths and actual nonprivate wet function; global spatial quality and residual usefulness separate')
ADAPTERS['program_functional_roles']=program_functional_roles

def partition_ledger(m):
 from partition_audit118 import partition_ledger as audit
 r=audit(m);errors=list(r['witness'].get('errors',[]));pending=list(r['witness'].get('pending',[]));account=m.get('spatial_accounting')
 if not account:return r
 physical={'inputs':m['inputs'],'walls':m['walls'],'common_spaces':m['common_spaces'],'units':[{k:u[k]for k in('id','ownership','rooms','fixtures','activities','routes','scenario_routes')}for u in m['units']]}
 if digest(physical)!=account.get('physical_geometry_hash'):errors.append('LEDGER_PHYSICAL_GEOMETRY_HASH')
 from threshold_check118 import examine as check_threshold
 threshold=check_threshold(m) if m.get('threshold_ownership') else {'errors':[], 'expected':[]}
 errors+=threshold['errors']
 raw=[('actual_wall_union',list(m['walls'].values()))]+threshold['expected']+[('unit_'+u['id']+'_floor',u['ownership'])for u in m['units']]
 raw +=[('common_'+k,v if isinstance(v[0],list)else[v])for k,v in m['common_spaces'].items()]
 expected={k:[rect(q)for q in qs]for k,qs in raw};actual={g['role']:[rect(q)for q in g['regions']]for g in account['plot_partition']};W,L=map(F,m['inputs'][:2])
 if set(actual)!=set(expected)|{'UNASSIGNED_PLOT_FLOOR'}:errors.append('LEDGER_ROLE_INVENTORY')
 allrect=[q for rs in expected.values()for q in rs]+[q for rs in actual.values()for q in rs]
 ys=sorted({F(0),L}|{v for q in allrect for v in(q[1],q[3])if 0<v<L});tested=0
 for y0,y1 in zip(ys,ys[1:]):
  y=(y0+y1)/2;active=[q for q in allrect if q[1]<y<q[3]];xs=sorted({F(0),W}|{v for q in active for v in(q[0],q[2])if 0<v<W})
  for x0,x1 in zip(xs,xs[1:]):
   x=(x0+x1)/2;want=next((k for k,_ in raw if any(q[0]<x<q[2]and q[1]<y<q[3]for q in expected[k])),'UNASSIGNED_PLOT_FLOOR');got=[k for k,rs in actual.items()if any(q[0]<x<q[2]and q[1]<y<q[3]for q in rs)];tested+=1
   if got!=[want]:errors.append('LEDGER_ROLE_NOT_ACTUAL_GEOMETRY:'+want);break
 return response(errors,pending,dict(r['witness'],exact_role_cells=tested),'Exact disjoint plot ledger additionally bound to every actual wall/unit/common cell with source precedence; residual useful capacity is not inferred')
ADAPTERS['partition_ledger']=partition_ledger
from fairness_audit118 import worst_unit_function
ADAPTERS['worst_unit_function']=worst_unit_function
from circulation_named_audit118 import private_grouping,long_corridor_facts
ADAPTERS['private_grouping']=private_grouping
from core_circulation_scope118 import applicability as circulation_applicability, evaluate as circulation_evaluate
ADAPTERS['long_corridor_necessity']=circulation_evaluate
APPLICABILITY_ADAPTERS={'long_corridor_necessity':circulation_applicability}
# Scope119: comparative preference remains review; actual functional integrity is mandatory.
from circulation_integrity119 import evaluate as circulation_functional_integrity
ADAPTERS['circulation_functional_integrity']=circulation_functional_integrity
# Version120: final-route floor data must be freshly derived, not pre-reroute residue.
def circulation_functional_integrity120(m, *, frame_core=None,frame_local=None):
 from circulation_integrity119 import evaluate as physical_integrity
 from final_route_ledger120 import evaluate as final_ledger
 a=physical_integrity(m,frame_core=frame_core,frame_local=frame_local);b=final_ledger(m)
 errors=list(a['witness'].get('errors',[]))+b['witness']['errors'];pending=list(a['witness'].get('pending',[]))
 return response(errors,pending,{'actual_functional_integrity':a,'final_route_classification':b},'Mandatory current physical circulation plus exact final-route floor classification; comparison preference and residual-useful capacity remain separate.')
ADAPTERS['circulation_functional_integrity']=circulation_functional_integrity120
from actual_opening_geometry121 import evaluate as actual_opening_geometry
ADAPTERS['actual_opening_geometry']=actual_opening_geometry

ADAPTERS.pop('window_opportunities',None)
