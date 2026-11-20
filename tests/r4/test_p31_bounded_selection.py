"""Synthetic P31 proof/count tests, never a source of product qualification."""
import copy, itertools,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'studies'))
import p31_bounded_selection as p
def h(s):return p.digest(['SYNTHETIC_TEST',s])
def cx(mode=p.FIXTURE,n=6,final=90):return {'schema':'P31_SELECTION_CONTEXT_V1','mode':mode,'request_digest':h('req'),
 'source_digest':h('src'),'environment_digest':h('env'),'programme_digest':h('programme'),'budget_account_digest':h('budget'),
 'opened_tick':0,'cutoff_tick':100,'finalized_tick':final,'requested_count':n}
def row(c,k,*,state='HYPOTHETICAL_VALIDATED',parent=None,start=5,end=10):
 return {'schema':'P31_CANDIDATE_RECEIPT_V1','id':k,'model_digest':h(k),'request_context_digest':p.digest(c),
  'programme_digest':c['programme_digest'],'attempt_id':'try-'+k,'parent_id':parent,'start_tick':start,'end_tick':end,
  'state':state,'evidence_digest':h('evidence-'+k),**p.AUTH}
def pair(c,a,b,kind='VERIFIED_FIXTURE_DISTINCT'):
 a,b=sorted((a,b),key=lambda x:x['id'])
 return {'schema':'P31_FIXTURE_PAIR_PROOF_V1','context_digest':p.digest(c),'left_id':a['id'],'right_id':b['id'],
  'left_model':a['model_digest'],'right_model':b['model_digest'],'left_candidate_digest':p.digest(a),'right_candidate_digest':p.digest(b),
  'result':kind,'evidence_digest':h('pair:'+a['id']+b['id']),**p.AUTH}
def links(c,a,b):
 return {'schema':'P31_FIXTURE_LINEAGE_PROOF_V1','context_digest':p.digest(c),'parent_id':a['id'],'child_id':b['id'],
  'parent_model':a['model_digest'],'child_model':b['model_digest'],'parent_candidate_digest':p.digest(a),'child_candidate_digest':p.digest(b),
  'result':'VERIFIED_FIXTURE_REPLACEMENT','evidence_digest':h('linked'),**p.AUTH}
def manifest(c,rs,ps,ls,order=None):
 return {'schema':'P31_EXTERNAL_MANIFEST_V1','context_digest':p.digest(c),'candidate_order':list(rs) if order is None else order,
  'candidate_digests':{k:p.digest(v)for k,v in rs.items()},'pair_digests':{k:p.digest(v)for k,v in ps.items()},'lineage_digests':{k:p.digest(v)for k,v in ls.items()}}
def all_pairs(c,rows):
 return {p.pair_key(x['id'],y['id']):pair(c,x,y)for x,y in itertools.combinations(rows.values(),2)}
def observe(c,rs,ps=None,ls=None,m=None,want=None):
 ps={}if ps is None else ps;ls={}if ls is None else ls
 m=manifest(c,rs,ps,ls)if m is None else m
 return p.select(c,rs,ps,ls,trusted_manifest=m,expected_manifest_digest=p.digest(m)if want is None else want)
