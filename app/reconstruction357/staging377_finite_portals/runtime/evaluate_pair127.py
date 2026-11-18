"""Fresh multi-proposal provenance AND whole physical gate; no receipt merge."""
from copy import deepcopy
from contract114 import digest
from construction_replay127 import verify

def evaluate(packet,context):
 model=packet['world_model'];trace=(context or {}).get('construction_trace',{})
 provenance=verify(model,context);binding=[]
 if packet.get('family')!=trace.get('family'):binding.append('PAIR_FAMILY_BINDING')
 for key,field in [('local_model','local_model_hash'),('core','core_hash')]:
  if digest(packet[key])!=trace.get(field):binding.append('PAIR_PACKET_BINDING:'+key)
 if packet.get('unit_proposal_hashes')!=trace.get('unit_proposal_hashes'):binding.append('PAIR_ASSIGNMENT_BINDING')
 if packet.get('admission_claim')is not False:binding.append('PRODUCER_ADMISSION_CLAIM')
 if packet.get('family')=='LEFT_RIGHT':
  from evaluate_world125 import evaluate_world
  report=evaluate_world(packet['local_model'],model,packet['core'],context)
 elif packet.get('family')=='FRONT_REAR':
  from checker114 import evaluate as check
  report=check(model,workflow_context=context)
 else:report={'status':'NOT_EVALUATED','errors':[],'pending':['UNSUPPORTED_PAIR_FAMILY'],'eligible_for_draft_export':False}
 report['multiproposal_provenance127']=provenance
 report['errors']+=provenance['errors']+binding;report['pending']+=provenance['pending']
 if not provenance['verified']or binding or report['errors']or report['pending']:
  report['eligible_for_draft_export']=False;report['status']='FAIL'if report['errors']else'NOT_EVALUATED'
 report['accepted']=False;report['release']=False
 return report
