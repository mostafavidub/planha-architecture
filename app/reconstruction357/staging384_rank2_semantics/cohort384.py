"""Pure exact finite comparison; caller gates current artifacts, no pinned-current loader."""
import ast,json,hashlib,copy
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
D=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def bind_intrinsic(r,f,i):
 m=r['candidate']['model'];e=i['evidence']
 if f['input_record_digest']!=D(r)or f['model_digest']!=D(m)or e['record_digest']!=D(r)or e['new_result_digest']!=D(f)or e['model_digest']!=D(m):raise ValueError('INTRINSIC_OWN_ARTIFACT_BINDING')
 if i['verdict']!='PASS'or i['eligible']is not True or len(i['rows'])!=18 or {x['id']for x in i['rows']}!={f'B{x:02}'for x in range(1,19)}or any(x['verdict']!='PASS'for x in i['rows']):raise ValueError('INTRINSIC_NOT_ELIGIBLE')
 return {'record_digest':D(r),'fresh_digest':D(f),'model_digest':D(m),'intrinsic_digest':D(i)}
def kernels():
 import comparison_metrics as metrics
 ns={'F':F,**{k:getattr(metrics,k)for k in('measure_model','route_metrics','rectangle_union_area')}}
 for path,names in [('finite_comparison358/q04_closure359.py',{'dimensions'}),('finite_comparison365/q04_closure365_v7.py',{'objective','compare'})]:
  nodes=[n for n in ast.parse((ROOT/path).read_text()).body if isinstance(n,ast.FunctionDef)and n.name in names]
  if {n.name for n in nodes}!=names:raise ValueError('UNCHANGED_COMPARISON_FUNCTIONS')
  exec(compile(ast.Module(body=nodes,type_ignores=[]),'<UNCHANGED_Q04>','exec'),ns)
 return ns

def verify_historical(historical,record):
 # Immutable historical identity plus exact model/brief rebinding for later current runs.
 authority=json.loads((Path(__file__).parent/'historical_authority.json').read_text());saved={}
 for name,spec in authority.items():
  raw=(ROOT.parent/spec['path']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=spec['sha256']:raise ValueError('HISTORICAL_AUTHORITY_PIN:'+name)
  saved[name]=json.loads(raw)
 if D(historical)!=D(saved['cohort']):raise ValueError('HISTORICAL_SUMMARY_IDENTITY')
 sr,sf=saved['record'],saved['fresh']
 if historical['binding']['record_digest']!=D(sr)or historical['binding']['fresh_digest']!=D(sf)or historical['prior381_result_digest']!=D(saved['roles']):raise ValueError('HISTORICAL_RUN_PROVENANCE')
 if D(sr['candidate']['model'])!=D(record['candidate']['model'])or sr['candidate']['request']!=record['candidate']['request']:raise ValueError('HISTORICAL_EXACT_CURRENT_MODEL_BRIEF')
 # Every own-fresh/eligibility receipt is checked anew, not inferred from summary flags.
 code=(ROOT/'staging382_cohort_binding_fix/cohort382.py').read_text();fn=next(n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef)and n.name=='evaluate')
 defs=ast.literal_eval(next(n.value for n in fn.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='definitions'for t in n.targets)))
 pairs={x['id']:x for x in historical['pairs']}
 if len(pairs)!=8 or set(pairs)!={x[0]for x in defs}:raise ValueError('HISTORICAL_PAIR_INVENTORY')
 if historical['binding']['model_digest']!=D(record['candidate']['model']):raise ValueError('HISTORICAL_CURRENT_MODEL_MISMATCH')
 ledger=json.loads((ROOT/'finite_comparison358/bound_comparison_actual358.json').read_text());first={x['id']:x for x in ledger['members']};receipts=[]
 for name,path,fp,ep in defs:
  raw=(ROOT/path).read_bytes();r=json.loads(raw);c=r['selected'][0]if name=='baseline351'else r['candidate'];pair=pairs[name]
  if c['request']!=record['candidate']['request']or any(c['model'][k]!=record['candidate']['model'][k]for k in('program','profile','inputs')):raise ValueError('HISTORICAL_SAME_BRIEF:'+name)
  if pair['artifact_sha256']!=hashlib.sha256(raw).hexdigest()or pair['model_digest']!=D(c['model']):raise ValueError('HISTORICAL_ARTIFACT:'+name)
  if name=='baseline351':
   e=first[name]['eligibility'];proof=e['result']
   if e['result_digest']!=D(proof)or first[name]['artifact_sha256']!=hashlib.sha256(raw).hexdigest():raise ValueError('BASELINE_LEDGER')
  else:
   f=json.loads((ROOT/fp).read_text());proof=json.loads((ROOT/'semantic_rules357'/ep).read_text())
   if f['input_record_digest']!=D(r)or f['model_digest']!=D(c['model'])or proof['evidence']['record_digest']!=D(r)or proof['evidence']['new_result_digest']!=D(f)or pair['historical_eligibility']['fresh_digest']!=D(f):raise ValueError('OWN_HISTORICAL_FRESH:'+name)
  if not proof['eligible']or proof['verdict']!='PASS'or proof['evidence']['model_digest']!=D(c['model'])or D(pair['historical_eligibility']['proof'])!=D(proof)or not pair['eligible']:raise ValueError('HISTORICAL_INTRINSIC:'+name)
  receipts.append({'id':name,'proof_digest':D(proof),'comparison_digest':D(pair['comparison'])})
 return receipts

