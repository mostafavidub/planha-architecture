"""Supplemental same-process producer provenance, not architectural acceptance.
Historical replay proves reconstruction, not the identity of this new producer.
"""
import hashlib
from pathlib import Path
import inspect,sys
from review_cycle import digest

def snapshot(root,paths):
    root=Path(root).resolve();out={}
    for name in paths:
        p=(root/name).resolve()
        if root not in p.parents:raise ValueError('PRODUCER_PATH_OUTSIDE_ROOT')
        out[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    if not out:raise ValueError('PRODUCER_SOURCES_REQUIRED')
    return out

def require_unchanged(root,before):
    if snapshot(root,list(before))!=before:raise ValueError('EXPERIMENTAL_PRODUCER_SOURCE_CHANGED')

def require_imported(module,expected,private_expected):
    if Path(module.__file__).resolve()!=Path(expected).resolve():raise ValueError('PRODUCER_IMPORT_PATH_MISMATCH')
    fn=module.private_source
    owner=sys.modules[fn.__module__]
    if Path(owner.__file__).resolve()!=Path(private_expected).resolve() or Path(inspect.getsourcefile(fn)).resolve()!=Path(private_expected).resolve():
        raise ValueError('PRODUCER_PRIVATE_IMPORT_PATH_MISMATCH')

def receipt(*,sources,request_digest,raw,proposal,packet,context,review,engine_revision):
    if not sources:raise ValueError('PRODUCER_SOURCES_REQUIRED')
    trace=context['construction_trace']
    if trace.get('raw')!=raw or trace.get('proposal')!=proposal:raise ValueError('PRODUCER_TRACE_BINDING')
    model_hash=digest(packet['world_model'])
    if context['construction_trace']['model_hash']!=model_hash or review.get('model_hash')!=model_hash:
        raise ValueError('PRODUCER_MODEL_BINDING')
    result={'schema':'V25_EXPERIMENTAL_PRODUCER_RECEIPT_V1',
      'source_files':dict(sources),'request_digest':request_digest,
      'proposal_digest':digest(proposal),'initial_model_digest':model_hash,
      'construction_context_digest':digest(context),'initial_review_digest':digest(review),
      'historical_engine_revision':engine_revision,
      'accepted':False,'delivery_allowed':False,'qualified':False,
      'scope':'same-process experimental producer identity plus separately evaluated historical reconstruction; not independent solver replay or architectural qualification'}
    result['receipt_digest']=digest(result)
    return result
