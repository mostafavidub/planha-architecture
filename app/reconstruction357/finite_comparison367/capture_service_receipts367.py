"""One diagnostic invocation preserving exact nested receipts, not an admission gate."""
import json,sys,hashlib,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='03bb8341527b35da7ac2566c3e91da7cb525b7712bce3ea585bf0ebe77e0867d'
p=ROOT/'finite_comparison367/service_manifest367.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()==MANIFEST_SHA
files=json.loads(p.read_text())['files']
def check():
 for n,h in files.items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
check();sys.path[:0]=[str(ROOT/'finite_comparison367'),str(ROOT/'semantic_rules357')]
import service_criterion367_v3 as s
from service_role_inventory_joint367 import evaluate as roles
from common import digest
r,f=[json.loads((ROOT/p).read_text())for p in ['review367_joint_attempt2/actual367.json','review367_joint_source_validation_attempt2/result.json']]
t=time.monotonic();cost=s.costs(r,f);q=s.necessity(r,f);partition=roles(r,f);result=s.reduce_bound(r,f,cost,q,partition);check()
assert result['cost_receipt_digest']==digest(cost)and result['necessity_receipt_digest']==digest(q)and result['functional_partition_digest']==digest(partition)

def diff(a,b,path=''):
 if type(a)!=type(b):return [{'path':path,'before':a,'after':b}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append({'path':path+'/'+k,'before':a.get(k),'after':b.get(k)})
   else:out+=diff(a[k],b[k],path+'/'+k)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [{'path':path,'before_length':len(a),'after_length':len(b)}]
  return [d for i,(x,y)in enumerate(zip(a,b))for d in diff(x,y,path+'/'+str(i))]
 return []if a==b else[{'path':path,'before':a,'after':b}]
oldq=json.loads((ROOT/'finite_comparison367/q04_actual367_v3.json').read_text());oldp=json.loads((ROOT/'semantic_rules357/service_role_inventory_joint_actual367.json').read_text())
out={'schema':'DIAGNOSTIC367_SAME_INVOCATION_RECEIPT_CAPTURE','manifest_sha256':MANIFEST_SHA,'record_digest':digest(r),'fresh_result_digest':digest(f),'nested':{'cost':cost,'q04':q,'partition':partition},'reduced_result':result,'digests_recompute_match':True,'q04_diffs_from_standalone':diff(oldq,q),'partition_diffs_from_standalone':diff(oldp,partition),'elapsed_seconds':time.monotonic()-t,'admission':False}
target=ROOT/'finite_comparison367/service_receipts_capture367.json';assert not target.exists();target.write_text(json.dumps(out,indent=2));print(json.dumps({'qdiff':len(out['q04_diffs_from_standalone']),'pdiff':len(out['partition_diffs_from_standalone']),'seconds':out['elapsed_seconds']}))