def source_equivalence_checks(base,alternative,zero_core):
 bc=base['candidate']['packet']['core'];choice=alternative['trace']['enumeration'][0];bp=bc['balanced_portals365']
 keys=('entry_x','portal_y','slide_direction','selected_interval','operation_domains','portal_intervals')
 return {'full_proposal':D(base['trace']['proposal'])==D(alternative['trace']['proposal']),
 'all_nonselector_core_fields':{k:v for k,v in zero_core.items()if k!='balanced_portals365'}=={k:v for k,v in bc.items()if k!='balanced_portals365'},
 'geometry_consumed_selector_fields':all(choice[k]==bp[k]for k in keys),
 'base_core_digest':bp['source_base_core_digest']==zero_core['balanced_portals365']['source_base_core_digest'],
 'ownership_family':base['candidate']['packet']['family']==alternative['candidate']['packet']['family']}
def rank0_coverage(record,alternative):
 base=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());choice=alternative['trace']['enumeration'][0]
 from core378 import core
 zero=core(*map(F,record['candidate']['model']['inputs'][:2]),choice)
 checks=source_equivalence_checks(base,alternative,zero)
 code=(ROOT/'staging365_balanced_portals/assemble365.py').read_text();consumed=set()
 for node in ast.walk(ast.parse(code)):
  if isinstance(node,ast.Subscript)and isinstance(node.value,ast.Subscript)and isinstance(node.value.value,ast.Name)and node.value.value.id=='core'and isinstance(node.value.slice,ast.Constant)and node.value.slice.value=='balanced_portals365':
   if not isinstance(node.slice,ast.Constant):raise ValueError('DYNAMIC_SELECTOR_READ')
   consumed.add(node.slice.value)
 checks['exact_assembler_selector_readset']=consumed=={'portal_y','slide_direction'}
 return {'checks':checks,'covered':all(checks.values()),'baseline_model_digest':D(base['candidate']['model']),'core_source_digest':hashlib.sha256((ROOT/'staging378_finite_portals/core378.py').read_bytes()).hexdigest(),'assembler_source_digest':hashlib.sha256(code.encode()).hexdigest(),'full_proposal_digest':D(base['trace']['proposal']),'scope':'Existing actual balanced365 midpoint representative, full proposal equality and all non-selector core equality, unchanged assembler geometry selector readset. Cheap core reconstruction only, no candidate build.'}

