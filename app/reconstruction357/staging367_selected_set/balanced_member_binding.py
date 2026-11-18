"""Read one fixed actual qualification. No caller input, rerun or issuance."""
import json,hashlib
from pathlib import Path
from selection_v2 import REQUIRED,digest,_hex64
P=Path(__file__).resolve().parent;ROOT=P.parent
REGISTRY_SHA='cda83584db40c0e5ddfc147c1cc77ec891afbefe2b49a2132b88bfe4e7dba2e4'
STATUS='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW'
def validate_content(record,fresh,out,manifest):
 m=record['candidate']['model'];mh=digest(m);rd=digest(record);fd=digest(fresh)
 if out['schema']!='BALANCED365_QUALIFICATION_EXPANDED367' or out['model_digest']!=mh or out['record_digest']!=rd or out['fresh_result_digest']!=fd:raise ValueError('QUALIFICATION_CURRENT_BINDING')
 if manifest['record_digest']!=rd or manifest['fresh_digest']!=fd or fresh['model_digest']!=mh:raise ValueError('FIXED_INPUT_BINDING')
 qs=out['quality']
 if type(qs)is not list or len(qs)!=12 or any(type(q)is not dict for q in qs):raise ValueError('QUALITY_SHAPE')
 ids=[q['rule_id']for q in qs]
 if len(set(ids))!=12 or set(ids)!=set(REQUIRED)|{'DISTINCTNESS_AND_FAIRNESS'}:raise ValueError('EXACT_RULE_INVENTORY')
 for q in qs:
  if q['rule_id'] in REQUIRED:
   if q['verdict']!='PASS' or q.get('missing')!=[] or q.get('model_hash')!=mh or not q.get('scope') or not q.get('source_closure'):raise ValueError('INCOMPLETE_SCOPED_PARENT')
 q12=out['internal_q12'];units=[u['id']for u in m['units']];rows=q12['evidence']
 if len(set(units))!=len(units) or type(rows)is not list or len(rows)!=len(units) or any(type(x)is not dict for x in rows) or {x['unit']for x in rows}!=set(units):raise ValueError('Q12_UNIT_INVENTORY')
 if q12['status']!=STATUS or q12['blocking_dependencies']!=[]:raise ValueError('Q12_PENDING')
 deps=q12['sealed_dependency_digests']
 if set(deps)!=set(q12['depends_on']) or not all(_hex64(v)for v in deps.values()):raise ValueError('Q12_DEPENDENCY_SEALS')
 nodes=out['roles']['nodes']
 if any(deps[k]!=digest(nodes[k])for k in deps):raise ValueError('Q12_SOURCE_NODE_SEALS')
 if digest(nodes['Q12_PER_UNIT'])!=digest(q12):raise ValueError('Q12_ACTUAL_NODE')
 balance=q12['balanced_common_access'];bh=digest(balance)
 if balance['model_hash']!=mh or balance['record_digest']!=rd or balance['fresh_result_digest']!=fd:raise ValueError('BALANCE_CURRENT_BINDING')
 for row in rows:
  if row['whole_unit_verdict']!=STATUS or row['exact_pending']!=[] or row['resolved_dependency_digests']!={k:deps[k]for k in ('COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON')} or row['balanced_access_digest']!=bh or not row['source_room_roles'] or not row['capacity_use_access_source_rows']:raise ValueError('Q12_UNIT_INCOMPLETE')
 return {'model_digest':mh,'record_digest':rd,'fresh_digest':fd,'qualification_digest':digest(out),'unit_ids':units,'q12_digest':digest(q12),'eleven_parent_evidence_complete':True,'membership_authority':False}
def inspect_registered_member():
 try:
  data=(P/'balanced_member_registry.json').read_bytes()
  if hashlib.sha256(data).hexdigest()!=REGISTRY_SHA:raise ValueError('REGISTRY_CHANGED')
  reg=json.loads(data)
  def read(k):
   x=reg['files'][k];d=(ROOT/x['path']).read_bytes()
   if hashlib.sha256(d).hexdigest()!=x['sha256']:raise ValueError('FIXED_FILE_CHANGED:'+k)
   return d
  captured={k:read(k)for k in reg['files']};man=json.loads(captured['manifest'])
  def check():
   for n,h in man['files'].items():
    if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('TRANSITIVE_SOURCE_CHANGED:'+n)
   for k in reg['files']:read(k)
  check();out=json.loads(captured['qualification'])
  if out['invocation_manifest_sha256']!=reg['files']['manifest']['sha256']:raise ValueError('INVOCATION_MANIFEST')
  result=validate_content(json.loads(captured['record']),json.loads(captured['fresh']),out,man);check()
  result.update(status='BOUND_ACTUAL_MEMBER_PENDING_INDEPENDENT_AUDIT_AND_FINAL_REGISTRY',qualified_selected_count=0,request_fulfilled=False,accepted=False,delivery_allowed=False)
  return result
 except (ValueError,KeyError,TypeError,IndexError,OSError)as e:return {'status':'UNKNOWN','missing':[str(e)],'membership_authority':False,'qualified_selected_count':0,'accepted':False,'delivery_allowed':False}
