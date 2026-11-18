"""Per-input bounded Q04 common-circulation comparison, no length cutoff.
Historical full-span alternative is checked as a CORE COMPONENT ONLY. Its unit
interfaces are explicit conditional stubs, never purported habitable units.
Current whole model remains subject to all separate functional named gates.
"""
from fractions import Fraction as F
import hashlib,json
from core_wall_audit118 import q,hit,covered,sweep,core_concept,opening_hosts,output,safe
from circulation_named_audit118 import area,measures,long_corridor_facts

SOURCE={'Q04': {'source_line': 591, 'source_text': 'Q04 CIRCULATION — طول مسیر واقعی ورود تا عملکردها، دورزدن نسبت به مسیر مرجع، تعداد گلوگاه و پیچ و سطح مصرف\u200cشده گردش؛ profile فعالیت معلوم باشد. حذف راهرو با تخریب استفاده واقعی برتری نیست.', 'source_modified': '2026-11-12T19:13:23.746Z'}, 'IR-P10': {'source_line': 4002, 'source_text': 'IR-P10 | گردش آشکار و پنهان\nدر همه پلان\u200cها؛ مسیر عبور از میان مبلمان فرضی، مقابل تلویزیون و ناحیه غذاخوری نیز گردش است؛ مساحت یک\u200cبار شمرده شود. منبع و ردیابی: S04؛ Q04. مصالحه: راهروی حذف\u200cشده در برابر اختلال فعالیت. زیرآزمون جاری: مساحت گردش اختصاصی و گردش داخل نشیمن/غذاخوری جدا اندازه\u200cگیری و بدون دوباره\u200cشماری گزارش شوند؛ نوار باریک با نام «ادامه نشیمن» فقط وقتی سطح نشستن محسوب شود که چیدمان و عبور هم\u200cزمان قابل استفاده شاهد داشته باشند. حذف نام راهرو یا دیوار، به\u200cتنهایی فضای مفید ایجاد نمی\u200cکند.', 'source_modified': '2026-11-12T19:13:23.746Z'}, 'long_corridor_condition': {'source_line': 7, 'text': 'راهروی طولانی تنها با مقایسه بدیل و دلیل ضرورت مجاز است.'}, 'blueprint_sha256': 'd9cf1ac027529a0c340d6ce4c8a3c8dee595202832dcddc6484480caf9584d9a'}

def applicability(m):
 return {'status':'PASS_LIMITED','witness':{'applies':True,'scope':'Assess actual common junction versus historical full-span core component and record its route costs; does not classify all analytical body-route floor as long corridor.'},'scope':'No invented metre/aspect-ratio threshold; current private grouping and bath-access gates remain separate.'}

def subtract(r,cut):
 x,y,X,Y=r;a,b,A,B=cut;a=max(x,a);b=max(y,b);A=min(X,A);B=min(Y,B)
 if a>=A or b>=B:return[r]
 return [q for q in[(x,y,a,Y),(A,y,X,Y),(a,y,A,b),(a,B,A,Y)]if q[0]<q[2]and q[1]<q[3]]
