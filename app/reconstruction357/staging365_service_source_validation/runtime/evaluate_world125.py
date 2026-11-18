"""Composed fresh physical world admission. No producer receipts accepted."""
from copy import deepcopy
from contract114 import digest
from world_inventory125 import examine
from frame_audit125 import evaluate_core

def evaluate_world(local_model,world_model,core,workflow_context=None):
 inv=examine(local_model,world_model,core);frame=evaluate_core(core)
 context=deepcopy(workflow_context)if workflow_context else None
 if context is not None:context['frame_core125']=deepcopy(core);context['frame_local129']=deepcopy(local_model)
 from checker114 import evaluate
 report=evaluate(world_model,workflow_context=context)
 report['world_inventory125']=inv;report['common_frame125']=frame
 report['errors']+=inv['errors']+frame['errors'];report['pending']+=inv['pending']
 if inv['errors']or frame['errors']or inv['pending']:
  report['status']='FAIL'if report['errors']else'NOT_EVALUATED';report['eligible_for_draft_export']=False
 report['accepted']=False;report['release']=False
 return report
