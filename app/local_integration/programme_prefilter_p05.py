"""Source-pinned capacity diagnostic; never changes dispatch or quality decisions."""
import argparse,hashlib,inspect,json,re,sys
from fractions import Fraction as Q
from pathlib import Path
from current_entry_boundary_x03 import ROOT,ENGINE,prepare as prepare_core
from public_wln_contract import parse_public,verify_public
from program_profile_registry import lookup
from same_version_front_rear_contract import digest

PINS={
 "app/reconstruction357/planha_general150_runtime_work/capacity_program118.py":"955bc2344d8f92ce403a278e01aa933c824f833d",
 "app/reconstruction357/planha_general150_runtime_work/contract114.py": "a2631c6a38a43b8d423edf82ad8d526ced1b8196",
 "app/reconstruction357/planha_general150_runtime_work/assemble114.py": "6e19b12c62820e015055765e0fe56d6339cd4312",
 "app/reconstruction357/planha_general150_runtime_work/search114.py": "65e0f278c9f9ef480388d3ea8056161c0a938a36",
 "app/local_integration/source_fit_candidate207.py": "be98c37a0827f23b34d6110182c582177532217c",
 "app/local_integration/current_entry_boundary_x03.py": "8383c54d4f6bfd3d94580ede2ab20276b917f414",
 "app/local_integration/public_wln_contract.py": "80fd2b2710342735dc35e484c9b0da790995d830",
 "app/local_integration/program_profile_registry.py": "af549f86f39e2e57554cd48e0ffdea54d5444262"
}
AUTH={k:False for k in ('accepted','qualified','display_allowed','delivery_allowed')}
CORE_ENTRY='SOURCE_FIT207_COMPACT_PAIR'
CORE_KIND='COMPACT_CONNECTED_CENTRAL_CORE118'
CORE_FIELDS={'kind','band','stair','lift','lobby','entry_centers','units','unit_ownership','core_extent_x','outside_band_unit_separator_y','assumptions'}
# Immutable minima of search114 and source_fit_candidate207 for fixed P1/P2, not PRD thresholds.
MINIMA={'double':('5.45','3.6'),'twin':('5.45','4.5'),'bath':('3.15','2.25'),
        'kitchen':('2.35','3.05'),'dining':('3.1','3.5')}
MODULE_SOURCES={'double':'bedroom_module116','twin':'twin_module118','bath':'bathroom_module117',
                'kitchen':'kitchen_module117','dining':'dining_module118'}
class MissingEvidence(ValueError):pass
def require(ok,code):
 if not ok:raise MissingEvidence(code)
def source_guard():
 observed={}
 for path,h in PINS.items():
  file=ROOT/path
  require(file.is_file() and not file.is_symlink(),'SOURCE_FILE_REQUIRED')
  data=file.read_bytes()
  require(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==h,'SOURCE_PIN_CHANGED')
  observed[path]=hashlib.sha256(data).hexdigest()
 for fn,name in ((prepare_core,'current_entry_boundary_x03.py'),(parse_public,'public_wln_contract.py'),
    (verify_public,'public_wln_contract.py'),(lookup,'program_profile_registry.py')):
  require(Path(inspect.getsourcefile(fn)).resolve()==ROOT/'app/local_integration'/name,'ACTUAL_SOURCE_PATH')
 sys.path.insert(0,str(ENGINE))
 import contract114,capacity_program118
 for fn,name in ((contract114.core_first,'contract114.py'),(contract114.program,'contract114.py'),
                 (capacity_program118.proposed_program,'capacity_program118.py')):
  require(Path(inspect.getsourcefile(fn)).resolve()==ENGINE/name,'ACTUAL_ENGINE_SOURCE_PATH')
 return observed
def n(v):
 # Builder emits exact decimals; floats/bool and arbitrary rational wire strings are not accepted.
 require(type(v) is str and re.fullmatch(r'[0-9]+(?:[.][0-9]+)?|[.][0-9]+',v) is not None,'RECTANGLE_TOKEN')
 return Q(v)
def rectangle(r):
 require(type(r) is list and len(r)==4,'RECTANGLE_SHAPE')
 x,y,X,Y=map(n,r);require(x<X and y<Y,'RECTANGLE_EXTENT')
 return x,y,X,Y
def intersect(a,b):
 r=(max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3]))
 return r if r[0]<r[2] and r[1]<r[3] else None
