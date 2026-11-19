"""Bounded fixed-route certificates and diagnostic overlays, never design delivery."""
import copy,html,inspect,json,pathlib,sys
from fractions import Fraction as F
from front_rear_runtime_adapter import ROOT,ENGINE,ensure,source_audit
from same_version_front_rear_contract import digest
from kitchen_guest_review import rect,sweeps
from source_guest_route_evaluator import assess as guest_assess,route_check
from fixed_route_clearance_diagnostic import fixed_polyline_capacity
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def scene(m,u,name):
 from geometry114 import cells
 uid=u['id'];body=F(m['profile']['body_m'])
 ko=next(o for o in m['operations']['kitchen'] if o['unit']==uid)
 obstacles=list(m['walls'].values())+[o['open_panel'] for o in m['operations']['doors']]
 labels=['wall:'+k for k in m['walls']]+['open_panel:'+str(i) for i,o in enumerate(m['operations']['doors'])]
 fx=[];fl=[]
 for k,q in u['fixtures'].items():
  if not u['fixture_metadata'][k].get('walkable') and not(name=='entry_WC' and k=='WC_iranian'):fx.append(q);fl.append('fixture:'+k)
 if name=='entry_WC':
  wc=u['activities']['WC_use'];q=rect(wc);x,y=(q[0]+q[2])/2,(q[1]+q[3])/2
  target=list(map(str,[x-body/2,y-body/2,x+body/2,y+body/2]))
  remain=cells([u['fixtures']['WC_iranian']],[target]);fx+=remain;fl+=['WC_non_target_material:'+str(i) for i in range(len(remain))]
 obstacles+=fx;labels+=fl
 for o in m['operations']['dining_chairs']:
  if o['unit']!=uid:continue
  a,b=rect(o['closed_rect']),rect(o['open_rect'])
  obstacles += [list(map(str,[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])])),o['occupied_body']]
  labels += ['chair_swept:'+o['fixture_id'],'chair_occupied:'+o['fixture_id']]
 for role,qs in u['rooms'].items():
  if role.startswith('bed') or role=='private_circulation':
   obstacles+=qs;labels+=['private:'+role+':'+str(i) for i in range(len(qs))]
 zones=[u['activities']['kitchen_work']]+ko['motion_envelopes']+[z['actor_rect'] for z in ko['workstations']]
 obstacles+=zones
 labels+=['kitchen_work']+['kitchen_motion:'+str(i) for i in range(len(ko['motion_envelopes']))]+['kitchen_workstation:'+str(i) for i in range(len(ko['workstations']))]
 occupied=[s['occupied_body'] for s in u['public_program']['capacity']['living_seats']]
 obstacles+=occupied;labels+=['living_occupied:'+s['fixture_id'] for s in u['public_program']['capacity']['living_seats']]
 roles=['living','entry_circulation','dining','kitchen']+(['bath'] if name=='entry_WC' else [])
 parts=[q for role in roles for q in u['rooms'].get(role,[])]
 for p in m['module_placements']:
  if p['unit_id']==uid and p['room_id'] in ('kitchen','bath'):parts+=m['module_aprons'][uid+'.'+p['room_id']]
 parts=cells(parts,[]);owner=u['ownership'];qs=list(map(rect,owner))
 box=list(map(str,[min(q[0] for q in qs),min(q[1] for q in qs),max(q[2] for q in qs),max(q[3] for q in qs)]))
 for label,domain in [('outside_floor',parts),('outside_owner',owner)]:
  outside=cells([box],domain);obstacles+=outside;labels+=[label+':'+str(i) for i in range(len(outside))]
 ensure(len(obstacles)==len(labels),'OBSTACLE_LABEL_COUNT')
 return {'parts':parts,'owner':owner,'box':box,'obstacles':obstacles,'labels':labels,'roles':roles,'body':str(body),'kitchen_operation_digest':digest(ko)}
