"""362 exact source geometry adapter; callable only after SOURCE_BALANCED365 artifact gate."""
import ast,types,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect
ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'staging365_balanced_portals';SRC=ROOT/'planha_general150_runtime_work'
def load_origin(record):
 trace=record['trace'];c=record['candidate'];m=c['model']
 from gate385 import load_inputs,validate
 validate(record,load_inputs()['fresh'])
 for name,sha in trace['source_inventory'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_BALANCED365_ORIGIN_SOURCE_DRIFT')
 return c,m,trace

def base(record):
 c,m,t=load_origin(record);path=HERE/'assemble365.py';data=path.read_bytes();tree=ast.parse(data);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='assemble');stop=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='uid'and any(isinstance(x,ast.FunctionDef)and x.name=='tr'for x in n.body));fn.body=fn.body[:stop]+[ast.Return(value=ast.Name(id='m',ctx=ast.Load()))];mod=types.ModuleType('_prefix365');mod.__file__=str(path);sys.path.insert(0,str(SRC));sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'staging362_core_notch'));exec(compile(ast.fix_missing_locations(tree),str(path),'exec'),mod.__dict__)
 raw=c['request'];out=mod.assemble(F(raw['W']),F(raw['L']),c['packet']['core'],t['proposal'])
 notch_path=ROOT/'staging362_core_notch/notch_frame362.py';notch_code=notch_path.read_bytes();key=str(notch_path.relative_to(ROOT))
 if t['source_inventory'].get(key)!=hashlib.sha256(notch_code).hexdigest():raise ValueError('NOTCH_FRAME_SOURCE_PIN')
 ns={};exec(compile(notch_code,str(notch_path),'exec'),ns);expected=ns['outer_right'](c['packet']['core'],F('.15'))
 if rect(out['wall_hosts']['core.lobby.outer_right'])!=tuple(expected) or rect(m['wall_hosts']['core.lobby.outer_right'])!=tuple(expected):raise ValueError('NOTCH_FRAME_EXACT_SOURCE_PREDICATE')
 return out,{'file':'staging365_balanced_portals/assemble365.py','sha256':hashlib.sha256(data).hexdigest(),'selector':'Executed source362 prefix before unit module installs; exact notch_frame362.outer_right source predicate with same-model core', 'notch_frame_source_sha256':hashlib.sha256(notch_code).hexdigest(), 'notch_frame_expected':list(map(str,expected))}

def hall(record):
 c,m,t=load_origin(record);sys.path.insert(0,str(SRC));sys.path.insert(0,str(HERE))
 sys.path.insert(0,str(ROOT/'staging359_hall_clamp'))
 from clamp_geometry359 import clamp
 from operation_reservations359 import extract
 proposal=t['proposal'];beds=[rect(proposal['rectangles']['bed'+str(i)])for i in (1,2,3)];L=F(c['request']['L']);thick=F('.15');rear=max(q[3]for q in beds)+thick;front=beds[0][1];back=rear+1;cx=F(proposal['ordered_macro']['private_interface_center_x']);half=F('.55');out={'walls':{},'wall_hosts':{}}
 for u in m['units']:
  uid=u['id'];source=[x for x in m['source_hall_clamp359']if x['unit']==uid]
  if len(source)!=1:raise ValueError('SOURCE_CLAMP_INVENTORY')
  source=source[0]
  def localrect(r):
   a,b,c,d=rect(r);return (a,b,c,d)if uid=='A'else(a,L-d,c,L-b)
  def tr(r):
   a,b,c,d=map(F,r);return list(map(str,(a,b,c,d)if uid=='A'else(a,L-d,c,L-b)))
  paths={k:[[F(p[0]),F(p[1])if uid=='A'else L-F(p[1])]for p in v]for k,v in source['original_required_paths'].items()}
  if set(paths)!={uid+'.bed'+str(i)for i in (1,2,3)}:raise ValueError('SOURCE_REQUIRED_BED_PORTS')
  ops={k:localrect(r)for k,r in extract(m['operations'],m['profile']['body_m']).items()};ops.update({'activity/'+k:localrect(r)for k,r in u['activities'].items()});connectors=[[a[2]+thick,front,b[0]-thick,rear]for a,b in zip(beds,beds[1:])];ds=[d for d in m['private_domains']if d['unit']==uid]
  if len(ds)!=1:raise ValueError('PRIVATE_DOMAIN_INVENTORY')
  cl=clamp([beds[0][0],rear,beds[-1][2],back],connectors,localrect(ds[0]['public_interface']['rect']),paths,ops,m['profile']['body_m'])
  if rect(cl['hall'])!=rect(source['proof']['hall']):raise ValueError('RECOMPUTED_SOURCE_CLAMP_GEOMETRY')
  left,_,right,_=map(F,cl['hall']);wallrects={'left_return':[left-thick,rear,left,back+thick],'right_return':[right,rear,right+thick,back+thick],'back_left':[left,back,cx-half,back+thick],'back_right':[cx+half,back,right,back+thick]}
  for k,q in wallrects.items():
   wid=uid+'.private_hall.'+k;out['walls'][wid]=tr(q);out['wall_hosts'][wid]=tr(q)
   if rect(m['walls'][wid])!=rect(tr(q))or rect(m['wall_hosts'][wid])!=rect(tr(q)):raise ValueError('REBUILT_HALL_GEOMETRY')
 return out,{'file':'staging359_hall_clamp/private_hall_producer359.py','source_inventory_digest':digest(t['source_inventory']),'selector':'Exact source clamp from same-model source ports/original paths/actual all operation+activity reservations, then source wall formula','not_necessity_proof':True}