def union_area(rects):
 """Exact 1-D y interval merges in each strip of the x arrangement."""
 if not rects:return Q()
 xs=sorted({x for r in rects for x in (r[0],r[2])})
 area=Q()
 for left,right in zip(xs,xs[1:]):
  intervals=sorted((y,Y) for x,y,X,Y in rects if x<=left<right<=X)
  start=end=None
  for lo,hi in intervals:
   if end is None:start,end=lo,hi
   elif lo>end:area+=(right-left)*(end-start);start,end=lo,hi
   else:end=max(end,hi)
  if end is not None:area+=(right-left)*(end-start)
 return area
def overlap_area(a,b):
 return union_area([z for x in a for y in b if (z:=intersect(x,y)) is not None])
def fixed_deductions(core,W,L):
 """Pre-construction analogue of exact fixed wall/common factory in assemble114 only."""
 require(type(core) is dict and set(core)==CORE_FIELDS and core['kind']==CORE_KIND,'FIXED_CORE_PROFILE_NOT_DOCUMENTED')
 a=Q('.25');t=Q('.15')
 band=rectangle(core['band']);y,Y=band[1],band[3]
 c,C=map(n,core['core_extent_x']); low,high=map(n,core['outside_band_unit_separator_y'])
 require(a<=c<C<=W-a and a<y<low<high<Y<L-a,'COMPACT_SOURCE_BOUNDARY')
 stair=rectangle(core['stair']);lift=rectangle(core['lift'])
 require(type(core['lobby']) is list and len(core['lobby'])==2,'COMMON_SPACE_INVENTORY')
 common=[stair,lift,*map(rectangle,core['lobby'])]
 require(type(core['entry_centers']) is dict and set(core['entry_centers'])=={'A','B'},'ENTRY_INVENTORY')
 require(all(type(v) is list and len(v)==2 for v in core['entry_centers'].values()),'ENTRY_SHAPE')
 ex=n(core['entry_centers']['A'][0]);left,right=ex-Q('.65'),ex+Q('.65')
 require(c<left<right<C and n(core['entry_centers']['B'][0])==ex,'ENTRY_APERTURE_BOUNDARY')
 wall={'perimeter.left':(Q(),Q(),a,L),'perimeter.right':(W-a,Q(),W,L),
       'perimeter.front':(a,Q(),W-a,a),'perimeter.back':(a,L-a,W-a,L),
       'core.lobby.outer_right':(C-t,y,C,Y)}
 for uid,lo,hi in (('A',y-t,y),('B',Y,Y+t)):
  wall[uid+'.boundary.left']=(c,lo,left,hi)
  wall[uid+'.boundary.right']=(right,lo,C,hi)
 for side,x,X in (('left',a,c),('right',C,W-a)):
  if x<X:wall['wing_separator.'+side]=(x,low,X,high)
 for name,(x,b,X,B),side,width in (('stair',stair,'right',Q('.9')),('lift',lift,'left',Q('1.1'))):
  cy=(b+B)/2;d,e=cy-width/2,cy+width/2
  wall[name+'.bottom']=(x,b-t,X,b);wall[name+'.top']=(x,B,X,B+t)
  for k,l,r in (('left',x-t,x),('right',X,X+t)):
   if k!=side:wall[name+'.'+k]=(l,b-t,r,B+t)
   else:
    wall[name+'.'+k+'.lower']=(l,b-t,r,d);wall[name+'.'+k+'.upper']=(l,e,r,B+t)
 plot=(Q(),Q(),W,L)
 require(all(z[0]<z[2] and z[1]<z[3] and intersect(z,plot)==z for z in [*wall.values(),*common]),'FIXED_DEDUCTION_OUTSIDE_FRAME')
 return common,wall
