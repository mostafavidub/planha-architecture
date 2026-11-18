"""Engineering program preference, NOT owner capacity law or whole-quality proof.
Offline callers must retain the revision of preserved gate evidence; runtime
callers must freshly gate candidates before selection.
"""
import json
from three_access_diversity133 import describe,compare
POLICY='SUPPORTED_PROGRAM_SOURCE_ACCESS_DIVERSITY_134_V1'
def rank_roles(roles):
 # Only profiles already operationally supported in this release are ranked.
 if roles==['double','twin','twin']:return 3
 if roles==['double','twin']:return 2
 if roles==['double']:return 1
 return 0

def select(candidates,requested):
 if type(requested)is not int or not 1<=requested<=12:raise ValueError('REQUESTED_COUNT_INTEGER_1_TO_12')
 groups={};rejected=[]
 for i,c in enumerate(candidates):
  g=c.get('gate',{})
  if g.get('status')!='PASS_CONCEPT_SCOPED_REVIEW'or g.get('gate_scope')!='CONCEPT117_SOURCE_COMPAT_V1'or not g.get('eligible_for_draft_export')or g.get('errors')or g.get('pending'):
   rejected.append({'index':i,'reason':'WHOLE_GATE_NOT_ADMITTED','errors':g.get('errors'),'pending':g.get('pending')});continue
  try:d=describe(c)
  except (ValueError,KeyError,TypeError)as ex:rejected.append({'index':i,'reason':'SOURCE_DESCRIPTOR_BINDING','detail':str(ex)});continue
  actual={u['id']:[]for u in c['model']['units']}
  for row in d['source_witness']['source_rooms']:
   label=row['functional_label']
   if label.startswith('bedroom:'):actual[row['unit']].append(label.split(':',1)[1])
  programs=[sorted(v)for v in actual.values()]
  roles=programs[0]if programs else[]
  declared=c['model']['program']
  if any(v!=roles for v in programs)or sorted(declared.get('sleep_roles',[]))!=roles or declared.get('bedrooms_per_unit')!=len(roles):
   rejected.append({'index':i,'reason':'PROGRAM_METADATA_NOT_ACTUAL_SOURCE_INVENTORY','actual_roles':actual});continue
  priority=rank_roles(roles)
  if not priority:rejected.append({'index':i,'reason':'UNSUPPORTED_PROGRAM_FOR_THIS_POLICY','sleep_roles':roles});continue
  group=groups.setdefault(d['program_key'],{'sleep_roles':roles,'priority':priority,'admitted_indices':[],'representatives':[],'descriptors':[],'comparisons':[]})
  group['admitted_indices'].append(i);tests=[compare(old,d)for old in group['descriptors']];group['comparisons'].append({'index':i,'against_representatives':tests})
  if all(t['distinct']for t in tests):group['representatives'].append(i);group['descriptors'].append(d)
 best=max(groups.values(),key=lambda x:(x['priority'],len(x['representatives'])),default=None)
 from quality_tradeoffs129 import facts,rank
 tradeoffs={i:facts(candidates[i]['model'])for g in groups.values()for i in g['admitted_indices']}
 selected=sorted(best['representatives'],key=lambda i:rank(tradeoffs[i]))[:requested]if best else[]
 alternatives=[]
 for key,v in groups.items():
  alternatives.append({k:v[k]for k in ('sleep_roles','priority','admitted_indices','representatives','comparisons')}|{'selected_program':v is best,'program_key':key,'reason':'HIGHER_SUPPORTED_ADMITTED_PROGRAM_BEFORE_COUNT'if v is best and v['priority']>=2 else'EXPLICIT_SINGLE_BED_FALLBACK_NO_ADMITTED_HIGHER_SUPPORTED_GROUP'if v is best else'LOWER_SUPPORTED_PROGRAM_NOT_CHOSEN_DESPITE_OPTION_COUNT'})
 return {'measured_alternative_tradeoffs':{str(i):v for i,v in tradeoffs.items()},'same_program_ranking':'Engineering lexicographic worst-unit service route, worst-unit bed route, common floor, worst-unit circulation; no mandatory threshold or global optimality claim','policy':POLICY,'policy_source':'Explicit engineering selection direction: prefer actually gated supported actual-source program capacity3/2/1 before option count; not a bedroom/area law.','selected_indices':selected,'selected_sleep_roles':best['sleep_roles']if best else None,'selected_count':len(selected),'requested_count':requested,'shortfall':requested-len(selected),'program_alternatives':alternatives,'rejected':rejected,'whole_quality_or_capacity_suitability_verified':False,'verified_architectural_diversity':False}