def retained_terminals(h,record):
 from comparison_metrics import rectangle_union_area
 fb=h['full_band_current'];draft=h['draft366_conditional_property'];failed=h['failed364_retained'];mh=D(record['candidate']['model']);checks={}
 checks['fullband_current']=fb['current_model_digest']==mh and fb['terminal_state']=='EXCLUDED_ONLY_FROM_PROTECTED_NONDECREASING_OWNERSHIP_DOMAIN'and len(fb['rows'])==2 and {x['unit']for x in fb['rows']}=={'A','B'}and all(F(x['loss_exact_m2'])==F(x['current_exact_m2'])-F(x['alternative_exact_m2'])>0 for x in fb['rows'])and fb['global_infeasibility']is False
 checks['draft_current']=draft['current_model_digest']==mh and draft['conditional_dominance']=='FALSE_FOR_SUCCESSFUL_FIXED_SOURCE_PATH'and draft['status']=='UNASSESSED_NO_BUILD_NO_FRESH'and draft['eligibility']=='UNKNOWN'and F(draft['current'])==rectangle_union_area(record['candidate']['model']['common_spaces']['lobby'])and F(draft['alternative_if_success'])-F(draft['current'])==F(draft['worse_by'])>0
 checks['draft_sources']=all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in draft['source_proof']['source_readset'].items())
 r=json.loads((ROOT/'staging364_balanced_portals/actual364.json').read_text());d=json.loads((ROOT/'review364_diagnostic/geometry_operations.json').read_text())
 checks['failed364']=D(r)==failed['record_digest']and D(d)==failed['diagnostic_digest']and failed['operation_result']==d['door_operations']and any(x['code']=='PANEL_CONTINUOUS_WALL_COLLISION'for x in d['door_operations']['errors'])and failed['eligible']is False and failed['global_infeasibility_claimed']is False
 return {'checks':checks,'closed_in_declared_conditional_domain':all(checks.values()),'scope':'Protected ownership domain and fixed-source conditional non-dominance only; no global infeasibility or draft eligibility.'}

def compare_registered(record,fresh,intrinsic,alternative_record,alternative_fresh,alternative_intrinsic,historical):
 a=bind_intrinsic(record,fresh,intrinsic);b=bind_intrinsic(alternative_record,alternative_fresh,alternative_intrinsic)
 if record['candidate']['request']!=alternative_record['candidate']['request']or any(record['candidate']['model'][k]!=alternative_record['candidate']['model'][k]for k in('program','profile','inputs')):raise ValueError('SAME_BRIEF_PROGRAM_PROFILE')
 p=record['candidate']['packet']['core']['balanced_portals365'];q=alternative_record['candidate']['packet']['core']['balanced_portals365']
 if p.get('finite_rank378')!=1 or q.get('finite_rank378')!=2:raise ValueError('REGISTERED_PAIR_RANKS')
 choices=alternative_record['trace']['enumeration']
 if len(choices)!=3 or any(any(v.get(k)!=x for k,x in choices[j].items())for j,v in[(1,p),(2,q)]):raise ValueError('FINITE_MEMBERSHIP_BINDING')
 receipts=verify_historical(historical,record);cmp=kernels()['compare'](record['candidate']['model'],alternative_record['candidate']['model']);zero=rank0_coverage(record,alternative_record)
 terminals=retained_terminals(historical,record);remaining=[]
 if not terminals['closed_in_declared_conditional_domain']:remaining.append('RETAINED_TERMINAL_DOMAIN_UNVERIFIED')
 if not zero['covered']:remaining.append('RANK0_SOURCE_REPRESENTATIVE_NOT_BOUND')
 if cmp['dominance']!='FALSE':remaining.append('RANK2_DOMINANCE_NOT_REFUTED')
 if not all(x['comparison']['dominance']=='FALSE'for x in historical['pairs']):remaining.append('HISTORICAL_DOMINANCE_NOT_REFUTED')
 return {'schema':'REGISTERED_FINITE_CURRENT_COMPARISON384','binding':{**a,'run_id':record['trace']['run_id'],'candidate_id':record['candidate_id'],'review_id':fresh['review_id']},'alternative_binding':b,'rank2_comparison':cmp,'rank0_source_coverage':zero,'retained_terminal_audit':terminals,'historical_receipts_rechecked':receipts,'historical_evidence_digest':D(historical),'historical_comparisons_recomputed':False,'rank2_comparison_recomputed':True,'full_band_current':historical['full_band_current'],'draft366_conditional_property':historical['draft366_conditional_property'],'failed364_retained':historical['failed364_retained'],'finite_member_coverage':{'0':'EXISTING_ACTUAL365_SOURCE_REPRESENTATIVE'if zero['covered']else'UNKNOWN','1':'CURRENT_ACTUAL_INTRINSIC_ELIGIBLE','2':'ACTUAL383_INTRINSIC_ELIGIBLE'},'remaining':remaining,'full_q04_closed':not remaining,'verdict':'PASS_SCOPED_DECLARED_FINITE_Q04'if not remaining else'UNKNOWN_FINITE_Q04','global_optimum':False,'accepted':False}