def ownership_metrics(core,W,L):
 """Maximum geometrically available ownership after known fixed exclusions, not usable area."""
 require(type(core) is dict and type(core.get('unit_ownership')) is dict and set(core['unit_ownership'])=={'A','B'},'OWNERSHIP_REQUIRED')
 require(type(core.get('units')) is dict and set(core['units'])=={'A','B'},'SOURCE_BOX_INVENTORY')
 common,walls=fixed_deductions(core,W,L);plot=(Q(),Q(),W,L)
 owners={}
 for uid,rows in core['unit_ownership'].items():
  require(type(rows) is list and rows,'OWNERSHIP_PARTS_REQUIRED')
  owners[uid]=[rectangle(z) for z in rows]
  require(all(intersect(z,plot)==z for z in owners[uid]),'OWNERSHIP_OUTSIDE_PLOT')
 require(overlap_area(owners['A'],owners['B'])==0,'CROSS_UNIT_OWNERSHIP_OVERLAP')
 result={}
 for uid,parts in owners.items():
  base=rectangle(core['units'][uid]);gross=union_area(parts)
  require(overlap_area([base],parts)==union_area([base]),'SOURCE_BOX_NOT_OWNED')
  fixed=overlap_area(parts,[*common,*walls.values()])
  width,depth=base[2]-base[0],base[3]-base[1]
  result[uid]={'owned_union_m2':str(gross),'fixed_core_overlap_m2':str(overlap_area(parts,common)),
   'fixed_wall_overlap_m2':str(overlap_area(parts,list(walls.values()))),'fixed_union_overlap_m2':str(fixed),
   'geometric_area_after_known_fixed_deductions_m2':str(gross-fixed),'historical_source_box_m2':str(width*depth),
   'source_box_width_m':str(width),'source_box_depth_m':str(depth)}
 return result,sorted(walls)
def lower_bound(profile):
 beds=profile['bedrooms_per_unit'];roles=profile['sleep_roles']
 require(type(beds) is int and beds in (1,2) and roles==['double']+['twin']*(beds-1),'PROGRAMME_PROFILE_NOT_READY')
 result=[]
 for role in (*roles,'bath','kitchen','dining'):
  w,h=MINIMA[role]
  result.append({'role':role,'module':MODULE_SOURCES[role],'minimum_width_m':w,'minimum_depth_m':h,
                 'minimum_disjoint_search_rectangle_m2':str(Q(w)*Q(h))})
 return result,sum((Q(r['minimum_disjoint_search_rectangle_m2']) for r in result),Q())
