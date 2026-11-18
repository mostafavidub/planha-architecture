"""Read-only IR-P07 measurement, no candidate or threshold generation."""
from build_ledger import *
from comparison_metrics import route_metrics,rectangle_union_area
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent

def gate():
 manifest=HERE/'q04_manifest362_v3.json';j=json.loads(manifest.read_text())
 for n,h in j['files'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('FIXED_READSET_CHANGED:'+n)
 return hashlib.sha256(manifest.read_bytes()).hexdigest()
def portal_center(o):
 a,b,c,d=map(F,o['rect']);return [(a+c)/2,(b+d)/2]
def measure(c):
 m=c['model'];opens={o['id']:o for o in m['openings']};out={}
 for task,path in m['common_routes'].items():
  q=route_metrics(path);source,unit=task.split('_');s=opens[source+'.entry'];e=opens[unit+'.entry'];sp,ep=portal_center(s),portal_center(e)
  if len(path)!=3:raise ValueError('SOURCE_ROUTE_NOT_TWO_SEGMENT')
  pts=[list(map(F,p))for p in path]
  # Same actual rectilinear path clipped to portal midplanes, not a new route.
  if not(pts[0][1]==pts[1][1]and pts[1][0]==pts[2][0]and sp[1]==pts[0][1]and ep[0]==pts[2][0]):raise ValueError('PORTAL_PATH_CLIPPING_UNSUPPORTED')
  clipped=[sp,pts[1],ep];cq=route_metrics([[str(v)for v in p]for p in clipped])
  def width(o):
   a,b,c,d=map(F,o['rect']);return max(c-a,d-b)
  out[task]={'actual_source_path':path,'length_m':q['length'],'turns':q['direction_changes'],'portal_midplane_path':[[str(v)for v in p]for p in clipped],'portal_to_portal_length_m':cq['length'],'portal_to_portal_turns':cq['direction_changes'],'portal_aperture_widths_m':{'source':str(width(s)),'destination':str(width(e))},'exact_route_bottleneck_clearance_m':None,'bottleneck_status':'UNKNOWN_NOT_MEASURED_BY_STORED_CORE_ROUTE_WITNESS','selected_body_profile_m':str(F(m['profile']['body_m']))}
 return {'routes':out,'lift_length_A_minus_B_m':str(F(out['lift_A']['length_m'])-F(out['lift_B']['length_m'])),'lift_turn_A_minus_B':out['lift_A']['turns']-out['lift_B']['turns'],'common_lobby_area_m2':str(rectangle_union_area(m['common_spaces']['lobby'])),'core_geometry':m['common_spaces'],'portals':{k:opens[k]for k in ('lift.entry','stair.entry','A.entry','B.entry')}}
def run():
 freeze=gate();rows=[]
 for name,path in [('baseline351','actual_run/actual_response.json'),('translated357','staging357_comparative/attached_service_final357.json'),('row358','staging358_comparative/row_candidate358.json'),('clamped359','staging359_hall_clamp/actual359.json'),('notched362','staging362_core_notch/actual362.json')]:
  p=ROOT/path;r=json.loads(p.read_text());c=r['selected'][0]if name=='baseline351'else r['candidate'];rows.append({'id':name,'artifact':path,'artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'model_digest':digest(c['model']),'request':c['request'],'program':c['model']['program'],'profile':c['model']['profile'],'measured':measure(c)})
 assert len({digest(x['request'])for x in rows})==len({digest(x['program'])for x in rows})==len({digest(x['profile'])for x in rows})==1
 invariant=len({digest(x['measured']['routes'])for x in rows})==1
 source=ROOT.parent/'recovered233_rendered/sections.json';doc=json.loads(source.read_text());section=doc['sections']['IR-P07']
 if gate()!=freeze:raise ValueError('READSET_MUTATED')
 return {'schema':'IR_P07_READONLY_FIVE_EXISTING_CANDIDATES362','source_contract':{'file':str(source),'file_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'author_rendered_sha256':doc['source_sha256'],'selector':section['source_selector'],'character_range':section['html_character_range'],'algorithm':section['fields']['رابطه و الگوریتم دقیق'],'no_invented_significance_tolerance':True},'readset_manifest_sha256':freeze,'members':rows,'exact_existing_routes_and_portals_metrics_invariant':invariant,'better_balance_alternative_in_this_cohort':False if invariant else None,'balance_resolved':False,'missing':['Exact free bottleneck width along required actual paths (not portal aperture or selected body size)','Supported balance resolution or explicit owner decision; no numeric negligible tolerance invented','Actual alternative core/entry placement improving balance while preserving required functional use if redesign is pursued'],'engineering_framework':{'comparison':'Keep per-unit vector (actual length, turns, measured bottleneck, door conflicts, source waiting/arrival use) separate; require protected use and componentwise non-deterioration for an improving alternative, no averaging across units','balance':'Record signed and absolute A/B differences, not a PASS threshold. Zero observed difference is descriptive, not proof all access conditions satisfied. Nonzero unresolved difference remains explicit.','invariance_scope':'Only these five fixed candidates. Same portal/core source positions explain common route invariance; no claim no better placement exists.'},'no_generation':True,'no_solver':True,'no_new_fresh':True,'accepted':False}
if __name__=='__main__':
 x=run();p=HERE/'lift_balance_readonly_actual362.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2));print([(a['id'],a['measured']['lift_length_A_minus_B_m'],a['measured']['routes']['lift_A']['length_m'],a['measured']['routes']['lift_B']['length_m'])for a in x['members']])
