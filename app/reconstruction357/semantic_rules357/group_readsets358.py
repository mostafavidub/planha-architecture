"""Pure, pinned stored-artifact reassessment. Never Origin267 or live authority.
Version358 extracts unchanged semantic group285 validator body and network288
kernel from pinned351 code. Their origin gate is NOT mocked: an explicit358
artifact/provenance/source gate replaces it, under distinct view schema.
"""
import json,hashlib,types,copy,ast,time
from pathlib import Path
from common import digest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

PROFILE_REGISTRIES={'SOURCE358':('method_registry_source358.json','group_readsets358_pins.json')}

def build(record,new_result,seconds=8,source_profile='SOURCE358'):
 if type(seconds)not in(int,float)or not 0<seconds<=10:raise ValueError('BOUNDED_SECONDS')
 if source_profile not in PROFILE_REGISTRIES:raise ValueError('UNREGISTERED_SOURCE_PROFILE')
 registry_name,pins_name=PROFILE_REGISTRIES[source_profile]
 before=digest([record,new_result]);pins=json.loads((HERE/pins_name).read_text())
 if digest(record)!=pins['record_digest']or digest(new_result)!=pins['result_digest']:raise ValueError('UNREGISTERED_STORED_ARTIFACT_NOT_LIVE_AUTHORITY')
 registry_path=HERE/registry_name
 if hashlib.sha256(registry_path.read_bytes()).hexdigest()!=pins['registry_sha256']:raise ValueError('REGISTRY_PIN')
 registry=json.loads(registry_path.read_text());r=new_result;c=record['candidate'];p=r['provenance'];m=c['model'];mh=digest(m)
 if r['schema']!=pins['expected_schema']or r['input_record_digest']!=digest(record)or r['outer_trace_digest']!=digest(record['trace'])or r['model_digest']!=mh:raise ValueError('SOURCE358_RECORD_RESULT_BINDING')
 if p['input_record_digest']!=digest(record)or p['outer_trace_digest']!=digest(record['trace'])or p['candidate_digest']!=digest(c)or p['packet_digest']!=digest(c['packet'])or p['model_hash']!=mh:raise ValueError('SOURCE358_PROVENANCE_BINDING')
 if digest(c['packet']['world_model'])!=mh or c['model_digest']!=mh or record['trace']['candidate_digest']!=digest(c):raise ValueError('SOURCE358_PACKET_TRACE')
 if digest(p['raw'])!=digest(record['trace']['raw'])or digest(p['raw'])!=digest(c['request']):raise ValueError('VERIFIED_RAW_INPUT_BINDING')
 expected=r['expected_method_registry']
 if registry['sources']!=expected['sources']or registry['methods']!=expected['methods']or registry['applicability']!=expected['applicability']:raise ValueError('PRECOMPUTED_REGISTRY_BINDING')
 for name,sha in registry['sources'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE358_SOURCE_DRIFT:'+name)
 # Instantiate common source profile without changing process-global common state.
 source=(HERE/'common.py').read_bytes();cm=types.ModuleType('_group358_bound_common');cm.__file__=str(HERE/'common.py');exec(compile(source,cm.__file__,'exec'),cm.__dict__);cm.REGISTRY_NAME=registry_name;cm.rows(m,r['raw_report'])
 path=ROOT/'staging351_collision_lineage/fresh_bridge.py';code=path.read_bytes()
 if hashlib.sha256(code).hexdigest()!=pins['bridge_sha256']:raise ValueError('BRIDGE_PIN')
 bridge=types.ModuleType('_group358_semantic_kernel351');bridge.__file__=str(path);exec(compile(code,str(path),'exec'),bridge.__dict__)
 contract,_=bridge._group_sources285();bridge._network_sources288()
 envelope={'schema':'REGISTERED_SOURCE358_VIEW','candidate_id':digest(c),'raw':copy.deepcopy(p['raw']),'packet':copy.deepcopy(c['packet']),'input_record_digest':digest(record),'outer_trace_digest':digest(record['trace']),'original_result_digest':digest(r),'artifact_reassessment_only':True,'new_fresh_execution':False}
 result={'schema':'REGISTERED_SOURCE358_RESULT_VIEW','candidate_digest':digest(envelope),'raw_fresh_report':copy.deepcopy(r['raw_report']),'original_result_digest':digest(r),'input_record_digest':digest(record),'outer_trace_digest':digest(record['trace']),'artifact_reassessment_only':True,'new_fresh_execution':False}
 # Extract only nested semantic predicates + row validation loop, never old
 # source_groups285(origin,facts,...) entry/exit gates or fabricated facts.
 tree=ast.parse(code);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='source_groups285');text=ast.get_source_segment(code.decode(),node)
 start=text.index(" raw=result['raw_fresh_report']");end=text.index(" _phase293('network.begin')")
 body=text[start:end]
 fn="def semantic_rows358(envelope,result,contract,methods):\n model=envelope['packet']['world_model'];mh=_digest_model282(model)\n"+body+" return summaries\n"
 ns=dict(bridge.__dict__);exec(compile(fn,'<EXPLICIT358_SEMANTIC_BODY_FROM_PINNED351>','exec'),ns)
 groups=ns['semantic_rows358'](envelope,result,contract,{k:registry['methods'][k]for k in bridge.GROUP285_IDS})
 network=bridge._network288(envelope,result,groups,min(seconds,2));groups.append(network)
 states=[g['verdict']for g in groups];state='FAIL'if 'FAIL'in states else'UNKNOWN'if 'UNKNOWN'in states else'SCOPED_PASS'
 output={'schema':'REGISTERED_SOURCE358_GROUP_READSETS','model_hash':mh,'fresh_result_digest':digest(result),'original_result_digest':digest(r),'input_record_digest':digest(record),'outer_trace_digest':digest(record['trace']),'rows':groups,'review_verdict':state,'parent_complete':False,'repair_authority':False,'artifact_reassessment_only':True,'new_fresh_execution':False,'source_profile':source_profile,'semantic_kernel_bridge_sha256':pins['bridge_sha256'],'transformation':'EXTRACT_SEMANTIC_BODY_ONLY; REPLACE_ORIGIN267_GATE_WITH_REGISTERED358_ARTIFACT_GATE; NO_MOCK_FACTS'}
 if before!=digest([record,new_result])or digest(result['raw_fresh_report'])!=digest(r['raw_report']):raise ValueError('INPUT_OR_RAW_MUTATION')
 for name,sha in registry['sources'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_CHANGED_DURING_READSETS')
 return {'envelope':envelope,'result':result,'groups':output,'network':network,'new_fresh_execution':False,'live_authority':False}
