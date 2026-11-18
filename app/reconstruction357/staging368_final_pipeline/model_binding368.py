"""Run-specific request/model inventory binding, no geometry verdict."""
from request_contract368 import digest,verify
SCHEMAS={'balanced':'ROW_BALANCED_PORTALS365_SOURCE_TRACE_V1','joint':'SOURCE_SERVICE_JOINT367_TRACE_V1'}
def bind(envelope,record,kind,run_id):
 e=verify(envelope);c=record['candidate'];t=record['trace'];m=c['model'];p=c['packet']
 if kind not in SCHEMAS or t['schema']!=SCHEMAS[kind]:raise ValueError('PRODUCER_SCHEMA')
 if digest(c['request'])!=e['raw_digest']or c['request_digest']!=e['raw_digest']:raise ValueError('PRODUCER_REQUEST_CHANGED')
 mh=digest(m)
 if m.get('schema')!='GENERAL117_HIERARCHICAL_STUDY' or m.get('contract_version')!='114-provisional-v1':raise ValueError('COMMON_MODEL_SCHEMA')
 expected={'balanced':'8013a1328a6104be58d9de22834dce16b1754277f450fa0ba8475253c26fc783','joint':'b1256726013116ef5f1cbcd784380a80861fa485c372909d52bf8bce0d398759'}
 if mh!=expected[kind]:raise ValueError('FIXED_SOURCE_MODEL_CHANGED_NOT_CACHED_RETURN')
 if c['model_digest']!=mh or t['model_digest']!=mh or t['candidate_digest']!=digest(c) or digest(p['world_model'])!=mh:raise ValueError('MODEL_PACKET_TRACE_BINDING')
 if m['inputs']!=['26','28',2] or digest(m['inputs'])!=digest(['26','28',2]):raise ValueError('MODEL_INPUT_TYPES')
 units=m['units'];ids=[u['id']for u in units]
 if len(ids)!=2 or set(ids)!={'A','B'}or any(type(x)is not str for x in ids):raise ValueError('UNIT_ID_INVENTORY')
 opening_ids=[x.get('id')for x in m['openings']]
 if any(type(x)is not str or not x for x in opening_ids)or len(set(opening_ids))!=len(opening_ids):raise ValueError('OPENING_IDS')
 entities=[]
 for u in units:
  for category in ('rooms','fixtures','activities'):
   if type(u[category])is not dict or any(type(k)is not str or not k.strip()for k in u[category]):raise ValueError('ENTITY_IDS')
   entities.extend({'unit_id':u['id'],'kind':category,'source_id':k}for k in u[category])
 candidate_id=digest({'run_id':run_id,'kind':kind,'model_digest':mh})
 return {'schema':'RUN_CANDIDATE_BINDING368','run_id':run_id,'candidate_id':candidate_id,'canonical_request_digest':e['canonical_request_digest'],'normalized_request_digest':e['raw_digest'],'source_candidate_digest':digest(c),'source_trace_digest':digest(t),'model_digest':mh,'packet_digest':digest(p),'unit_ids':ids,'entity_ids':[dict(x,qualified_id=candidate_id+'/'+x['unit_id']+'/'+x['kind']+'/'+x['source_id'])for x in entities],'scope':'EXACT_DATA_BINDING_NOT_REVIEW_OR_ACCEPTANCE'}
