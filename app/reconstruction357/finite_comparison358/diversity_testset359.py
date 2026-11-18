"""Two actual source models, TEST_ONLY; not delivery or fabricated second option."""
from build_ledger import *
def graph(m):
 # Structural projection, NOT a claim to recovered TOPOLOGY_CANONICAL schema.
 return {'program':m['program'],'core_presence':sorted(m['common_spaces']),'unit_role_inventory':{u['id']:sorted(u['rooms'])for u in m['units']},'portal_edges':sorted([sorted(o['connects']) for o in m['openings']]),'private_group_membership':sorted([sorted(d['bedrooms'])for d in m['private_domains']]),'opening_role_types':sorted([(tuple(sorted(o['connects'])),o.get('kind',o.get('type')))for o in m['openings']])}
def run():
 members=[]
 for name,path in [('row358','staging358_comparative/row_candidate358.json'),('clamped359','staging359_hall_clamp/actual359.json')]:
  p=ROOT/path;x=json.loads(p.read_text());c=x['candidate'];t=x['trace'];assert digest(c)==t['candidate_digest'];assert digest(c['model'])==c['model_digest']==t['model_digest']
  members.append({'id':name,'path':path,'artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'model_digest':c['model_digest'],'record_digest':digest(x),'request':c['request'],'profile':c['model']['profile'],'role_graph_projection':graph(c['model']),'intrinsic_state':'REQUIRES_CURRENT_MODEL_GATE_BOUND_HERE_NOT_INFERRED_FROM_SOURCE_REPLAY'})
 a,b=members;assert a['request']==b['request'];same=digest(a['role_graph_projection'])==digest(b['role_graph_projection'])
 source=json.loads((ROOT.parent/'recovered233_rendered/sections.json').read_text());q=source['sections']['Q14']
 out={'schema':'TEST_ONLY_DIVERSITY_SET359','requested_count':a['request']['requested_count'],'k':2,'required_unordered_pairs':1,'members':members,'pairs':[{'ids':[a['id'],b['id']],'same_exact_role_graph_projection':same,'D4_enumeration_needed_to_prove_projection_equal':False if same else True,'verdict':'UNKNOWN_FULL_CANONICAL_SCHEMA_AND_MEMBER_GATE','distinctness_witness_present_in_projection':not same,'numeric_geometry_delta_not_counted_as_diversity':True}],'selected_for_delivery':False,'counted_distinct_deliverable_options':0,'request_fulfilled':False,'source':{'sha256':source['source_sha256'],'selector':q['source_selector'],'range':q['html_character_range'],'algorithm':q['fields']['رابطه و الگوریتم دقیق']},'limitations':['Projection equality is exact, not whole canonical equivalence proof','Whole Q14 requires all applicable own-program intrinsic gates and genuine program-or-organization witness','No false rejection from unsupported canonicalization; no fake second option from hall-length change']}
 Path(__file__).with_name('diversity_testset_actual359.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('pairs',1,'projection_equal',same,'delivered_options',0)
if __name__=='__main__':run()