def certify(row,s,path_digest):
 from public_program_audit118 import covered
 ensure(digest(row['path'])==path_digest,'PATH_DIGEST')
 ensure(row['state']=='PASS_SOURCE_PROFILE_ROUTE_ONLY','ROUTE_NOT_WITNESSED')
 ensure(row['floor_roles']==s['roles'] and row['floor_digest']==digest(s['parts']) and row['ownership_digest']==digest(s['owner']) and digest(row['domain_box'])==digest(s['box']),'DOMAIN_BINDING')
 ensure(row['obstacle_digest']==digest(s['obstacles']) and row['obstacle_count']==len(s['obstacles']),'SCENARIO_BINDING')
 body=F(s['body']);ensure(body==F(row['body_m'])==F('.7'),'SOURCE_BODY')
 route_check(row['path'],row['start'],row['end'],body,s['parts'],s['obstacles'])
 for band in sweeps(row['path'],body):ensure(covered(band,list(map(rect,s['owner']))),'OWNER_COVERAGE')
 cap=fixed_polyline_capacity(row['path'],s['box'],s['obstacles']);width=F(cap['maximum_uniform_axis_aligned_square_width_m'])
 ensure(width>=body,'CAPACITY_CONTRADICTION')
 route_check(row['path'],row['start'],row['end'],width,s['parts'],s['obstacles'])
 for band in sweeps(row['path'],width):ensure(covered(band,list(map(rect,s['owner']))),'CAPACITY_OWNER')
 try:route_check(row['path'],row['start'],row['end'],width+F(1,1000000),s['parts'],s['obstacles'])
 except ValueError as ex:
  ensure(str(ex) in ('ROUTE_DOMAIN_COVERAGE','ROUTE_OBSTACLE_COLLISION'),'UNRELATED_REJECTION');cause=str(ex)
 else:raise ValueError('ABOVE_CAPACITY_NOT_REJECTED')
 for c in cap['limiting_constraints']:
  if c['kind']=='obstacle':c['source_label']=s['labels'][c['obstacle_index']]
 cap['independent_certificate']={'at_capacity_clear':True,'above_capacity_rejection':cause,'test_epsilon_m':'1/1000000','epsilon_is_design_threshold':False}
 cap['domain_scope']='Fixed orthogonal path in exact typed-floor and ownership union via complement obstacles plus independent coverage checks; not globally best route, bottleneck doorway width, ergonomics or state-complete operation proof.'
 return {'path_digest':path_digest,'source_body_sweeps':[list(map(str,b)) for b in sweeps(row['path'],body)],'capacity':cap,'scene_digest':digest(s)}
def overlay(uid,row,s,certificate,mh):
 b=list(map(F,s['box']));scale=35.;margin=25.;top=65.
 W=float(b[2]-b[0])*scale+2*margin;H=float(b[3]-b[1])*scale+top+margin
 def rectangle(q,fill,stroke='none',opacity=1):
  x0,y0,x1,y1=map(F,q)
  return '<rect x="'+str(margin+float(x0-b[0])*scale)+'" y="'+str(top+float(b[3]-y1)*scale)+'" width="'+str(float(x1-x0)*scale)+'" height="'+str(float(y1-y0)*scale)+'" fill="'+fill+'" stroke="'+stroke+'" opacity="'+str(opacity)+'"/>'
 pieces=['<svg xmlns="http://www.w3.org/2000/svg" width="'+str(W)+'" height="'+str(H)+'" viewBox="0 0 '+str(W)+' '+str(H)+'">','<rect width="100%" height="100%" fill="white"/>']
 pieces+=['<text x="15" y="20" font-size="13">DIAGNOSTIC REVIEW ONLY / NOT QUALIFIED</text>','<text x="15" y="39" font-size="11">'+html.escape(uid+' '+row['id']+' / '+mh[:12])+'</text>']
 pieces += [rectangle(q,'#edf0f3') for q in s['parts']]
 # Clip obstacle rendering to route-domain box without changing geometry checks.
 for q in s['obstacles']:
  r=rect(q);v=[max(r[0],b[0]),max(r[1],b[1]),min(r[2],b[2]),min(r[3],b[3])]
  if v[0]<v[2] and v[1]<v[3]:pieces.append(rectangle(v,'#d99c74',opacity=.55))
 pieces += [rectangle(q,'#3fb8d1',opacity=.45) for q in certificate['source_body_sweeps']]
 for c in certificate['capacity']['limiting_constraints']:
  if c['kind']=='obstacle':pieces.append(rectangle(c['rect'],'none','#c93030'))
 points=' '.join(str(margin+float(F(p[0])-b[0])*scale)+','+str(top+float(b[3]-F(p[1]))*scale) for p in row['path'])
 pieces.append('<polyline points="'+points+'" fill="none" stroke="#124ac0" stroke-width="2"/>')
 pieces.append('</svg>');return ''.join(pieces)