def why(out,k):return next(x['reason']for x in out['candidate_reasons']if x['id']==k)
class P31SelectionTest(unittest.TestCase):
 def test_six_requires_fifteen_and_does_not_report_product_qualified(self):
  c=cx();rs={k:row(c,k)for k in 'abcdefg'};before=p.digest(rs)
  out=observe(c,rs,all_pairs(c,rs))
  self.assertEqual(out['selected_hypothetical'],list('abcdef'));self.assertEqual(out['selected_pair_count'],15)
  self.assertEqual(out['qualified_count'],0);self.assertEqual(out['synthetic_count'],6)
  self.assertTrue(all(out[k]is False for k in p.AUTH));self.assertFalse(out['live_verifier_or_api_wired'])
  self.assertEqual(out['cutoff_tick_unchanged'],100);self.assertFalse(out['budget_reset'])
  self.assertEqual(why(out,'g'),'LIMIT_REACHED');self.assertEqual(p.digest(rs),before)
 def test_missing_fifteenth_never_filled(self):
  c=cx();rs={k:row(c,k)for k in 'abcdef'};ps=all_pairs(c,rs);ps.pop('e|f')
  o=observe(c,rs,ps)
  self.assertEqual(o['selected_pair_count'],10);self.assertEqual(o['synthetic_count'],5)
  self.assertEqual(why(o,'f'),'PAIR_MISSING')
 def test_unknown_is_not_duplicate_and_different_programme_not_compared(self):
  c=cx();rs={k:row(c,k)for k in 'abcd'};rs['c']['programme_digest']=h('other');rs['d']['state']='UNKNOWN'
  ps={'a|b':pair(c,rs['a'],rs['b'],'UNKNOWN')}
  o=observe(c,rs,ps)
  self.assertEqual([why(o,k)for k in 'bcd'],['PAIR_UNRESOLVED','DIFFERENT_PROGRAMME','CANDIDATE_UNKNOWN'])
  self.assertEqual(o['unfilled_fixture_slots'],5)
 def test_same_model_not_distinct_regardless_of_pair_claim(self):
  c=cx();rs={k:row(c,k)for k in 'ab'};rs['b']['model_digest']=rs['a']['model_digest']
  out=observe(c,rs,all_pairs(c,rs));self.assertEqual(why(out,'b'),'DUPLICATE_MODEL')
 def test_explicit_duplicate_distinct_from_unresolved(self):
  c=cx();rs={k:row(c,k)for k in 'ab'}
  ps={'a|b':pair(c,rs['a'],rs['b'],'VERIFIED_FIXTURE_DUPLICATE')}
  self.assertEqual(why(observe(c,rs,ps),'b'),'PAIR_VERIFIED_DUPLICATE')
 def test_pair_context_and_a_same_context_but_stale_candidate_receipt(self):
  c=cx();rs={k:row(c,k)for k in 'ab'};ps=all_pairs(c,rs)
  rs['b']['evidence_digest']=h('different receipt')
  self.assertEqual(why(observe(c,rs,ps),'b'),'PAIR_STALE_OR_WRONG_BINDING')
  ps=all_pairs(c,rs);ps['a|b']['context_digest']=h('other scope')
  self.assertEqual(why(observe(c,rs,ps),'b'),'PAIR_STALE_OR_WRONG_BINDING')
 def test_unchanged_external_manifest_not_minted_from_candidate(self):
  c=cx();rs={'a':row(c,'a',state='REJECTED')};m=manifest(c,rs,{},{});want=p.digest(m)
  rs['a']['state']='HYPOTHETICAL_VALIDATED'
  self.assertEqual(why(observe(c,rs,m=m,want=want),'a'),'CANDIDATE_UNPINNED_OR_CHANGED')
  with self.assertRaisesRegex(ValueError,'P31_UNTRUSTED_MANIFEST'):
   observe(c,rs,m=manifest(c,rs,{},{}),want=want)
 def test_even_pinned_positives_never_admit_archive_or_gate_strings(self):
  c=cx(p.ARCHIVE);rs={k:row(c,k)for k in 'ab'};rs['b']['state']='FOUR_CURRENT_CHECKS_COMPLETE_NOT_PRODUCT_QUALIFIED'
  o=observe(c,rs);self.assertEqual(o['selected_hypothetical'],[]);self.assertEqual(o['qualified_count'],0)
  self.assertEqual(why(o,'a'),'POSITIVE_AUTHORITY_UNWIRED_FOR_ARCHIVES');self.assertEqual(why(o,'b'),'CANDIDATE_UNKNOWN_STATE')
 def test_late_timeout_and_bad_clock_do_not_fill(self):
  c=cx(final=101);rs={'a':row(c,'a',end=100),'b':row(c,'b',end=99),'c':row(c,'c',end=102)}
  o=observe(c,rs)
  self.assertEqual([why(o,k)for k in 'abc'],['ATTEMPT_TIMEOUT','SELECTION_WINDOW_EXPIRED','UNBOUND_ATTEMPT_CLOCK'])
  self.assertEqual(o['synthetic_count'],0)
 def test_verified_child_can_replace_without_dual_count(self):
  c=cx(n=2);rs={'parent':row(c,'parent'),'child':row(c,'child',parent='parent',start=12,end=14)}
  self.assertEqual(why(observe(c,rs),'child'),'CHILD_RELATION_NOT_VERIFIED')
  a,b=rs.values();o=observe(c,rs,ls={'child':links(c,a,b)})
  self.assertEqual(o['selected_hypothetical'],['child']);self.assertEqual(why(o,'parent'),'PARENT_REPLACED_BY_VERIFIED_CHILD')
 def test_timed_out_or_unverified_child_does_not_replace_parent(self):
  c=cx(n=2);rs={'parent':row(c,'parent'),'child':row(c,'child',state='TIMEOUT',parent='parent',start=10,end=16)}
  a,b=rs.values();o=observe(c,rs,ls={'child':links(c,a,b)})
  self.assertEqual(o['selected_hypothetical'],['parent']);self.assertEqual(why(o,'child'),'ATTEMPT_TIMEOUT')
 def test_bound_relation_and_pair_checks_required_for_replacement(self):
  c=cx(n=2);rs={'other':row(c,'other'),'parent':row(c,'parent'),'child':row(c,'child',parent='parent',start=11,end=12)}
  a,b=rs['parent'],rs['child'];o=observe(c,rs,{'other|parent':pair(c,rs['other'],a)},{'child':links(c,a,b)})
  self.assertEqual(o['selected_hypothetical'],['other','parent']);self.assertEqual(why(o,'child'),'PAIR_MISSING')
  l=links(c,a,b);l['parent_model']=h('stale')
  o=observe(c,rs,{'other|parent':pair(c,rs['other'],a)},{'child':l})
  self.assertEqual(why(o,'child'),'CHILD_RELATION_NOT_VERIFIED')
 def test_reused_attempt_and_exact_boolean_flags(self):
  c=cx();rs={'a':row(c,'a'),'b':row(c,'b',state='TIMEOUT'),'c':row(c,'c')}
  rs['b']['attempt_id']=rs['a']['attempt_id'];rs['c']['qualified']=0
  o=observe(c,rs)
  self.assertEqual([why(o,k)for k in 'abc'],['REUSED_ATTEMPT_ID','REUSED_ATTEMPT_ID','CANDIDATE_MISSING_OR_INVALID'])
  self.assertEqual(o['synthetic_count'],0)
if __name__=='__main__':unittest.main()
