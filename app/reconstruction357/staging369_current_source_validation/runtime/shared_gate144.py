from copy import deepcopy
from shared_gate142 import apply_shared_gate as source_gate
from nonseating144 import require,check_model,check_packet

def apply_shared_gate(packet,context,whole):
 p=context.get('construction_trace',{}).get('proposal',{});g=source_gate(packet,context,whole)
 if 'nonseating_protection144'not in p:return g
 g=deepcopy(g)
 try:
  require(p);audits=check_packet(packet)
  g['nonseating144']=audits
 except Exception as exc:
  g['nonseating144']={'status':'FAIL','reason':str(exc)};g['status']='FAIL';g['eligible_for_draft_export']=False;g['accepted']=False;g['release']=False;g.setdefault('errors',[]).append('NONSEATING144_NOT_VERIFIED:'+str(exc))
 return g
