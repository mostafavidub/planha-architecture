"""Independent declarative geometry projection study, not a world-model schema.
No extraction/solver/admission: callers must separately establish source completeness.
Points use affine translation; direction/offset vectors do not. Embedded modules,
ledgers, semantic ownership, operation scenarios and physical validity are outside.
"""
import copy,hashlib,json,re
from fractions import Fraction as F
from decimal import Decimal,localcontext
SCHEMA='DECLARED_GEOMETRY_PROJECTION_V1'
POINT_FIELDS='hand_point hand_start hand_end center hinge closed_actor open_actor open_access shelf_target held_target grip_closed grip_open storage_target workpoint access_point point target actor hand'.split()
VECTOR_FIELDS='translation actor_offset_m normal front_normal'.split()
RECT_FIELDS='rect plan_rect closed_panel open_panel pocket rail_envelope panel_rect actor_rect actor_start actor_end closed_rect open_rect occupied_body standing_body closed_tray open_tray body_rect front_rect region'.split()
PATH_FIELDS='path egress_route route open_transfer_points'.split()
FIELD_ROLES={'walls':'rectangle','wall_hosts':'rectangle','source_wall_hosts':'rectangle','openings.rect':'rectangle','module_placements.transform':'placement','units.dining_module_placement.transform':'placement','units.routes':'path','units.scenario_routes':'path','common_routes':'path','units.route_targets':'point','units.entry_point':'point'}
FIELD_ROLES.update({'operations.'+k:'point' for k in POINT_FIELDS})
FIELD_ROLES.update({'operations.'+k:'vector' for k in VECTOR_FIELDS})
FIELD_ROLES.update({'operations.'+k:'rectangle' for k in RECT_FIELDS})
FIELD_ROLES.update({'operations.'+k:'path' for k in PATH_FIELDS})
FIELD_ROLES.update({'operations.'+k:'canonical' for k in ('canonical_isometry','canonical_transform')})
CONTRACT={'schema':SCHEMA,'root_fields':['schema','units','records'],
 'record_fields':['unit_id','id','source_field','value'],
 'field_roles':FIELD_ROLES,'unit_namespace':['A','B','COMMON'],
 'required_roles':['rectangle','point','vector','path','placement','canonical'],
 'coordinate_type':'canonical finite decimal string; no float/int/bool/tuple',
 'identity':'unique (unit_id,id), same local ID in A and B is permitted',
 'source_completeness':'NOT_CHECKED; source_field is a declared role, not authenticated pointer',
 'frame_semantics':{'placement':'source module coordinates -> current world coordinates; new placement = T composed with P','canonical':'current world coordinates -> fixed canonical module coordinates; new canonical = C composed with inverse(T)','point':'world position, receives affine translation','vector':'world direction or displacement, no affine translation'},
 'producer_scope':'Historical producer125 only supports zero-translation swapXY. General D4 here is a projection study, not producer compatibility.',
 'accepted':False,'qualified':False,'delivery_allowed':False}
def require(ok,code):
 if not ok:raise ValueError(code)
def digest(v):
 return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def scalar_text(v):
 with localcontext() as c:
  c.prec=max(80,len(str(v.numerator))+len(str(v.denominator))+5)
  s=format(Decimal(v.numerator)/Decimal(v.denominator),'f')
 return (s.rstrip('0').rstrip('.') if '.' in s else s) if v else '0'
