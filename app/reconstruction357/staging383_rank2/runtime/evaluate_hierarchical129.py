"""Fresh hierarchical origin plus complete family-specific physical checks."""
from contract114 import digest
from construction_replay129 import verify

def evaluate(packet,context):
 model=packet['world_model'];trace=context.get('construction_trace',{});origin=verify(model,context);errors=[]
 for name,field in [('local_model','local_model_hash'),('core','core_hash')]:
  if digest(packet[name])!=trace.get(field):errors.append('HIERARCHICAL_PACKET_BINDING:'+name)
 if packet.get('family')!=trace.get('family'):errors.append('HIERARCHICAL_FAMILY_BINDING')
 if packet.get('admission_claim')is not False:errors.append('PRODUCER_ADMISSION_CLAIM')
 if packet.get('family')=='LEFT_RIGHT':
  from evaluate_world125 import evaluate_world
  report=evaluate_world(packet['local_model'],model,packet['core'],context)
 elif packet.get('family')=='FRONT_REAR':
  from checker114 import evaluate as whole
  report=whole(model,workflow_context=context)
 else:report={'errors':[],'pending':['UNSUPPORTED_HIERARCHICAL_FAMILY'],'status':'NOT_EVALUATED','eligible_for_draft_export':False}
 report['hierarchical_provenance129']=origin;report['errors']+=errors+origin['errors'];report['pending']+=origin['pending']
 if report['errors']or report['pending']or not origin['verified']:
  report['status']='FAIL'if report['errors']else'NOT_EVALUATED';report['eligible_for_draft_export']=False
 report['accepted']=False;report['release']=False
 return report