def inspect_request(body,programme='PROGRAM_2BED_V1'):
 envelope=parse_public(body);verify_public(body,envelope)
 result={'schema':'P05_NET_CAPACITY_DIAGNOSTIC_V1','state':'PROFILE_NOT_READY','input_valid':True,
   'request_digest':envelope['canonical_request_digest'],'transport_body_sha256':envelope['transport_body_sha256'],
   'programme':programme,'independent_geometry_not_placement_proof':True,'global_infeasibility_proven':False,
   'dispatch_authorized':False,'fit_verified':False,**AUTH}
 if envelope['canonical_request']['unit_count']!=2:
  result['reason']='ONLY_COMPACT_FRONT_REAR_N2_DIAGNOSTIC';return result
 try:
  before=source_guard()
  require(type(programme) is str and programme in ('PROGRAM_1BED_V1','PROGRAM_2BED_V1'),'PROGRAMME_PROFILE_NOT_READY')
  profile=lookup(programme)
  require(profile['approval']['status']=='APPROVED_DESIGN_PROGRAM','PROGRAMME_PROFILE_NOT_READY')
  try:p=prepare_core(CORE_ENTRY,body)
  except ValueError as ex:
   require(str(ex)!='CURRENT_CORE_METHOD_NO_FIT_NOT_INFEASIBLE','CURRENT_CORE_METHOD_NO_FIT_NOT_INFEASIBLE')
   raise
  require(digest(p['envelope'])==digest(envelope),'REQUEST_ENVELOPE_BINDING')
  core,raw=p['core'],p['raw'];W,L=map(Q,(raw['W'],raw['L']))
  source_metrics,wall_keys=ownership_metrics(core,W,L)
  import contract114
  require(Path(inspect.getsourcefile(contract114.program)).resolve()==ENGINE/'contract114.py','HISTORICAL_SOURCE_PATH')
  old=contract114.program(W,L,core,raw)
  import capacity_program118
  historical_bound=int(Q(source_metrics['A']['historical_source_box_m2'])/(Q('5.45')*Q('3.6')))
  try:
   old_source=capacity_program118.proposed_program(core,raw)
   require(old_source['necessary_module_area_bound']==historical_bound,'HISTORICAL_MODULE_BOUND_MISMATCH')
   historical_status='PROGRAMME_CHOICES_RECORDED';historical_choices=old_source['bedroom_choices']
  except ValueError as ex:
   if str(ex)!='CURRENT_MODULE_PROGRAM_BOUND_EMPTY_NOT_GLOBAL_INFEASIBILITY':raise
   require(historical_bound==0,'HISTORICAL_MODULE_BOUND_MISMATCH')
   historical_status=str(ex);historical_choices=[]
  modules,minimum=lower_bound(profile)
  for row in source_metrics.values():
   row['geometric_area_comparison']='BELOW_SOURCE_MODULE_AREA_BOUND' if Q(row['geometric_area_after_known_fixed_deductions_m2'])<minimum else 'AREA_NOT_BELOW_BOUND_NOT_FIT'
   row['geometric_double_bedroom_area_quotient_not_count']=int(Q(row['geometric_area_after_known_fixed_deductions_m2'])/Q('19.62'))
   row['source_box_comparison']='BELOW_SOURCE_MODULE_AREA_BOUND' if Q(row['historical_source_box_m2'])<minimum else 'AREA_NOT_BELOW_BOUND_NOT_FIT'
   row['modules_not_fitting_source_box_dimensions']=[r['role'] for r in modules if
     Q(r['minimum_width_m'])>Q(row['source_box_width_m']) or Q(r['minimum_depth_m'])>Q(row['source_box_depth_m'])]
  require(source_guard()==before,'SOURCE_CHANGED_DURING_OBSERVATION')
  result.update(state='MEASURED_SCOPED_NO_FIT_CLAIM',family='FRONT_REAR',core_method=CORE_KIND,
    dimensions_m={'W':raw['W'],'L':raw['L']},per_unit=source_metrics,
    core_digest=digest(core),programme_digest=digest(profile),sources=before,
    derived_fixed_wall_piece_ids=wall_keys,known_common_space_ids=['stair','lift','lobby'],
    fixed_overlap_policy='Wall/core overlap columns can overlap; only their combined union intersection is subtracted once. Piece labels are analytic, not assembled wall IDs.',
    excluded_from_deductions=['UNBUILT_MODULE_PARTITIONS','UNBUILT_FIXTURES','UNVERIFIED_CIRCULATION_QUALITY'],
    historical={'source':'frozen contract114.program: initial box-only floor(area/55), cap1–4',
      'basis':old['basis'],'bedroom_choices':old['bedroom_choices'],'meaning':'Historical provisional ordering only; not an owner rule or search result'},
    historical_module_bound={'source':'frozen capacity_program118.proposed_program: floor(box area/19.62)',
      'bound':historical_bound,'state':historical_status,'bedroom_choices':historical_choices,
      'scope':'Pure historical prefilter recomputation only, not a rerun of engine114 or a present programme decision'},
    module_bounds=modules,necessary_disjoint_module_area_m2=str(minimum),
    lower_bound_scope='Selected frozen search rectangles only. Omits furniture-use, access and spacing. No source-wide minimum or quality threshold.')
 except MissingEvidence as ex:result['reason']=str(ex)
 except (ValueError,TypeError,KeyError,OSError,ZeroDivisionError):result['reason']='SOURCE_EVIDENCE_INCOMPLETE'
 return result
# Same-request HTTP observation only. Never consulted for dispatch or admission.
HTTP_SCHEMA='P05_HTTP_PREFLIGHT_OBSERVATION_V1'
HTTP_AREAS=('owned_union_m2','fixed_union_overlap_m2','geometric_area_after_known_fixed_deductions_m2',
 'historical_source_box_m2','source_box_width_m','source_box_depth_m')
HTTP_COMPARE=('BELOW_SOURCE_MODULE_AREA_BOUND','AREA_NOT_BELOW_BOUND_NOT_FIT')
HTTP_REASONS={'SOURCE_FILE_REQUIRED','SOURCE_PIN_CHANGED','ACTUAL_SOURCE_PATH','ACTUAL_ENGINE_SOURCE_PATH',
 'SOURCE_CHANGED_DURING_OBSERVATION','SOURCE_EVIDENCE_INCOMPLETE','CURRENT_CORE_METHOD_NO_FIT_NOT_INFEASIBILITY'}
def http_unknown(body):
 return {'schema':HTTP_SCHEMA,'state':'PROFILE_NOT_READY','request_digest':hashlib.sha256(body).hexdigest(),
  'reason':'CAPACITY_OBSERVATION_UNVERIFIED','programme':'PROGRAM_2BED_V1','fit_verified':False,'dispatch_authorized':False,**AUTH}
