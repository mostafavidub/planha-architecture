"""Additional source-bound local group evidence. Never promotes a whole-gate failure."""
from copy import deepcopy
from contract114 import digest
from coarse_sidecar_group138 import validate_group_exact
from shared_producer137 import propose as propose_local
from shared_binding137 import check as check_local
GROUP_MARKER='SIDECAR_OPPOSING_GROUP138_LOCAL_CONNECTION_PENDING'
ROOT_MARKER='SIDECAR_RIGHT_ROOTED_GROUP139_LOCAL_CONNECTION_PENDING'
TRACE='CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1'
def needs_group(p):
 return p.get('generation_method')in (GROUP_MARKER,ROOT_MARKER) or 'opposing_group_study'in p or 'shared_body_witness'in p or 'rooted_service_study'in p

def require_runtime_group_proposal(p,expected_marker=None,core=None):
 marker=p.get('generation_method')
 if marker not in (GROUP_MARKER,ROOT_MARKER)or(expected_marker is not None and marker!=expected_marker):raise ValueError('GROUP140_METHOD_REQUIRED')
 metadata=p.get('opposing_group_study',{})
 if type(metadata.get('gap_bodies'))is not int or metadata['gap_bodies']!=2:raise ValueError('GROUP140_RUNTIME_TWO_BODY_BAND_REQUIRED')
 errors=validate_group_exact(p['rectangles'],p['shared_body_witness'],metadata)
 if errors:raise ValueError('GROUP140_EXACT_GEOMETRY:'+','.join(errors))
 if marker==ROOT_MARKER:
  if core is None:raise ValueError('ROOT140_CORE_REQUIRED')
  reconstruct_root(p,core)
 elif 'rooted_service_study'in p:raise ValueError('UNEXPECTED_ROOT_METADATA_ON_GROUP138')

def reconstruct_root(p,core):
 from bathroom_module117 import build
 from rooted_bath139 import anchor,validate
 module=build('4.3','3.1');box=core['units']['A'];contract=anchor(module,box);audit=validate(module,box,p['rectangles']['bath'])
 if audit.get('status')!='EXACT_RIGHT_SOURCE_CONTACT':raise ValueError('ROOT140_EXACT_SOURCE_CONTACT_FAILED')
 if p.get('rooted_service_study')!={'contract':contract,'audit':audit}:raise ValueError('ROOT140_METADATA_BINDING')
 return audit

def actual_root_hosts(local,p,core):
 from fractions import Fraction as F
 from contract114 import S
 audit=reconstruct_root(p,core);a,b,c,d=map(F,audit['host_rect']);L=F(local['inputs'][1]);face=F(audit['root_face_x']);hosts=local['wall_hosts'];shell=tuple(map(F,hosts['right']))
 if shell[0]!=face or not shell[2]>face:raise ValueError('ROOT140_ACTUAL_SHELL_FACE')
 out={}
 for uid,q in [('A',(a,b,c,d)),('B',(a,L-d,c,L-b))]:
  key=uid+'.bath.'+audit['source_host']
  if tuple(map(F,hosts[key]))!=q:raise ValueError('ROOT140_ACTUAL_SOURCE_HOST:'+uid)
  contact=min(q[3],shell[3])-max(q[1],shell[1])
  if q[2]!=shell[0]or contact<=0:raise ValueError('ROOT140_POSITIVE_SHELL_CONTACT:'+uid)
  out[uid]={'source_host':key,'host_rect':list(map(S,q)),'contact_length_m':S(contact)}
 return {'status':'PASS_EXACT_ACTUAL_ROOT140','source_audit':audit,'actual_local_units':out}

def shared_evidence(packet,ctx):
 trace=ctx['construction_trace'];p=trace['proposal'];require_runtime_group_proposal(p,core=packet['core'])
 if trace.get('schema')!=TRACE or packet.get('family')!='LEFT_RIGHT' or trace.get('family')!='LEFT_RIGHT':raise ValueError('GROUP140_LOCAL_FRAME_REQUIRED')
 for key,field in [('local_model','local_model_hash'),('world_model','model_hash'),('core','core_hash')]:
  if digest(packet[key])!=trace.get(field):raise ValueError('GROUP140_TRACE_BINDING:'+key)
 local=packet['local_model'];units=local['units']
 if len(units)!=2 or sorted(u['id']for u in units)!=['A','B']:raise ValueError('GROUP140_TWO_UNIQUE_UNITS_REQUIRED')
 root=actual_root_hosts(local,p,packet['core'])if p['generation_method']==ROOT_MARKER else None
 audits={}
 for uid in ('A','B'):
  proposed=propose_local(local,uid,p)
  if proposed.get('audit',{}).get('status')!='LOCAL_STUDY_PASS_NOT_FULL_GATE':raise ValueError('GROUP140_LOCAL_PROPOSAL_FAILED:'+uid+':'+str(proposed.get('status')))
  evidence=proposed['packet'];audit=check_local(local,uid,p,evidence)
  if audit.get('status')!='LOCAL_STUDY_PASS_NOT_FULL_GATE' or audit.get('model_hash')!=digest(local) or audit.get('packet_hash')!=digest(evidence):raise ValueError('GROUP140_FRESH_LOCAL_BINDING:'+uid)
  audits[uid]={'packet':evidence,'audit':audit}
 return {'status':'PASS_LIMITED_SHARED_GROUP140','local_model_hash':digest(local),'world_model_hash':digest(packet['world_model']),'units':audits,'rooted_source_contact':root,'scope':'Local-frame witness bound to the same hierarchical world gate; not a world-witness schema, comfort or comprehensive quality approval.'}

def apply_shared_gate(packet,ctx,whole):
 trace=ctx.get('construction_trace',{});proposal=trace.get('proposal',{})
 if not needs_group(proposal):return whole
 g=deepcopy(whole)
 try:g['shared_group140']=shared_evidence(packet,ctx)
 except Exception as ex:
  g['shared_group140']={'status':'FAIL','reason':type(ex).__name__+':'+str(ex)}
  g.setdefault('errors',[]).append('SHARED_GROUP140_NOT_VERIFIED:'+str(ex));g['status']='FAIL';g['eligible_for_draft_export']=False;g['accepted']=False;g['release']=False
 return g
