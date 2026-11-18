from copy import deepcopy
from shared_gate140 import apply_shared_gate as group_gate
from nonseating146 import require,check_packet

def apply_shared_gate(packet,context,whole):
 p=context['construction_trace']['proposal'];g=deepcopy(group_gate(packet,context,whole))
 try:require(p);g['nonseating146']=check_packet(packet)
 except Exception as ex:
  g['nonseating146']={'status':'FAIL','reason':str(ex)};g.setdefault('errors',[]).append('BRANCH146_NO_THROUGH_FAILED:'+str(ex));g.update(status='FAIL',eligible_for_draft_export=False,accepted=False,release=False)
 return g