def component(m):
 W,L=map(F,m['inputs'][:2]);s=q(m['common_spaces']['stair']);lift=q(m['common_spaces']['lift']);sw,sh=s[2]-s[0],s[3]-s[1];lw,lh=lift[2]-lift[0],lift[3]-lift[1]
 actualhosts=m['wall_hosts'];t=s[0]-q(actualhosts['core.stair.left'])[0];border=q(m['walls']['left'])[2]
 if t<=0 or border<=0:raise ValueError('CORE_PROFILE_THICKNESS_UNRESOLVED')
 y=s[1]-t;Y=s[3]+t;stair=(border+t,y+t,border+t+sw,Y-t);lift=(W-border-t-lw,Y-t-lh,W-border-t,Y-t)
 left=stair[2]+t;right=lift[0]-t
 if right<=left:return {'status':'COMPONENT_NOT_FEASIBLE','reason':'NO_POSITIVE_SHARED_LOBBY_BETWEEN_PRESERVED_CORES','clear_core_sizes':{'stair':[str(sw),str(sh)],'lift':[str(lw),str(lh)]},'whole_plan_feasible':False}
 lobby=[(left,y,right,Y)]
 if lift[1]-t>y:lobby.append((right,y,W-border,lift[1]-t))
 aperture={o['id']:q(o['rect'])for o in m['openings']}
 def width(name):
  r=aperture[name];return max(r[2]-r[0],r[3]-r[1])
 ew=width('A.entry')
 if width('B.entry')!=ew:raise ValueError('HISTORICAL_COMPONENT_REQUIRES_SAME_ENTRY_APERTURE_WIDTH')
 cx=left+F('.7');body=F(str(m['profile']['body_m']));h=body/2;ops=[];walls=[];interface=[]
 # Same historical opening widths and source-driven core profiles; no scaling.
 def wall(r,opening=None):
  if opening is None:walls.append(r)
  else:walls.extend(subtract(r,opening));ops.append(opening)
 for uid,lo,hi in [('A',y-t,y),('B',Y,Y+t)]:
  o=(cx-ew/2,lo,cx+ew/2,hi);wall((border,lo,W-border,hi),o)
  interface.append((cx-ew/2,lo-F('.8'),cx+ew/2,hi+F('.8')))
 for name,r,side,dw in [('stair',stair,'right',width('stair.entry')),('lift',lift,'left',width('lift.entry'))]:
  x0,y0,x1,y1=r;cy=(y0+y1)/2
  for sid,rect in [('left',(x0-t,y0-t,x0,y1+t)),('right',(x1,y0-t,x1+t,y1+t)),('bottom',(x0,y0-t,x1,y0)),('top',(x0,y1,x1,y1+t))]:
   wall(rect,(rect[0],cy-dw/2,rect[2],cy+dw/2)if sid==side else None)
 paths={}
 for uid,ty in [('A',y-t-F('.4')),('B',Y+t+F('.4'))]:
  for src,r,px in [('stair',stair,stair[2]-F('.4')),('lift',lift,lift[0]+F('.4'))]:paths[src+'_'+uid]=[[str(px),str((r[1]+r[3])/2)],[str(cx),str((r[1]+r[3])/2)],[str(cx),str(ty)]]
 errors=[];frame=(F(0),F(0),W,L)
 for r in [stair,lift]+lobby+walls:
  if not all(F(0)<=v for v in r)or not(r[2]<=W and r[3]<=L):errors.append('COMPONENT_OUTSIDE_FRAME')
 if hit(stair,lift)or any(hit(r,stair)or hit(r,lift)for r in lobby):errors.append('CORE_LOBBY_OVERLAP')
 for key,path in paths.items():
  src,uid=key.split('_');allowed=[stair if src=='stair'else lift]+lobby+ops+interface
  for r in sweep(path,body):
   if not covered(r,allowed)or any(hit(r,w)for w in walls):errors.append(key+':COMPONENT_BODY_PATH_INVALID')
   if hit(r,lift if src=='stair'else stair):errors.append(key+':OTHER_CORE_CROSSING')
 return {'status':'PASS_CORE_COMPONENT_GEOMETRY'if not errors else'FAIL_CORE_COMPONENT_GEOMETRY','errors':sorted(set(errors)),'inputs':m['inputs'],'clear_core_sizes':{'stair':[str(sw),str(sh)],'lift':[str(lw),str(lh)]},'stair':list(map(str,stair)),'lift':list(map(str,lift)),'lobby':[list(map(str,r))for r in lobby],'walls':[list(map(str,r))for r in walls],'openings':[list(map(str,r))for r in ops],'conditional_unit_interface_stubs':[list(map(str,r))for r in interface],'routes':paths,'route_metrics':{k:measures(p)for k,p in paths.items()},'lobby_union_area_m2':str(area(lobby)),'whole_plan_feasible':False,'not_checked':['unit furniture/program compatibility at these alternative interfaces','whole-plan privacy or daylight','core hardware/installation'],'source':'Reconstruction of actual historical full-span central-band core pattern, not a selected whole candidate or intentionally invented inferior fixture.'}

