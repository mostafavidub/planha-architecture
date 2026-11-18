"""Stored readset comparison, separate B eligibility and functional dominance."""
from build_ledger import *
import importlib
from fractions import Fraction as F
from operationalization import compare
H=ROOT/'semantic_rules357'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 x=json.loads((ROOT/'actual_run/actual_response.json').read_text())
 specs=[('baseline351',x['selected'][0],x['central_fresh_reviews'][0],'eligibility_intrinsic357_v2',{'source_profile':'SOURCE351'}),('translated357',json.loads((ROOT/'staging357_comparative/attached_service_final357.json').read_text()),json.loads((ROOT/'review357_source_identity/result.json').read_text()),'eligibility_intrinsic357',{}),('row358',json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text()),json.loads((ROOT/'review358_source_validation/result.json').read_text()),'eligibility_intrinsic358',{})]
 ledger=build(); models={}
 for member,(name,record,result,module,kw) in zip(ledger['members'],specs):
  gate=importlib.import_module(module).evaluate(record,result,seconds=30,**kw)
  candidate=record if name=='baseline351' else record['candidate']; model=candidate['model'];models[name]=model
  assert digest(model)==member['model_digest']
  if gate['evidence'].get('record_digest')!=digest(record) or gate['evidence'].get('new_result_digest')!=digest(result):raise ValueError('GATE_ARTIFACT_BINDING')
  member['eligibility']={'result':gate,'evaluator_sha256':sha(H/(module+'.py')),'result_digest':digest(gate),'record_digest':digest(record),'fresh_result_digest':digest(result)}
  member['terminal_state']='ELIGIBLE_SCOPED_B18' if gate['eligible']else 'UNKNOWN_EVIDENCE'
  member['reason']='INTRINSIC_DECLARED_PROFILE_ONLY_NOT_FINAL_PURPOSE_OR_COMPARATIVE_PROTECTED_VECTOR'
  member['bedroom_route_metrics']={}
  for u in model['units']:
   member['bedroom_route_metrics'][u['id']]={}
   for name,p in u['routes'].items():
    if name.startswith(('bed1.','bed2.','bed3.')):
     # Each source route begins at entry. Composite paths are declared via-entry,
     # not shortest paths nor a claim that dispersed private grouping is justified.
     l=F(member['metrics']['units'][u['id']]['routes'][name]['length'])
     member['bedroom_route_metrics'][u['id']][name]={'target_to_entry_m':str(l),'target_to_WC_via_entry_m':str(l+F(member['metrics']['units'][u['id']]['routes']['WC_use']['length'])),'scope':'LENGTH_OF_EXISTING_SOURCE_ROUTES_VIA_ENTRY_NOT_SHORTEST_OR_PRIVATE_GROUP_JUSTIFICATION'}
 for field in ['request','profile']:
  vals=[models[k].get(field) for k in models]
  ledger['same_'+field]=all(digest(v)==digest(vals[0]) for v in vals) if field=='profile' else all(digest((r if n=='baseline351'else r['candidate'])['request'])==digest(specs[0][1]['request'])for n,r,_,_,_ in specs)
 contract=ROOT/'staging274_evaluator_transport_fix/quality_contract.json'; qc=json.loads(contract.read_text())
 ledger['owner_derived_source274']={'path':str(contract.relative_to(ROOT)),'sha256':sha(contract),'status':qc['status'],'source_inventory':qc['source_inventory'],'rules':[v for v in qc['rules']if v['id']in ('SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS')]}
 eligible=[m for m in ledger['members'] if m['terminal_state']=='ELIGIBLE_SCOPED_B18']
 ledger['service_scoped_measurement']={}
 for unit in ['A','B']:
  vals={m['id']:m['metrics']['units'][unit]['bath_wc_union_m2'] for m in eligible}; smallest=min(map(F,vals.values())) if vals else None
  ledger['service_scoped_measurement'][unit]={'bath_WC_m2':vals,'smallest_B18_tested_service_room_m2':str(smallest),'room_area_excess_m2':{k:str(F(v)-smallest)for k,v in vals.items()},'exclusive_service_circulation_area':'UNKNOWN_ROLE_ATTRIBUTION','not_global_minimum':True,'whole_service_parent':'UNKNOWN'}
 ledger['partial_Q04_pair_vectors']=[]
 for a in eligible:
  for b in eligible:
   if a['id']==b['id']:continue
   definitions={}; av={};bv={}
   for u in a['metrics']['units']:
    am=a['metrics']['units'][u];bm=b['metrics']['units'][u]
    values=[('declared_circulation_union','exclusive_circulation_area_m2',am['declared_circulation_union_m2'],bm['declared_circulation_union_m2'])]
    for route in sorted(set(am['routes']) & set(bm['routes'])):
     ar=am['routes'][route];br=bm['routes'][route]
     if 'length' not in ar or 'length' not in br:continue
     values += [(route+'/length','path_length_m',ar['length'],br['length']),(route+'/turns','turn_count',ar['direction_changes'],br['direction_changes'])]
    for name,metric,aa,bb in values:
     key=u+'/'+name;d={'metric':metric,'role':'objective','unit':u,'scenario':'DECLARED_SOURCE_ROUTE','source_pointer':'rendered233/Q04'};definitions[key]=d
     av[key]={'value':aa,'definition':d,'readset_digest':a['model_digest']};bv[key]={'value':bb,'definition':d,'readset_digest':b['model_digest']}
   ledger['partial_Q04_pair_vectors'].append({'baseline':a['id'],'alternative':b['id'],'measurement':compare(av,bv,definitions),'scope':'PARTIAL_OBJECTIVE_VECTOR_ONLY_NOT_NECESSITY_NO_PROTECTED_METRICS','missing_dimensions':['bottleneck_count','protected_functional_vector','component_necessity']})
 ledger['rule_outcomes']={
 'Q04':{'state':'UNKNOWN','measured':'declared circulation union and actual all-target lengths/turns','missing':['COMPONENT_DESTINATION_NECESSITY','SOURCE_PROFILE_BOTTLENECK_COUNTS','PROTECTED_FUNCTIONAL_VECTOR'],'B18_dependency_closed':len(eligible)==3},
 'IR_P13':{'state':'BOUNDED_PARTIAL_COMPARISON','hard_failure_from_rank':False,'measured':'per-bedroom source target to entry and WC via entry route lengths','missing':['ACTUAL_PRIVATE_CONNECTIVITY_GRAPH','BEDROOM_TO_PUBLIC_TARGET_ROUTE','CLOSET_ORIENTATION_APPLICABILITY_AND_ALTERNATIVES','PROTECTED_USEFUL_LIVING_VECTOR']},
 'SERVICE_COMPACTNESS':{'state':'UNKNOWN','measured':'tested B18 room-area baseline and zero/nonzero excess independently each unit','missing':['EXCLUSIVE_SERVICE_CIRCULATION_ROLE_MEASUREMENT']},
 'COMMON_CORE_COMPACTNESS':{'state':'UNKNOWN','measured':'common areas,actual entry access length/turns and per-unit distance spread','missing':['STAGING_FUNCTION_PURPOSE','ACTUAL_CORE_ALTERNATIVE_BRANCH_PROOF','PROTECTED_FUNCTIONAL_VECTOR']}}
 ledger['missing']=['RULE_SPECIFIC_MISSING_LISTS_ABOVE'];ledger['schema']='FINITE358_BOUND_B18_COMPARISON_NOT_PARENT_ACCEPTANCE';ledger['closed_applicable_comparison']=False
 corefile=Path(__file__).with_name('core_branch_bound358.json')
 if corefile.exists():
  proof=json.loads(corefile.read_text());artifact=ROOT/proof['artifact']
  if sha(artifact)!=proof['artifact_sha256'] or proof['model_digest']!=digest(models['row358']):raise ValueError('CORE_BRANCH_PROOF_BINDING')
  ledger['unconstructed_branches']=[{'id':'source114_full_band_core','terminal_state':proof['terminal_state'],'proof':proof,'not_erased':True,'unsupported_full_plan_adapter_retained':True}]
  ledger['rule_outcomes']['COMMON_CORE_COMPACTNESS']['missing'].remove('ACTUAL_CORE_ALTERNATIVE_BRANCH_PROOF')
  ledger['rule_outcomes']['COMMON_CORE_COMPACTNESS']['bounded_branch_proof']='core_branch_bound358.json'
 Path(__file__).with_name('bound_comparison_actual358.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2));print([(m['id'],m['terminal_state'])for m in ledger['members']])
if __name__=='__main__':main()
