"""Saved-model independent negatives; no solving or generation."""
import copy,json
from pathlib import Path
from checker114 import evaluate
from operation_check114 import source_nonleaf117
ROOT=Path(__file__).parent

def run():
 m=json.loads((ROOT/'evidence/general117_complete_explicit2.json').read_text())['internal_proposals'][0]['model']
 results={};r=evaluate(m)
 assert r['status']=='PASS_CONCEPT_SCOPED_REVIEW' and not r['errors'] and not r['pending']
 assert len(r['not_evaluated'])==3 and not r['accepted'] and not r['release']
 results['positive']={'status':r['status'],'model_hash':r['model_hash'],'unknowns':r['not_evaluated']}
 # A flag cannot turn a private opening into a source-backed permanent arch.
 n=copy.deepcopy(m);p=next(p for p in n['openings']if '.bed' in p['id']);oid=p['id'];p.update(kind='permanent_open_arch',hardware=None)
 n['operations']['doors']=[d for d in n['operations']['doors']if d['opening_id']!=oid]
 assert not source_nonleaf117(n,p)
 q=evaluate(n);assert q['errors'] or q['pending'];results['private_relabel']={'errors':q['errors'],'pending':q['pending']}
 n=copy.deepcopy(m);p=next(p for p in n['openings']if p['id']=='lift.entry');p['connects']=['A.bed1','lobby'];assert not source_nonleaf117(n,p)
 q=evaluate(n);assert q['errors']or q['pending'];results['core_private_relabel']={'errors':q['errors'],'pending':q['pending']}
 n=copy.deepcopy(m);pl=next(p for p in n['module_placements']if p['module']['schema']=='BATHROOM_MODULE117');pl['module_hash']='0'*64
 q=evaluate(n);assert q['errors'];results['bath_source_tamper']={'errors':q['errors']}
 n=copy.deepcopy(m);op=next(d for d in n['operations']['doors']if d.get('kind')=='pocket_source113');op['continuous_actor_segments']=[]
 q=evaluate(n);assert q['errors']or q['pending'];results['pocket_actor_removed']={'errors':q['errors'],'pending':q['pending']}
 n=copy.deepcopy(m);wid=next(k for k in n['walls']if 'privacy_screen'in k);del n['walls'][wid]
 q=evaluate(n);assert q['errors']or q['pending'];results['actual_privacy_screen_removed']={'errors':q['errors'],'pending':q['pending']}
 (ROOT/'evidence/final_scope117_mutations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print('PASS: saved whole + five independent mutation checks')
if __name__=='__main__':run()