def grammar(m, *, frame_core=None,frame_local=None):
 """Current module-composed two-bedroom grammar only, never arbitrary labels.
 Unknown enclosing-wall sources/rooms remain pending, including renamed halls.
 Separate mandatory module-placement tests prove every mapped wall geometry.
 """
 from private_binding121 import examine as bind_private
 binding=bind_private(m) if m.get('private_domains') else None
 missing=[];mapped=set();supported={'PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118','BATHROOM_MODULE117','KITCHEN_MODULE117'}
 for placement in m.get('module_placements',[]):
  module=placement['module']
  if module.get('schema')not in supported:missing.append('UNSUPPORTED_CIRCULATION_MODULE_GRAMMAR')
  mapped|={placement['id_map'][k]for k in module['walls']}
 expected={'left','right','front','back','unit_shared_wing_left','unit_shared_wing_right','core.lobby.outer_right'}
 expected|={uid+'.unit_boundary.solid'+str(i)for uid in('A','B')for i in(0,1)}
 expected|={'core.stair.'+k for k in('left','bottom','top','right.solid0','right.solid1')}
 expected|={'core.lift.'+k for k in('right','bottom','top','left.solid0','left.solid1')}
 if binding is not None:
  missing.extend(binding['errors']+binding['pending']);expected.update(binding['boundary_wall_ids'])
 from notch_grammar362 import allowed_walls
 expected.update(allowed_walls(m,frame_core))
 if m.get('frame_binding125'):
  from frame_circulation125 import grammar as frame_grammar
  missing.extend(frame_grammar(m,frame_core,frame_local))
 elif set(m['walls'])-mapped!=expected:missing.append('UNCLASSIFIED_ENCLOSING_WALL_OR_CORRIDOR_SOURCE')
 for u in m['units']:
  beds={k for k in u['rooms']if k.startswith('bed')}
  allowed_extra={'private_circulation'} if len(beds)==3 and binding is not None else set()
  if beds not in ({'bed1'},{'bed1','bed2'},{'bed1','bed2','bed3'}) or set(u['rooms']) != beds|{'bath','kitchen','dining','living','entry_circulation'}|allowed_extra:missing.append(u['id']+':UNSUPPORTED_OR_RENAMED_ROOM_CIRCULATION_GRAMMAR')
 from paired_private_zone118 import examine
 pairs=examine(m)
 for u in m['units']:
  beds={k for k in u['rooms']if k.startswith('bed')}
  if len(beds)==3 and binding is not None and not binding['errors'] and not binding['pending']:
   continue
  if len(beds)==1:
   # Source-bound placement and actual access are checked independently; a
   # two-bedroom paired zone is inapplicable, not waived for multi-bedroom.
   placed=[p for p in m.get('module_placements',[]) if p.get('module',{}).get('schema') in {'PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118'} and any(v.startswith(u['id']+'.bed1.') for v in p.get('id_map',{}).values())]
   if len(placed)!=1:missing.append(u['id']+':SINGLE_BEDROOM_SOURCE_PLACEMENT_MISSING')
   continue
  if not any(z['unit']==u['id']and z['status']=='PASS_TWO_BEDROOM_PRIVATE_APPROACH_TOPOLOGY'and set(z['bedrooms'])=={u['id']+'.bed1',u['id']+'.bed2'}for z in pairs['zones']):missing.append(u['id']+':NO_INDEPENDENT_REAL_PAIRED_PRIVATE_ZONE')
 return sorted(set(missing))

