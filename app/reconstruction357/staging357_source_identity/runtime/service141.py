"""Source-bound storage/HTTP protocol for the experimental general engine.
Engine and independent checker are injected; this module admits no geometry.
"""
import json,sqlite3,re,hashlib,base64
from copy import deepcopy
from collections import OrderedDict
from threading import RLock

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
class Service:
 def __init__(self,db,run,check_candidate,revision,exporters,budget_seconds=15):
  self.db=db;self.run=run;self.check=check_candidate;self.revision=revision;self.exporters=exporters;self.budget=budget_seconds;self.startup_revision=revision()
  self._counts_cache=OrderedDict();self._counts_lock=RLock();self._counts_limit=16
  with sqlite3.connect(db)as c:c.execute('CREATE TABLE IF NOT EXISTS drafts141(id TEXT PRIMARY KEY,raw TEXT,payload TEXT)')
 def _decorate(self,result,raw):
  p=deepcopy(result);p['service_schema']='GENERAL141';p['source_revision']=self.revision();p['request_raw']=deepcopy(raw)
  cs=[]
  for c in p.get('candidates',[]):
   c=deepcopy(c);c['candidate_id']=digest({'raw':raw,'source_revision':p['source_revision'],'candidate':c});cs.append(c)
  p['candidates']=cs
  self._counts(p);p['payload_hash']=digest(p);return p
 def _counts(self,p):
  # Cache only a successful deterministic count/selection verification. It is
  # NOT a gate receipt: _validate still freshly checks all pool/selected items.
  # Never key on the caller's payload_hash or mutable object identity.
  revision=self.revision()
  if revision!=self.startup_revision:raise ValueError('SOURCE_REVISION_CHANGED')
  snapshot=deepcopy({k:v for k,v in p.items()if k!='payload_hash'})
  key=digest({'policy':'COUNTS141_V1','source_revision':revision,'payload':snapshot})
  with self._counts_lock:
   hit=key in self._counts_cache
   if hit:self._counts_cache.move_to_end(key)
  if not hit:self._counts_uncached(snapshot)
  if self.revision()!=revision:raise ValueError('SOURCE_REVISION_CHANGED')
  if digest({k:v for k,v in p.items()if k!='payload_hash'})!=digest(snapshot):raise ValueError('COUNTS_PAYLOAD_CHANGED')
  # Empty/failed/pending selections are deliberately never memoized.
  from engine114 import _eligible
  pool=snapshot.get('admitted_pool',[])
  if pool and all(_eligible(c.get('gate',{}))for c in pool):
   with self._counts_lock:
    self._counts_cache[key]=True;self._counts_cache.move_to_end(key)
    while len(self._counts_cache)>self._counts_limit:self._counts_cache.popitem(last=False)
 def _counts_uncached(self,p):
  n=len(p.get('candidates',[]))
  from schedule123 import requested_count
  requested=requested_count(p.get('request_raw',{'requested_count':p.get('requested_count')}))
  if p.get('requested_count')!=requested or p.get('distinct_count')!=n or p.get('shortfall')!=requested-n or not 0<=n<=requested:raise ValueError('COUNT_CONTRACT')
  from engine141 import select_scoped
  pool=p.get('admitted_pool')
  if not isinstance(pool,list):raise ValueError('MISSING_ADMITTED_POOL')
  from engine114 import _eligible
  internal=p.get('internal_proposals')
  if not isinstance(internal,list):raise ValueError('MISSING_PAIR_EVIDENCE')
  derived=[{'model':e['packet'].get('model',e['packet'].get('world_model')),'packet':e['packet'],'generation_context':e['generation_context'],'gate':e['gate']}for e in internal if _eligible(e.get('gate',{}))]
  if digest(derived)!=digest(pool):raise ValueError('ADMITTED_POOL_PAIR_EVIDENCE_BINDING')
  bare=[{k:v for k,v in c.items()if k!='candidate_id'}for c in p.get('candidates',[])]
  selected,proof=select_scoped(pool,requested)
  if digest(selected)!=digest(bare):raise ValueError('PROGRAM_FIRST_SELECTED_POOL_BINDING')
  if p.get('organization_count')!=len(selected)or p.get('organization_shortfall')!=requested-len(selected):raise ValueError('ORGANIZATION_COUNT_BINDING')
  if p.get('pool_diversity_diagnostics')!=proof:raise ValueError('PROGRAM_POLICY_POOL_PROOF_BINDING')
  _,selectedproof=select_scoped(selected,requested)
  if p.get('scoped_diversity')!=selectedproof:raise ValueError('SELECTED_PROOF_BINDING')
  if p.get('verified_architectural_diversity')is not False:raise ValueError('ARCHITECTURAL_DIVERSITY_SCOPE')
  if p.get('admitted_count')!=len(pool):raise ValueError('ADMITTED_POOL_COUNT')
  if type(p.get('admitted_count'))is not int or p['admitted_count']<n:raise ValueError('ADMISSION_COUNT_CONTRACT')
 def _validate(self,p,raw,candidate_id=None):
  if p.get('service_schema')!='GENERAL141'or p.get('request_raw')!=raw:raise ValueError('SAVED_INPUT_SCHEMA')
  if p.get('source_revision')!=self.revision():raise ValueError('SOURCE_REVISION_CHANGED')
  if digest({k:v for k,v in p.items()if k!='payload_hash'})!=p.get('payload_hash'):raise ValueError('SAVED_PAYLOAD_HASH')
  self._counts(p)
  for c in p['admitted_pool']:
   if digest(self.check(c,raw))!=digest(c):raise ValueError('POOL_FRESH_GATE_BINDING')
  for c in p['candidates']:
   bare={k:v for k,v in c.items()if k!='candidate_id'}
   if digest({'raw':raw,'source_revision':p['source_revision'],'candidate':bare})!=c['candidate_id']:raise ValueError('CANDIDATE_BINDING')
   if candidate_id is None or c['candidate_id']==candidate_id:
    fresh=self.check(bare,raw)
    if digest(fresh)!=digest(bare):raise ValueError('SAVED_GATE_OR_MODEL_BINDING')
 def handle(self,path,r):
  try:
   if self.revision()!=self.startup_revision:raise ValueError('SOURCE_REVISION_CHANGED')
   op=r.get('operation_id','')
   if not re.fullmatch('[a-f0-9]{32}',op):raise ValueError('OPERATION_ID')
   with sqlite3.connect(self.db)as db:row=db.execute('SELECT raw,payload FROM drafts141 WHERE id=?',(op,)).fetchone()
   if path=='/generate-hybrid141':
    if set(r)-{'operation_id','W','L','n','requested_count'}or not {'W','L','n','requested_count'}<=set(r):raise ValueError('REQUEST_FIELDS')
    raw={k:v for k,v in r.items()if k!='operation_id'}
    if row:
     if raw!=json.loads(row[0]):raise ValueError('OPERATION_INPUT_CONFLICT')
     p=json.loads(row[1]);self._validate(p,raw)
    else:
     generated=self.run(raw,budget_seconds=self.budget)
     if self.revision()!=self.startup_revision:raise ValueError('SOURCE_REVISION_CHANGED')
     p=self._decorate(generated,raw)
     with sqlite3.connect(self.db)as db:db.execute('INSERT INTO drafts141 VALUES(?,?,?)',(op,json.dumps(raw),json.dumps(p)))
   elif path in('/reopen-hybrid141','/hybrid141-artifact'):
    expected={'operation_id'}if path=='/reopen-hybrid141'else{'operation_id','payload_hash','candidate_id','artifact_type'}
    if set(r)!=expected or not row:raise ValueError('NOT_FOUND_OR_FIELDS')
    raw=json.loads(row[0]);p=json.loads(row[1])
    if path=='/hybrid141-artifact':
     if r['payload_hash']!=p.get('payload_hash')or len([c for c in p['candidates']if c['candidate_id']==r['candidate_id']])!=1:raise ValueError('ARTIFACT_SELECTION_BINDING')
    self._validate(p,raw,r.get('candidate_id'))
   else:raise ValueError('UNKNOWN_PATH')
   response={'operation_id':op,'result':p}
   if path=='/hybrid141-artifact':
    kind=r['artifact_type']
    if kind not in self.exporters:raise ValueError('ARTIFACT_TYPE')
    c=next(c for c in p['candidates']if c['candidate_id']==r['candidate_id']);bare={k:v for k,v in c.items()if k!='candidate_id'};b=self.exporters[kind](bare)
    response['artifact']={'base64':base64.b64encode(b).decode(),'sha256':hashlib.sha256(b).hexdigest(),'name':'plan141-'+r['candidate_id'][:12]+'.'+kind,'candidate_id':r['candidate_id'],'payload_hash':p['payload_hash'],'mime':'image/svg+xml'if kind=='svg'else'application/dxf'}
   if self.revision()!=self.startup_revision:raise ValueError('SOURCE_REVISION_CHANGED')
   return response
  except Exception as e:return {'status':'REQUEST_FAILED','reason':str(e),'candidates':[],'accepted':False}