def freeze_http(value):
 data=json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
 return data,hashlib.sha256(data).hexdigest()
def capture_http(body,envelope):
 """Freeze only safe fields. Preserve an unknown without changing the main result."""
 base=http_unknown(body)
 try:
  checked=verify_public(body,envelope)
  require(checked['canonical_request']['unit_count']==2,'HTTP_N2_ONLY')
  r=inspect_request(body);scope=r.get('state')
  require(r.get('schema')=='P05_NET_CAPACITY_DIAGNOSTIC_V1' and r.get('input_valid') is True
   and r.get('programme')=='PROGRAM_2BED_V1' and r.get('dispatch_authorized') is False
   and r.get('fit_verified') is False and all(r.get(k) is False for k in AUTH)
   and r['transport_body_sha256']==base['request_digest'] and r['request_digest']==checked['canonical_request_digest'],'HTTP_CAPACITY_BINDING')
  if scope=='PROFILE_NOT_READY':
   if r.get('reason') in HTTP_REASONS:base['reason']=r['reason']
  elif scope=='MEASURED_SCOPED_NO_FIT_CLAIM':
   source=source_guard()
   require(digest(source)==digest(r['sources']) and r['family']=='FRONT_REAR' and r['core_method']==CORE_KIND,'HTTP_CAPACITY_SOURCE')
   require(set(r['per_unit'])=={'A','B'},'HTTP_CAPACITY_UNITS')
   per={}
   for uid,row in r['per_unit'].items():
    v={k:row[k] for k in HTTP_AREAS}
    require(all(type(z) is str and len(z)<=256 and re.fullmatch(r'[0-9]+(?:/[1-9][0-9]*)?',z) for z in v.values()),'HTTP_CAPACITY_RATIO')
    for k in ('geometric_area_comparison','source_box_comparison'):
     require(row[k] in HTTP_COMPARE,'HTTP_CAPACITY_COMPARISON');v[k]=row[k]
    q=row['geometric_double_bedroom_area_quotient_not_count']
    require(type(q) is int and 0<=q<=100,'HTTP_CAPACITY_QUOTIENT')
    v['geometric_double_bedroom_area_quotient_not_count']=q
    roles=row['modules_not_fitting_source_box_dimensions']
    require(type(roles) is list and len(set(roles))==len(roles) and set(roles)<=set(MINIMA),'HTTP_CAPACITY_ROLES')
    v['modules_not_fitting_source_box_dimensions']=list(roles)
    require(Q(v['owned_union_m2'])-Q(v['fixed_union_overlap_m2'])==Q(v['geometric_area_after_known_fixed_deductions_m2']),'HTTP_CAPACITY_DEDUCTION')
    per[uid]=v
   bound=r['historical_module_bound']['bound'];minimum=r['necessary_disjoint_module_area_m2']
   require(type(bound) is int and bound==int(Q(per['A']['historical_source_box_m2'])/Q('19.62')),'HTTP_CAPACITY_HISTORICAL_BOUND')
   require(type(minimum) is str and Q(minimum)==Q('69.25'),'HTTP_CAPACITY_P2_BOUND')
   require(all(type(r[k]) is str and re.fullmatch('[a-f0-9]{64}',r[k]) for k in ('core_digest','programme_digest')),'HTTP_CAPACITY_SHA')
   base.pop('reason')
   base.update(state=scope,canonical_input_digest=r['request_digest'],source_digest=digest(source),core_digest=r['core_digest'],
    programme_digest=r['programme_digest'],family='FRONT_REAR',core_method=CORE_KIND,per_unit=per,
    historical_module_area_bound=bound,necessary_disjoint_module_area_m2=minimum)
  else:raise MissingEvidence('HTTP_CAPACITY_STATE')
 except Exception:
  base=http_unknown(body)
 return freeze_http(base)
