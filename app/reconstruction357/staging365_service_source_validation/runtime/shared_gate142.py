"""Additional D4 evidence, never replaces or promotes the existing whole gate."""
from copy import deepcopy
from seating_binding142 import MARKER,evidence
from shared_gate140 import apply_shared_gate as old_gate

def apply_shared_gate(packet,context,whole):
 p=context.get('construction_trace',{}).get('proposal',{})
 if p.get('generation_method')!=MARKER and 'compact_d4_sources142'not in p:return old_gate(packet,context,whole)
 g=deepcopy(whole)
 try:g['compact_group142']=evidence(packet,context)
 except Exception as exc:
  g['compact_group142']={'status':'FAIL','reason':type(exc).__name__+':'+str(exc)}
  g.setdefault('errors',[]).append('COMPACT142_SOURCE_LOCAL_WORLD_FAILED:'+str(exc));g['status']='FAIL';g['eligible_for_draft_export']=False;g['accepted']=False;g['release']=False
 return g
