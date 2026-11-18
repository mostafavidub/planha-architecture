"""Additional rooted-branch evidence; never promotes whole-gate failure."""
from copy import deepcopy
from fractions import Fraction as F
from shared_gate140 import apply_shared_gate as group_gate,actual_root_hosts
from nonseating149 import require,check_packet
from private_branch_binding146 import examine

def evidence(packet,context):
 p=context['construction_trace']['proposal'];require(p,packet['core'])
 private=examine(packet['world_model'],packet['local_model'],packet['core'])
 if private.get('errors')or private.get('pending'):raise ValueError('BRANCH149_PRIVATE_SOURCE_BINDING:'+str(private))
 root=actual_root_hosts(packet['local_model'],p,packet['core'])
 if packet['family']!='LEFT_RIGHT':raise ValueError('BRANCH149_WORLD_FRAME')
 # Direct actual world-host bind, in addition to unchanged full world/frame gate.
 for uid,item in root['actual_local_units'].items():
  a,b,c,d=map(F,item['host_rect']);key=item['source_host']
  if tuple(map(F,packet['world_model']['wall_hosts'][key]))!=(b,a,d,c):raise ValueError('BRANCH149_WORLD_ROOT_HOST:'+uid)
 local_shell=tuple(map(F,packet['local_model']['wall_hosts']['right']));a,b,c,d=local_shell
 if tuple(map(F,packet['world_model']['wall_hosts']['right']))!=(b,a,d,c):raise ValueError('BRANCH149_WORLD_ROOT_SHELL')
 return {'private':private,'actual_root':root,'nonseating':check_packet(packet),'scope':'Root contact, branch source and no-through evidence; not comprehensive spatial quality.'}

def apply_shared_gate(packet,context,whole):
 g=deepcopy(group_gate(packet,context,whole))
 try:g['rooted_branch149']=evidence(packet,context)
 except Exception as ex:
  g['rooted_branch149']={'status':'FAIL','reason':str(ex)};g.setdefault('errors',[]).append('ROOTED_BRANCH149_FAILED:'+str(ex));g.update(status='FAIL',eligible_for_draft_export=False,accepted=False,release=False)
 return g