def attach_http(summary,body,frozen,expected_canonical=None):
 """Check the frozen advisory record against this request without changing existing keys."""
 try:
  data,h=frozen
  require(type(data) is bytes and len(data)<=12000 and hashlib.sha256(data).hexdigest()==h,'HTTP_CAPACITY_SNAPSHOT')
  payload=json.loads(data)
  require(payload.get('schema')==HTTP_SCHEMA and payload.get('request_digest')==hashlib.sha256(body).hexdigest()
   and payload.get('dispatch_authorized') is False and payload.get('fit_verified') is False
   and all(payload.get(k) is False for k in AUTH),'HTTP_CAPACITY_REQUEST_BINDING')
  common=set(http_unknown(body))
  if payload.get('state')=='MEASURED_SCOPED_NO_FIT_CLAIM':
   measured={'canonical_input_digest','source_digest','core_digest','programme_digest','family','core_method',
    'per_unit','historical_module_area_bound','necessary_disjoint_module_area_m2'}
   require(set(payload)==(common-{'reason'})|measured and payload['programme']=='PROGRAM_2BED_V1','HTTP_CAPACITY_KEYS')
   per=payload['per_unit'];row_keys=set(HTTP_AREAS)|{'geometric_area_comparison','source_box_comparison',
    'geometric_double_bedroom_area_quotient_not_count','modules_not_fitting_source_box_dimensions'}
   require(set(per)=={'A','B'} and all(set(row)==row_keys for row in per.values()),'HTTP_CAPACITY_NESTED_KEYS')
   require(all(type(payload[k]) is str and re.fullmatch('[a-f0-9]{64}',payload[k]) for k in
    ('canonical_input_digest','source_digest','core_digest','programme_digest')),'HTTP_CAPACITY_SHA_AT_PROJECTION')
   require(expected_canonical is None or payload['canonical_input_digest']==expected_canonical,'HTTP_CAPACITY_CANONICAL')
   require(payload['family']=='FRONT_REAR' and payload['core_method']==CORE_KIND
    and payload['necessary_disjoint_module_area_m2']=='277/4'
    and type(payload['historical_module_area_bound']) is int and 0<=payload['historical_module_area_bound']<=100,'HTTP_CAPACITY_SCOPE')
   for row in per.values():
    require(all(type(row[k]) is str and len(row[k])<=256 and re.fullmatch(r'[0-9]+(?:/[1-9][0-9]*)?',row[k]) for k in HTTP_AREAS),'HTTP_CAPACITY_RATIO_AT_PROJECTION')
    require(all(row[k] in HTTP_COMPARE for k in ('geometric_area_comparison','source_box_comparison')),'HTTP_CAPACITY_COMPARE_AT_PROJECTION')
    q=row['geometric_double_bedroom_area_quotient_not_count'];roles=row['modules_not_fitting_source_box_dimensions']
    require(type(q) is int and 0<=q<=100 and type(roles) is list and len(roles)<=5 and set(roles)<=set(MINIMA),'HTTP_CAPACITY_ROW_AT_PROJECTION')
    net=Q(row['geometric_area_after_known_fixed_deductions_m2']);box=Q(row['historical_source_box_m2'])
    require(Q(row['owned_union_m2'])-Q(row['fixed_union_overlap_m2'])==net
     and Q(row['source_box_width_m'])*Q(row['source_box_depth_m'])==box and q==int(net/Q('19.62')),'HTTP_CAPACITY_ARITHMETIC')
    for k,metric in (('geometric_area_comparison',net),('source_box_comparison',box)):
     require(row[k]==HTTP_COMPARE[int(metric>=Q('69.25'))],'HTTP_CAPACITY_COMPARISON_ARITHMETIC')
   require(payload['historical_module_area_bound']==int(Q(per['A']['historical_source_box_m2'])/Q('19.62')),'HTTP_CAPACITY_HISTORICAL_ARITHMETIC')
   require(payload['source_digest']==digest(source_guard()),'HTTP_CAPACITY_SOURCE_AT_PROJECTION')
  else:
   require(payload.get('state')=='PROFILE_NOT_READY' and set(payload)==common and payload['programme']=='PROGRAM_2BED_V1'
    and payload['reason'] in HTTP_REASONS|{'CAPACITY_OBSERVATION_UNVERIFIED'},'HTTP_CAPACITY_STATE')
 except Exception:
  payload=http_unknown(body);_,h=freeze_http(payload)
 return {**summary,'capacity_observation':{**payload,'observation_digest':h}}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--programme',default='PROGRAM_2BED_V1')
 parser.add_argument('--body',required=True,help='Exact public JSON body; decimal dimensions must be strings')
 args=parser.parse_args()
 print(json.dumps(inspect_request(args.body.encode(),args.programme),sort_keys=True,allow_nan=False))
