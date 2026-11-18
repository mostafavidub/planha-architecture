"""Source-bound storage/HTTP protocol for the experimental general engine.
Engine and independent checker are injected; this module admits no geometry.
"""
import json,sqlite3,re,hashlib,base64
from copy import deepcopy

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
class Service:
 def __init__(self,db,run,check_candidate,revision,exporters,budget_seconds=15):
  self.db=db;self.run=run;self.check=check_candidate;self.revision=revision;self.exporters=exporters;self.budget=budget_seconds;self.startup_revision=revision()
  with sqlite3.connect(db)as c:c.execute('CREATE TABLE IF NOT EXISTS drafts118(id TEXT PRIMARY KEY,raw TEXT,payload TEXT)')
 def _decorate(self,result,raw):
  p=deepcopy(result);p['service_schema']='GENERAL118';p['source_revision']=self.revision();p['request_raw']=deepcopy(raw)
  cs=[]
  for c in p.get('candidates',[]):
   c=deepcopy(c);c['candidate_id']=digest({'raw':raw,'source_revision':p['source_revision'],'candidate':c});cs.append(c)
  p['candidates']=cs
  self._counts(p);p['payload_hash']=digest(p);return p
 def _counts(self,p):
  n=len(p.get('candidates',[]))
  if p.get('requested_count')!=6 or p.get('distinct_count')!=n or p.get('shortfall')!=6-n or not 0<=n<=6:raise ValueError('COUNT_CONTRACT')
  if type(p.get('admitted_count'))is not int or p['admitted_count']<n:raise ValueError('ADMISSION_COUNT_CONTRACT')
 def _validate(self,p,raw,candidate_id=None):
  if p.get('service_schema')!='GENERAL118'or p.get('request_raw')!=raw:raise ValueError('SAVED_INPUT_SCHEMA')
  if p.get('source_revision')!=self.revision():raise ValueError('SOURCE_REVISION_CHANGED')
  if digest({k:v for k,v in p.items()if k!='payload_hash'})!=p.get('payload_hash'):raise ValueError('SAVED_PAYLOAD_HASH')
  self._counts(p)
  for c in p['candidates']:
   bare={k:v for k,v in c.items()if k!='candidate_id'}
   if digest({'raw':raw,'source_revision':p['source_revision'],'candidate':bare})!=c['candidate_id']:raise ValueError('CANDIDATE_BINDING')
   if candidate_id is None or c['candidate_id']==candidate_id:
    fresh=self.check(bare,raw)
    if digest(fresh)!=digest(bare):raise ValueError('SAVED_GATE_OR_MODEL_BINDING')
 def handle(self,path,r):
  # Explicit protocol aliases within the isolated122 service only. Earlier
  # databases/servers are never opened or migrated by this adapter.
  path={'/generate-hybrid122':'/generate-hybrid118','/reopen-hybrid122':'/reopen-hybrid118','/hybrid122-artifact':'/hybrid118-artifact','/generate-hybrid121':'/generate-hybrid118','/reopen-hybrid121':'/reopen-hybrid118','/hybrid121-artifact':'/hybrid118-artifact','/generate-hybrid120':'/generate-hybrid118','/reopen-hybrid120':'/reopen-hybrid118','/hybrid120-artifact':'/hybrid118-artifact','/generate-hybrid119':'/generate-hybrid118','/reopen-hybrid119':'/reopen-hybrid118','/hybrid119-artifact':'/hybrid118-artifact'}.get(path,path)
  try:
   if self.revision()!=self.startup_revision:raise ValueError('SOURCE_REVISION_CHANGED')
   op=r.get('operation_id','')
   if not re.fullmatch('[a-f0-9]{32}',op):raise ValueError('OPERATION_ID')
   with sqlite3.connect(self.db)as db:row=db.execute('SELECT raw,payload FROM drafts118 WHERE id=?',(op,)).fetchone()
   if path=='/generate-hybrid118':
    if set(r)-{'operation_id','W','L','n','requested_count'}or not {'W','L','n','requested_count'}<=set(r):raise ValueError('REQUEST_FIELDS')
    raw={k:v for k,v in r.items()if k!='operation_id'}
    if row:
     if raw!=json.loads(row[0]):raise ValueError('OPERATION_INPUT_CONFLICT')
     p=json.loads(row[1]);self._validate(p,raw)
    else:
     generated=self.run(raw,budget_seconds=self.budget)
     if self.revision()!=self.startup_revision:raise ValueError('SOURCE_REVISION_CHANGED')
     p=self._decorate(generated,raw)
     with sqlite3.connect(self.db)as db:db.execute('INSERT INTO drafts118 VALUES(?,?,?)',(op,json.dumps(raw),json.dumps(p)))
   elif path in('/reopen-hybrid118','/hybrid118-artifact'):
    expected={'operation_id'}if path=='/reopen-hybrid118'else{'operation_id','payload_hash','candidate_id','artifact_type'}
    if set(r)!=expected or not row:raise ValueError('NOT_FOUND_OR_FIELDS')
    raw=json.loads(row[0]);p=json.loads(row[1])
    if path=='/hybrid118-artifact':
     if r['payload_hash']!=p.get('payload_hash')or len([c for c in p['candidates']if c['candidate_id']==r['candidate_id']])!=1:raise ValueError('ARTIFACT_SELECTION_BINDING')
    self._validate(p,raw,r.get('candidate_id'))
   else:raise ValueError('UNKNOWN_PATH')
   response={'operation_id':op,'result':p}
   if path=='/hybrid118-artifact':
    kind=r['artifact_type']
    if kind not in self.exporters:raise ValueError('ARTIFACT_TYPE')
    c=next(c for c in p['candidates']if c['candidate_id']==r['candidate_id']);bare={k:v for k,v in c.items()if k!='candidate_id'};b=self.exporters[kind](bare)
    response['artifact']={'base64':base64.b64encode(b).decode(),'sha256':hashlib.sha256(b).hexdigest(),'name':'plan122-'+r['candidate_id'][:12]+'.'+kind,'candidate_id':r['candidate_id'],'payload_hash':p['payload_hash'],'mime':'image/svg+xml'if kind=='svg'else'application/dxf'}
   if self.revision()!=self.startup_revision:raise ValueError('SOURCE_REVISION_CHANGED')
   return response
  except Exception as e:return {'status':'REQUEST_FAILED','reason':str(e),'candidates':[],'accepted':False}
