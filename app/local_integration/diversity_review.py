"""All-pairs diagnostic, never converts coordinate differences into six designs."""
import json,sys,itertools,hashlib
from pathlib import Path
from review_cycle import decide,digest
ROOT=next(p for p in Path(__file__).resolve().parents if(p/'manifests/WORKTREE_STATE.json').is_file())
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'

def audit(candidates,request_digest,source_revision):
 sys.path.insert(0,str(ENGINE));import diversity124 as base;import diversity_multidim126 as multi
 descriptions=[];failures=[];cache={}
 for index,c in enumerate(candidates):
  try:
   expected=decide(c,request_digest,source_revision,c.get('repair_receipt'))
   if c['review_decision']!=expected:raise ValueError('DIVERSITY_REVIEW_BINDING')
   if expected['state']!='PHYSICAL_PASS_SEMANTIC_UNKNOWN':raise ValueError('PHYSICAL_REVIEW_NOT_PASS')
   key=c['model_digest']
   if key not in cache:
    d=base.describe_model(c['model']);program=json.loads(d['program_key']);program['frame']=[sorted(program['frame'][:2],key=multi.F),program['frame'][2]]
    cache[key]={'program_key':base.canonical(program),'access_signature':d['access_signature'],'spatial':multi.spatial_variants(c['model'])}
   descriptions.append(cache[key])
  except(KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as error:
   descriptions.append(None);failures.append({'index':index,'reason':str(error)})
 pairs=[]
 for i,j in itertools.combinations(range(len(candidates)),2):
  if candidates[i]['model_digest']==candidates[j]['model_digest']:comparison={'status':'DUPLICATE_MODEL','distinct':False}
  elif descriptions[i]is None or descriptions[j]is None:comparison={'status':'UNRESOLVED_MISSING_BOUND_DESCRIPTOR','distinct':False}
  else:comparison=multi.compare(descriptions[i],descriptions[j])
  pairs.append({'a':i,'b':j,**comparison})
 return {'schema':'MAC_ALL_PAIRS_DIVERSITY_V1','request_digest':request_digest,'source_revision':source_revision,'candidate_ids':[c['candidate_id']for c in candidates],'model_digests':[c['model_digest']for c in candidates],'required_pairs':len(candidates)*(len(candidates)-1)//2,'pairs':pairs,'descriptor_failures':failures,'proven_distinct_pairs':sum(p['distinct']for p in pairs),'qualified_count':0,'accepted':False,'delivery_allowed':False,'scope':'All current generated pairs, not six-option search or architectural qualification. Exact source-bound relation differences must survive isometries and unit permutations; UNKNOWN is not proof of sameness.','source_hashes':{n:hashlib.sha256((ENGINE/n).read_bytes()).hexdigest()for n in ['diversity124.py','diversity_multidim126.py']}}
