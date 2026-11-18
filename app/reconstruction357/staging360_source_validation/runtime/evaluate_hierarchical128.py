"""Internal saved-proposal evaluation; no public 128 endpoint asserted."""
from contract114 import digest
from construction_replay128 import verify

def evaluate(packet,context):
 from checker114 import evaluate as whole
 from private_macro128 import inspect
 model=packet['model'];origin=verify(model,context);macro=inspect(model)
 report=whole(model,workflow_context=context)
 report['hierarchical_provenance128']=origin;report['private_macro_interface128']=macro
 report['errors']+=origin['errors']+macro['errors'];report['pending']+=origin['pending']+macro['pending']
 if digest(packet['core'])!=context.get('construction_trace',{}).get('core_hash'):report['errors'].append({'code':'HIERARCHICAL_PACKET_CORE_BINDING'})
 if packet.get('admission_claim')is not False:report['errors'].append({'code':'PRODUCER_ADMISSION_CLAIM'})
 if report['errors']or report['pending']or not origin['verified']:
  report['status']='FAIL'if report['errors']else'NOT_EVALUATED';report['eligible_for_draft_export']=False
 report['accepted']=False;report['release']=False
 return report
