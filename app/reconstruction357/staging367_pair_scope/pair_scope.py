"""One fixed source-bound organization pair; no qualified output selection."""
import json,hashlib,types,builtins
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parent;ROOT=P.parent

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def validate_member(record,result,pins):
 c=record['candidate'];m=c['model'];p=result['provenance'];t=record['trace']
 if digest(record)!=pins['record_digest']or digest(result)!=pins['result_digest']:raise ValueError('FIXED_MEMBER_ARTIFACT')
 if t['schema']!=pins['trace_schema']or result['schema']!=pins['result_schema']:raise ValueError('SOURCE_PROFILE')
 h=digest(m)
 if h!=pins['model_digest']or c['model_digest']!=h or digest(c['packet']['world_model'])!=h:raise ValueError('CURRENT_MODEL')
 if digest(c)!=p['candidate_digest']or digest(c['packet'])!=p['packet_digest']or p['model_hash']!=h:raise ValueError('PROVENANCE_PACKET')
 if p['input_record_digest']!=digest(record)or p['outer_trace_digest']!=digest(t)or result['input_record_digest']!=digest(record)or result['outer_trace_digest']!=digest(t):raise ValueError('CURRENT_RECORD_TRACE')
 raw=c['request']
 if digest(raw)!=c['request_digest']or digest(p['raw'])!=digest(raw):raise ValueError('CURRENT_REQUEST')
 if t['schema']=='SOURCE_SERVICE_JOINT367_TRACE_V1':
  if set(raw)!={'W','L','n','requested_count'} or any(type(raw[k])is not type(v)or raw[k]!=v for k,v in {'W':'26','L':'28','n':2,'requested_count':2}.items()):raise ValueError('JOINT_FIXED_REQUEST')
  if list(map(F,m['inputs']))!=[F(raw[k])for k in ('W','L','n')]:raise ValueError('JOINT_REQUEST_MODEL')
  if p['schema']!=t['schema']or p['parent_record_digest']!=t['parent_record_digest']:raise ValueError('JOINT_PARENT_SOURCE')
  if digest(p['ordered_stages'])!=digest(t['stages']):raise ValueError('JOINT_ORDERED_REPLAY')
 elif t['schema']=='ROW_BALANCED_PORTALS365_SOURCE_TRACE_V1':
  if digest(raw)!=digest(t['raw']):raise ValueError('BALANCED_TRACE_REQUEST')
 else:raise ValueError('UNSUPPORTED_PAIR_SOURCE')
 if result['raw_report']['model_hash']!=h:raise ValueError('RAW_MODEL')
 return m

def canonical_signature(v):
 if type(v)is not list or len(v)!=2:raise ValueError('TWO_UNIT_SIGNATURE')
 out=[]
 for row in v:
  if type(row)is not list or len(row)!=3 or any(type(x)not in(int,F)or x not in(-1,0,1)for x in row):raise ValueError('DIRECTION_DOT_DOMAIN')
  out.append((int(row[0]),*sorted(map(int,row[1:]))))
 return tuple(sorted(out))

def evaluate():
 pins=json.loads((P/'pins.json').read_text())
 def check():
  for n,h in pins['sources'].items():
   if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_CHANGED:'+n)
 check();loaded={};rt=ROOT/'planha_general150_runtime_work'
 def load(name):
  if name in loaded:return loaded[name]
  path=rt/(name+'.py');data=path.read_bytes()
  if hashlib.sha256(data).hexdigest()!=pins['sources'].get(str(path.relative_to(ROOT))):raise ValueError('UNPINNED_ACTIVE_SOURCE')
  m=types.ModuleType('_pair367_'+name);m.__file__=str(path);loaded[name]=m
  def imp(n,g=None,l=None,fromlist=(),level=0):
   if level==0 and (rt/(n+'.py')).exists():return load(n)
   return builtins.__import__(n,g,l,fromlist,level)
  m.__dict__['__builtins__']={**vars(builtins),'__import__':imp};exec(compile(data,str(path),'exec'),m.__dict__);return m
 algorithm=load('three_access_diversity133').access_signature;members=[];models=[]
 for key,p in pins['members'].items():
  record=json.loads((ROOT/p['record_path']).read_text());result=json.loads((ROOT/p['result_path']).read_text());m=validate_member(record,result,p)
  for n,h in result['expected_method_registry']['sources'].items():
   if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('MEMBER_SOURCE_CHANGED:'+n)
  a=algorithm(m);sig=canonical_signature(a['signature']);models.append(m)
  members.append({'member':key,'record_digest':digest(record),'fresh_result_digest':digest(result),'model_digest':digest(m),'trace_schema':record['trace']['schema'],'prechecker_registry_digest':digest(result['expected_method_registry']),'source_signature':sig,'source_direction_witness':a['witness'],'member_quality_qualified':False})
 if digest(models[0]['inputs'])!=digest(models[1]['inputs'])or digest(models[0]['program'])!=digest(models[1]['program'])or digest(models[0]['profile'])!=digest(models[1]['profile']):raise ValueError('SHARED_INPUT_PROGRAM_PROFILE')
 distinct=members[0]['source_signature']!=members[1]['source_signature'];check()
 return {'schema':'FIXED_JOINT367_BALANCED365_ORGANIZATION_PAIR_ONLY','status':'PAIR_DISTINCT_SOURCE_SCOPE_BUT_MEMBERS_NOT_YET_QUALIFIED'if distinct else'PAIR_ORGANIZATION_NOT_PROVEN_DISTINCT','members':members,'pair_count':1,'source_organization_distinct':distinct,'pair_identity':digest([{k:m[k]for k in('member','record_digest','fresh_result_digest','model_digest','trace_schema')}for m in members]),'requested_count':2,'qualified_selected_count':0,'request_fulfilled':False,'selected_set_membership_authority':False,'live_authority':False,'accepted':False,'delivery_allowed':False,'missing':['OWN_11_PARENT_AND_PER_UNIT_Q12_QUALIFICATION_FOR_EACH_MEMBER','FINAL_IMMUTABLE_QUALIFIED_SELECTED_SET'],'scope':'SOURCE133 ACTUAL BEDROOM PORT NORMAL DOT RELATIONS; D4_AND_TWIN_SWAP_INVARIANT; NOT_ALL_ARCHITECTURE_OR_MEMBER_QUALITY; NO_LEGACY_GATE_FLAGS_SYNTHESIZED'}