def assess(bundle,directory):
 strict_pin=digest(bundle);m=bundle['packet']['world_model'];mh=digest(m)
 ensure(mh==bundle['model_digest'] and bundle['reports']['physical']['model_hash']==mh,'SAME_MODEL')
 ensure(digest(bundle['reports']['physical'])==bundle['report_digests']['physical'],'PHYSICAL_DIGEST')
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration')]
 from producer_provenance import snapshot,require_unchanged
 from geometry114 import cells
 from public_program_audit118 import covered
 paths=['app/local_integration/'+x for x in ('guest_route_certificate_study.py','source_guest_route_evaluator.py','fixed_route_clearance_diagnostic.py','kitchen_guest_review.py','current_programme_evaluator.py','guest_four_route_diagnostic.py')]
 snap=snapshot(ROOT,paths);audit=source_audit()
 for fn,path in [(cells,ENGINE/'fast_cells120.py'),(covered,ENGINE/'public_program_audit118.py'),(guest_assess,ROOT/paths[1]),(route_check,ROOT/paths[1]),(fixed_polyline_capacity,ROOT/paths[2]),(sweeps,ROOT/paths[3])]:
  ensure(pathlib.Path(inspect.getsourcefile(fn)).resolve()==path,'IMPORT_SOURCE')
 out={'schema':'EIGHT_GUEST_FIXED_PATH_CERTIFICATES_V1','state':'UNKNOWN','model_digest':mh,'historical_physical_digest':bundle['report_digests']['physical'],'source_snapshot':snap,'rows':[],'integrity_verified':False,'completed':False,'scope':'Fresh construction of existing four-route study profile; new fixed-path certificates/diagnostic overlays only. Historical model, not current input generation. No global clearance, ergonomic or architectural approval.',**{k:False for k in AUTH}}
 def save():
  tmp=directory/'report.tmp';tmp.write_text(json.dumps(out,sort_keys=True,indent=2));tmp.replace(directory/'guest-certificates.json')
 save()
 try:
  guest=guest_assess(bundle);gp=digest(guest)
  ensure(guest.get('integrity_verified') is True and not guest.get('missing'),'FRESH_ROUTE_EVALUATOR')
  ensure(guest['model_digest']==mh and guest['original_physical_digest']==out['historical_physical_digest'],'ROUTE_REPORT_BINDING')
  out['fresh_route_report_digest']=gp
  for u in m['units']:
   g=next(z for z in guest['units'] if z['unit']==u['id'])
   ensure(len(g['routes'])==4,'FOUR_ROUTES')
   for r in g['routes']:
    row={'unit':u['id'],'route_id':r['id'],'route_state':r['state'],'usable_evidence':False};out['rows'].append(row);save()
    try:
     if r['state']!='PASS_SOURCE_PROFILE_ROUTE_ONLY':row['state']='NO_SOURCE_WITNESS_CERTIFICATE_NOT_EVALUATED';continue
     s=scene(m,u,r['id']);ensure(s['kitchen_operation_digest']==g['kitchen_operation_digest'],'OPERATION_BINDING')
     cert=certify(r,s,digest(r['path']))
     row.update(state='CERTIFIED_FIXED_PATH_ONLY',route=copy.deepcopy(r),certificate=cert,scenario=g['scenario'],operation_digest=g['kitchen_operation_digest'])
     svg=overlay(u['id'],r,s,cert,mh);filename=u['id']+'_'+r['id']+'.svg';(directory/filename).write_text(svg)
     import hashlib
     row['overlay']={'file':filename,'sha256':hashlib.sha256(svg.encode()).hexdigest(),'model_digest':mh,'path_digest':cert['path_digest'],'scene_digest':cert['scene_digest'],'diagnostic_only':True}
     ensure(digest(bundle)==strict_pin and digest(guest)==gp,'INPUT_OR_REPORT_MUTATION')
    except Exception as ex:row.update(state='EVALUATOR_OR_BINDING_ERROR',error_type=type(ex).__name__,error_code=str(ex)[:120])
    finally:save()
  out['completed']=len(out['rows'])==8 and all(r['state']=='CERTIFIED_FIXED_PATH_ONLY' for r in out['rows'])
 except Exception as ex:out.update(error_type=type(ex).__name__,error_code=str(ex)[:120])
 finally:
  try:
   ensure(digest(bundle)==strict_pin,'INPUT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==audit,'SOURCE_CHANGED');out['integrity_verified']=True
   for r in out['rows']:r['usable_evidence']=r.get('state')=='CERTIFIED_FIXED_PATH_ONLY'
  except Exception as ex:
   out.update(state='INTEGRITY_ERROR',completed=False,integrity_verified=False,integrity_error=type(ex).__name__)
   for r in out['rows']:r['usable_evidence']=False
  save()
 return out
if __name__=='__main__':
 directory=pathlib.Path(sys.argv[2]);directory.mkdir(exist_ok=False)
 assess(json.loads(pathlib.Path(sys.argv[1]).read_bytes()),directory)