def _evaluate(m,workflow_context=None):
 errors=[];pending=[]
 frame_witness=None
 if m.get('frame_binding125')or workflow_context:
  from circulation_frame148 import examine as frame_binding
  frame_witness=frame_binding(m,workflow_context);errors.extend(frame_witness['errors']);pending.extend(frame_witness['pending'])
 if m.get('frame_binding125'):
  # Historical component assumes native front/rear axes. Do not run it on
  # transposed world geometry or convert a binding repair into quality PASS.
  baseline={'status':'NOT_EVALUATED_FRAME_COMPARISON','reason':'HISTORICAL_COMPONENT_FRAME_BOUND_COMPARISON_REQUIRED','whole_plan_feasible':False}
 else:baseline=component(m)
 W,L=map(F,m['inputs'][:2])
 if not m.get('frame_binding125') and (q(m['walls']['left'])[0]!=0 or q(m['walls']['right'])[2]!=W or q(m['walls']['front'])[1]!=0 or q(m['walls']['back'])[3]!=L):errors.append('CURRENT_ACTUAL_FRAME_RAW_INPUT_BINDING')
 if F(str(m['profile']['body_m']))!=F('.7'):pending.append('BODY_PROFILE_OUTSIDE_CURRENT_SOURCE_STUDY')
 grammar_errors=grammar(m,frame_core=(workflow_context or{}).get('frame_core125'),frame_local=(workflow_context or{}).get('frame_local129'))
 pending.extend(grammar_errors)
 current_core=core_concept(m);hosts=opening_hosts(m)
 if current_core['status']!='PASS_LIMITED'or hosts['status']!='PASS_LIMITED':pending.append('CURRENT_ACTUAL_CORE_OR_HOST_CHECK_NOT_PASSED')
 if m['inputs'][2]!=2:pending.append('THIS_COMPONENT_COMPARISON_PROFILE_REQUIRES_TWO_UNITS')
 # Named constructed corridors, if supplied, cannot be excused by common-core
 # reduction. Analytical entry_circulation alone does not trigger this condition.
 corridors=[u['id']+'.private_corridor'for u in m['units']if u['rooms'].get('private_corridor')]
 if corridors:pending.append('SEPARATE_CONSTRUCTED_PRIVATE_CORRIDOR_COMPARISON_REQUIRED')
 current_lobby=[q(r)for r in m['common_spaces']['lobby']];current_area=area(current_lobby);routes={k:measures(v)for k,v in m['common_routes'].items()}
 if baseline['status']!='PASS_CORE_COMPONENT_GEOMETRY':pending.append('HISTORICAL_COMPONENT_COMPARISON_NOT_GEOMETRICALLY_VALID')
 else:
  deltas={k:F(v['length_m'])-F(baseline['route_metrics'][k]['length_m'])for k,v in routes.items()}
  if current_area>=F(baseline['lobby_union_area_m2'])or not any(v<0 for v in deltas.values())or any(v>0 for v in deltas.values()):pending.append('CURRENT_COMMON_CIRCULATION_REDUCTION_NOT_ESTABLISHED')
 # Extra rectangle without any actual required route use is NOT necessary
 # functional circulation. Preserve physical floor; report it as unprogrammed.
 unused=[];body=F(str(m['profile']['body_m']))
 for i,r in enumerate(current_lobby):
  if not any(hit(r,s)for p in m['common_routes'].values()for s in sweep(p,body)):unused.append({'component':i,'rect':list(map(str,r)),'area_m2':str(area([r])),'classification':'COMMON_UNPROGRAMMED_NOT_PROVEN_FUNCTIONAL','no_geometry_changed':True})
 common_scope_ready=not errors and not pending
 internal=long_corridor_facts(m)
 # Existing routes are measured and separately collision-checked, but neither
 # their existence nor a comparison of relocated core interfaces proves the
 # necessity of internal detours. Do not launder a component PASS into Q04.
 pending.append('INTERNAL_CIRCULATION_COMPARATIVE_NECESSITY_NOT_ESTABLISHED')
 return output('Q04',errors,pending,{'source':SOURCE,'actual_frame_binding148':frame_witness,'common_core_subcondition_status':'PASS_LIMITED'if common_scope_ready else'NOT_EVALUATED_OR_FAILED','internal_route_cost_facts':internal['witness'],'internal_comparison_required_next':['Same actual start/end functional targets and body/obstacle/door state, independently route a feasible alternative in the same floor, compare length/bends and any bottleneck; this is a path alternative, not an alternative dwelling.','If layout-created long corridor remains after route comparison, a genuine same-program layout alternative and explicit selection trade-off are still needed; no universal optimality proof demanded.'],'endpoint_comparison_warning':'Historical/current core route endpoints move with stair/lift/interfaces. Deltas compare component arrangements, not detour between fixed endpoints.','supported_grammar_findings':grammar_errors,'current_component_check':current_core,'current_hosts_check':hosts,'historical_fullspan_core_component':baseline,'current_lobby_union_area_m2':str(current_area),'current_common_route_metrics':routes,'common_unprogrammed_components':unused,'selection_reason':('No verified common-core selection comparison is established for this frame.'if not common_scope_ready else 'For this same raw input and preserved clear stair/lift sizes, retain the actual compact core with fewer shared-floor metres and no longer required common body route than the independently checked historical component. Current unit functionality is checked separately; the historical interfaces are conditional and do not certify another whole dwelling.'),'local_scope':'Bounded common-core comparison and explicit route-cost accounting; not minimum lobby width, global optimum, proof of all private corridor necessity, or architectural-quality approval.','panel_projection_warning':'An entry panel inside a unit does not prove an equal lobby-floor width physically necessary.','analytical_entry_circulation_is_not_automatically_constructed_corridor':True})


def evaluate(m,workflow_context=None):
 # Preserve legacy fail-closed exception classification while binding context.
 return safe(lambda actual:_evaluate(actual,workflow_context))(m)