def number(v):
 require(type(v)is str and len(v)<=128 and re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?',v) is not None,'DECIMAL_TYPE')
 f=F(v);require(scalar_text(f)==v,'DECIMAL_CANONICAL');return f
def keys(v,names,reason):
 require(type(v)is dict and set(v)==set(names) and all(type(k)is str for k in v),reason)
def point(v):
 require(type(v)is list and len(v)==2,'POINT_SHAPE');return list(map(number,v))
def matrix(a):
 require(type(a)is list and len(a)==2 and all(type(r)is list and len(r)==2 and all(type(x)is int and x in(-1,0,1) for x in r) for r in a),'MATRIX_TYPE')
 require(all(sum(a[k][i]*a[k][j] for k in range(2))==int(i==j) for i in range(2) for j in range(2)),'MATRIX_NOT_SIGNED_PERMUTATION')
 return a
def iso(t):
 keys(t,['matrix','translation'],'ISOMETRY_FIELDS');matrix(t['matrix']);point(t['translation']);return t
def rect(v):
 require(type(v)is list and len(v)==4,'RECT_SHAPE');q=list(map(number,v))
 require(q[0]<q[2] and q[1]<q[3],'RECT_EXTENT');return q
def identifier(v):
 require(type(v)is str and re.fullmatch(r'[A-Za-z][A-Za-z0-9_.:-]{0,95}',v) is not None,'IDENTIFIER')
def validate(v):
 keys(v,CONTRACT['root_fields'],'ROOT_FIELDS');require(v['schema']==SCHEMA and type(v['schema'])is str,'SCHEMA')
 require(type(v['units'])is list and v['units']==['A','B'] and all(type(x)is str for x in v['units']),'UNIT_IDENTITY')
 require(type(v['records'])is list and 1<=len(v['records'])<=10000,'RECORDS')
 seen=set();roles=set()
 for r in v['records']:
  keys(r,CONTRACT['record_fields'],'RECORD_FIELDS');identifier(r['id'])
  require(type(r['unit_id'])is str and r['unit_id'] in CONTRACT['unit_namespace'],'UNIT_REFERENCE')
  key=(r['unit_id'],r['id']);require(key not in seen,'DUPLICATE_UNIT_INSTANCE');seen.add(key)
  require(type(r['source_field'])is str and r['source_field'] in FIELD_ROLES,'UNDECLARED_SOURCE_FIELD')
  role=FIELD_ROLES[r['source_field']];roles.add(role);q=r['value']
  if role=='rectangle':rect(q)
  elif role in ('point','vector'):point(q)
  elif role=='path':
   require(type(q)is list and 2<=len(q)<=10000,'PATH_SHAPE')
   for p in q:point(p)
  else:iso(q)
 require(set(CONTRACT['required_roles'])<=roles,'PROJECTION_ROLE_COVERAGE')
 return True
def mul(a,b):
 return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mv(a,v):
 return [sum(a[i][k]*v[k] for k in range(2)) for i in range(2)]
def inverse(t):
 iso(t);a=t['matrix'];b=[[a[j][i] for j in range(2)] for i in range(2)]
 return {'matrix':b,'translation':[scalar_text(-x) for x in mv(b,point(t['translation']))]}
def compose(t,p):
 iso(t);iso(p);a=t['matrix'];x=mv(a,point(p['translation']));y=point(t['translation'])
 return {'matrix':mul(a,p['matrix']),'translation':[scalar_text(x[i]+y[i]) for i in range(2)]}
def transform(v,t):
 validate(v);iso(t);before=digest(v);out=copy.deepcopy(v);a=t['matrix'];shift=point(t['translation'])
 def pt(q,vector=False):
  z=mv(a,point(q));return [scalar_text(z[i]+(0 if vector else shift[i])) for i in range(2)]
 for r in out['records']:
  role=FIELD_ROLES[r['source_field']];q=r['value']
  if role=='rectangle':
   x,y,X,Y=rect(q);corners=[pt([scalar_text(u),scalar_text(w)]) for u,w in ((x,y),(x,Y),(X,y),(X,Y))]
   axes=list(zip(*[[F(n) for n in p] for p in corners]))
   r['value']=[scalar_text(min(axes[0])),scalar_text(min(axes[1])),scalar_text(max(axes[0])),scalar_text(max(axes[1]))]
  elif role in ('point','vector'):r['value']=pt(q,role=='vector')
  elif role=='path':r['value']=[pt(p) for p in q]
  elif role=='placement':r['value']=compose(t,q)
  else:r['value']=compose(q,inverse(t))
 validate(out);require(digest(v)==before,'INPUT_MUTATED');return out
def check(v):
 try:
  validate(v)
  return {'state':'DECLARED_PROJECTION_VALID_ONLY','projection_digest':digest(v),'contract_digest':digest(CONTRACT),'source_completeness_verified':False,'physical_verified':False,'accepted':False,'qualified':False,'delivery_allowed':False}
 except (ValueError,TypeError,KeyError,UnicodeError,OverflowError,RecursionError) as ex:
  return {'state':'INVALID_DECLARED_PROJECTION','error_type':type(ex).__name__,'accepted':False,'qualified':False,'delivery_allowed':False}
