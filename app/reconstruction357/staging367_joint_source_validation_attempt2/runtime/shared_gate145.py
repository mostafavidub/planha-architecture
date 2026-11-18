"""Runtime145 requires circulation policy for every compact D4 candidate.
The old 142 marker is retained by source144, so marker alone must not bypass
its mandatory new policy. Never promotes whole/source gate failures.
"""
from copy import deepcopy
from contract114 import digest
from seating_binding142 import MARKER
from nonseating144 import require
from shared_gate144 import apply_shared_gate as circulation_gate

def apply_shared_gate(packet,context,whole):
 p=context.get('construction_trace',{}).get('proposal',{})
 compact=p.get('generation_method')==MARKER or 'compact_d4_sources142'in p or 'nonseating_protection144'in p
 if not compact:return circulation_gate(packet,context,whole)
 g=deepcopy(whole)
 try:
  # Require even if attacker strips policy, marker or one metadata field.
  require(p)
  g=circulation_gate(packet,context,whole)
  audits=g.get('nonseating144',{})
  if set(audits)!={'local_model','world_model'}:raise ValueError('RUNTIME145_BOTH_FRAME_RECEIPTS_REQUIRED')
  for frame in ('local_model','world_model'):
   a=audits[frame]
   if a.get('status')!='PASS_NONSEATING_ZERO_GROUP_CROSS144'or a.get('errors')or a.get('model_hash')!=digest(packet[frame])or set(a.get('units',{}))!={'A','B'}:raise ValueError('RUNTIME145_CURRENT_NONSEATING_RECEIPT:'+frame)
 except Exception as exc:
  g=deepcopy(g);g['nonseating145_admission']={'status':'FAIL','reason':str(exc)};g['status']='FAIL';g['eligible_for_draft_export']=False;g['accepted']=False;g['release']=False;g.setdefault('errors',[]).append('RUNTIME145_NONSEATING_REQUIRED:'+str(exc))
 return g
