"""TEST_ONLY local counterfactual. No solver, whole model or Origin creation."""
import json,hashlib,copy,time,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'planha_general150_runtime_work'

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def transform(src):
 m=copy.deepcopy(src);u=m['unit'];c=list(map(F,u['fixtures']['bed1.closet']));room=list(map(F,u['rooms']['bed1'][0]));clearance=c[1]-room[1]
 # +90 degrees: source front +x becomes inward +y on room's long bottom wall.
 if room[2]-room[0]<=room[3]-room[1] or clearance<0:raise ValueError('REGISTERED_HORIZONTAL_LONG_WALL_ONLY')
 tx=c[0]+c[3];ty=room[1]+clearance-c[0]
 def point(p):x,y=map(F,p);return [str(-y+tx),str(x+ty)]
 def vector(p):x,y=map(F,p);return [str(-y),str(x)]
 def rect(r):
  a,b,A,B=map(F,r);ps=[point([x,y])for x in(a,A)for y in(b,B)];xs=[F(p[0])for p in ps];ys=[F(p[1])for p in ps];return list(map(str,(min(xs),min(ys),max(xs),max(ys))))
 op=m['operations']['closets'][0]
 if len(m['operations']['closets'])!=1 or op['fixture_id']!='bed1.closet' or op['front_axis']!='x'or op['front_side']!='max':raise ValueError('SOURCE_CLOSET_PROFILE')
 op['front_axis']='y';op['front_side']='max';op['shell_rects']=[rect(r)for r in op['shell_rects']]
 allowedpanel={'id','closed_panel','open_panel','translation','rail_envelope','states','continuous_actor_segments'}
 for panel in op['panels']:
  if set(panel)!=allowedpanel:raise ValueError('UNSUPPORTED_PANEL_READSET')
  for k in ('closed_panel','open_panel','rail_envelope'):panel[k]=rect(panel[k])
  panel['translation']=vector(panel['translation'])
  for st in panel['states']:
   for k in ('panel_rect','actor_rect'):st[k]=rect(st[k])
   st['hand_point']=point(st['hand_point'])
  for seg in panel['continuous_actor_segments']:
   for k in ('actor_start','actor_end'):seg[k]=rect(seg[k])
   for k in ('hand_start','hand_end'):seg[k]=point(seg[k])
 u['fixtures']['bed1.closet']=rect(u['fixtures']['bed1.closet']);u['fixture_metadata']['bed1.closet']['rotation_deg']=(u['fixture_metadata']['bed1.closet']['rotation_deg']+90)%360
 u['activities']['bed1.closet_front']=rect(u['activities']['bed1.closet_front'])
 # Keep all original paths; moved target invalidates access evidence, not global feasibility.
 u['route_targets']['bed1.closet_front']=point(u['route_targets']['bed1.closet_front'])
 # Counterfactual is derived test geometry, not producer replay or runtime candidate.
 m['source_binding']['producer_sha256']='TEST_ONLY_COUNTERFACTUAL_NOT_REPLAYED'
 proof={'schema':'TEST_ONLY_RIGID_CLOSET_COUNTERFACTUAL','source_module_digest':digest(src),'matrix':[[0,-1],[1,0]],'translation':list(map(str,(tx,ty))),'source_wall_clearance_m':str(clearance),'unchanged_keys':['bounds','walls','wall_hosts','openings','external_ports'],'access_status':'UNKNOWN_OLD_PATH_NOT_REPLANNED','live_authority':False}
 for k in proof['unchanged_keys']:
  if m[k]!=src[k]:raise ValueError('PRESERVED_FIELD_CHANGED:'+k)
 for k,r in src['unit']['fixtures'].items():
  if k!='bed1.closet'and m['unit']['fixtures'][k]!=r:raise ValueError('BED_MOVED')
 for k,r in src['unit']['activities'].items():
  if k!='bed1.closet_front'and m['unit']['activities'][k]!=r:raise ValueError('BED_ACTIVITY_MOVED')
 return m,proof

def sections(m):
 sys.path.insert(0,str(ROOT/'semantic_rules357'))
 from modules_spatial import rect,difference,union_area
 room=list(map(rect,m['unit']['rooms']['bed1']));obs=[rect(r)for r in m['walls'].values()]+[rect(r)for r in m['unit']['fixtures'].values()]+[rect(r)for r in m['unit']['activities'].values()]
 for op in m['operations']['closets']:
  for panel in op['panels']:
   a=rect(panel['closed_panel']);b=rect(panel['open_panel']);obs.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
   for seg in panel['continuous_actor_segments']:
    a=rect(seg['actor_start']);b=rect(seg['actor_end']);obs.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
 for op in m['operations'].get('doors',[]):
  a=rect(op['closed_panel']);b=rect(op['open_panel']);obs.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
 free=difference(room,obs);axisrows={}
 for axis in (0,1):
  bounds=sorted({r[i]for r in room+obs for i in(axis,axis+2)})
  rows=[]
  for a,b in zip(bounds,bounds[1:]):
   midpoint=(a+b)/2;intervals=sorted((r[1-axis],r[3-axis])for r in free if r[axis]<midpoint<r[axis+2]);merged=[]
   for x,X in intervals:
    if merged and x<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],X)
    else:merged.append([x,X])
   rows.append({'slab':list(map(str,(a,b))),'free_intervals':[list(map(str,r))for r in merged],'max_free_section_m':str(max((y-x for x,y in merged),default=F(0)))})
  axisrows[str(axis)]=rows
 return {'free_after_required_reservations_m2':str(union_area(free)),'sections':axisrows,'scope':'EXACT_BREAKPOINT_SLAB_SECTIONS_AFTER_BODIES_AND_RESERVED_USE; NOT_WHOLE_ROOM_USABILITY_OR_ROUTE_PROOF'}

def run():
 pins=json.loads((HERE/'preregistered.json').read_text());start=time.monotonic()
 for name,sha in pins['sources'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_CHANGED:'+name)
 sys.path.insert(0,str(SOURCE));import checker114,privacy116
 record=json.loads((ROOT/pins['artifact']).read_text());model=record['candidate']['model'];rows=[]
 for room in ('bed1','bed2'):
  if time.monotonic()-start>20:raise ValueError('LOCAL_CASE_BUDGET')
  src=next(p['module']for p in model['module_placements']if p['unit_id']=='A'and p['room_id']==room);new,proof=transform(src)
  # At most these two local source module checks. No whole checker or solver.
  report=checker114.check_twin_module(new)if room=='bed2'else checker114.check_module(new)
  fragment=copy.deepcopy(new);fragment['units']=[fragment['unit']];privacy=privacy116.examine_module(fragment)
  rows.append({'room_type':'twin'if room=='bed2'else'double','derivation':proof,'before_sections':sections(src),'after_sections':sections(new),'module_report':report,'privacy_report':privacy,'counterfactual':new,'parent_complete':False,'accepted':False})
 for name,sha in pins['sources'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_CHANGED_AFTER:'+name)
 return {'schema':'TWO_LOCAL_CLOSET_COUNTERFACTUALS_SERVICE365','rows':rows,'elapsed_seconds':time.monotonic()-start,'wholeplan_or_solver_runs':0,'no_general_longitudinal_infeasibility_claim':True,'source_pins':pins}
if __name__=='__main__':
 out=run();(HERE/'result.json').write_text(json.dumps(out,indent=2));print(json.dumps({'elapsed':out['elapsed_seconds'],'rows':[{'type':r['room_type'],'errors':r['module_report']['errors'],'privacy':r['privacy_report']}for r in out['rows']]}))
