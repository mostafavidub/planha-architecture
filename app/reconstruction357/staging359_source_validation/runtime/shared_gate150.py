"""Source-kind and exact variant dispatch; no legacy sidecar alias for branches."""
from copy import deepcopy
from contract114 import digest
from nonseating149 import require as require_root
from nonseating146 import require as require_nonroot
from shared_gate140 import ROOT_MARKER,GROUP_MARKER
from shared_gate149 import apply_shared_gate as rooted_gate
from shared_gate146 import apply_shared_gate as nonroot_gate
from private_branch_binding146 import examine as private_binding
from shared_gate145 import apply_shared_gate as old_gate
KIND='PARALLEL_TWINS_BRANCH146'
def is_branch(packet,context):
 p=context.get('construction_trace',{}).get('proposal',{})
 branches={u+'.private_branch146.'+n for u in ('A','B')for n in ('bottom','upper_stem_right','branch_top','branch_end')}
 models=(packet.get('local_model',{}),packet.get('world_model',{}))
 return any((v.get('ordered_macro')or{}).get('kind')==KIND for v in (p,*models)) or any(branches.intersection(v.get('wall_hosts',{})) for v in models)
def apply_shared_gate(packet,context,whole):
 if not is_branch(packet,context):return old_gate(packet,context,whole)
 g=deepcopy(whole)
 try:
  p=context['construction_trace']['proposal'];marker=p.get('generation_method')
  if marker==ROOT_MARKER:
   require_root(p,packet['core']);g=rooted_gate(packet,context,whole);b=g['rooted_branch149'];private=b['private'];ns=b['nonseating'];root=b['actual_root']
   if root.get('status')!='PASS_EXACT_ACTUAL_ROOT140'or set(root.get('actual_local_units',{}))!={'A','B'}:raise ValueError('BRANCH150_ROOT_SOURCE_REQUIRED')
  elif marker==GROUP_MARKER:
   if 'rooted_service_study'in p:raise ValueError('BRANCH150_ROOT_METADATA_ON_NONROOT')
   require_nonroot(p);g=nonroot_gate(packet,context,whole)
   private=private_binding(packet['world_model'],packet['local_model'],packet['core']);ns=g['nonseating146']
   g['private_branch150']=private
  else:raise ValueError('BRANCH150_EXACT_VARIANT_MARKER_REQUIRED')
  shared=g['shared_group140']
  if shared.get('status')!='PASS_LIMITED_SHARED_GROUP140' or shared.get('local_model_hash')!=digest(packet['local_model'])or shared.get('world_model_hash')!=digest(packet['world_model'])or set(shared.get('units',{}))!={'A','B'}:raise ValueError('BRANCH150_SHARED_CURRENT_FRAMES')
  if private.get('status')!='PASS_SOURCE_BOUND_ACTUAL_PRIVATE_BRANCH146_ONLY'or private.get('errors')or private.get('pending'):raise ValueError('BRANCH150_PRIVATE_SOURCE_REQUIRED')
  if set(ns)!={'local_model','world_model'}:raise ValueError('BRANCH150_TWO_NONSEATING_FRAMES')
  for frame in ('local_model','world_model'):
   a=ns[frame]
   if a.get('status')!='PASS_NONSEATING_ZERO_GROUP_CROSS144'or a.get('errors')or a.get('model_hash')!=digest(packet[frame])or set(a.get('units',{}))!={'A','B'}:raise ValueError('BRANCH150_NONSEATING_CURRENT:'+frame)
 except Exception as exc:
  g=deepcopy(g);g['branch150_admission']={'status':'FAIL','reason':str(exc)};g.update(status='FAIL',eligible_for_draft_export=False,accepted=False,release=False);g.setdefault('errors',[]).append('BRANCH150_REQUIRED:'+str(exc))
 return g
