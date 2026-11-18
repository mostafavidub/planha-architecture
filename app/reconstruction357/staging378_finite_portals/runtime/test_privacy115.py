"""Privacy math/negative tests only; synthetic fixtures are NOT accepted plans."""
import unittest,copy,json
from pathlib import Path
from fractions import Fraction as F
from privacy115 import examine,separator,rect,digest

def model():
 walls={};rooms={};openings=[];doors=[]
 for role,x in [('bed1',F(0)),('bath',F(6))]:
  rooms[role]=[[str(x+F('.1')),'.1',str(x+F('5.9')),'5.9']]
  for k,r in {'bottom':[x,0,x+6,F('.1')],'top':[x,F('5.9'),x+6,6],'leftlo':[x,0,x+F('.1'),F('.3')],'lefthi':[x,F('1.3'),x+F('.1'),6],'right':[x+F('5.9'),0,x+6,6],'shield':[x+F('1.5'),F('.1'),x+F('1.6'),F('5.9')]}.items():walls[role+'.'+k]=list(map(str,r))
  oid='A.'+role+'.door';ap=list(map(str,[x,F('.3'),x+F('.1'),F('1.3')]))
  openings.append({'id':oid,'rect':ap,'connects':['A.living','A.'+role]});doors.append({'opening_id':oid,'closed_panel':ap,'open_panel':list(map(str,[x,F('1.3'),x+F('.1'),F('2.3')])),'translation':['0','1']})
 return {'units':[{'id':'A','rooms':rooms,'fixtures':{'bed1.bed':['3','2','5','3.6'],'shower_floor':['9','3','9.9','3.9']},'fixture_metadata':{'bed1.bed':{'kind':'bed'},'shower_floor':{'kind':'shower_floor'}},'activities':{'bed1.changing':['3','4','3.7','4.7'],'WC_front':['9','1','9.7','1.7'],'shower_use':['9','3','9.7','3.7']}}],'walls':walls,'wall_hosts':copy.deepcopy(walls),'common_spaces':{},'openings':openings,'operations':{'doors':doors}}

class PrivacyTests(unittest.TestCase):
 def test_all_ray_certificate_and_conditional_boundary(self):
  s=rect([0,0,1,1]);t=rect([3,0,4,1]);w=rect([2,-1,2.1,2]);self.assertTrue(separator(s,t,w));self.assertIsNone(separator(s,t,rect([2,0,2.1,1])));self.assertTrue(separator(s,t,rect([2,0,2.1,1]),True))
  m=model();r=examine(m);self.assertEqual(r['errors'],[]);self.assertEqual(r['pending'],[]);self.assertEqual(r['evidence']['strict_count'],5)
 def test_actual_open_state_not_closed_panel(self):
  m=model();del m['walls']['bed1.shield'];r=examine(m);self.assertTrue(any(e['code']=='PRIVATE_TARGET_VISIBLE_FROM_OPEN_APERTURE'for e in r['errors']))
  # A shut-door record is not a fully-open state and cannot certify visibility.
  m['operations']['doors'][0]['open_panel']=m['operations']['doors'][0]['closed_panel'];r=examine(m);self.assertTrue(any(e['code']=='PRIVACY_INVALID_OPEN_DOOR_STATE'for e in r['errors']))
 def test_private_targets_cannot_be_removed(self):
  m=model();del m['units'][0]['activities']['bed1.changing'];r=examine(m);self.assertTrue(any('CHANGING_TARGET_MISSING'in x for x in r['pending']));self.assertNotEqual(r['evidence']['status'],'PASS_SCOPED_PRIVACY')
  del m['units'][0]['fixtures']['shower_floor'];r=examine(m);self.assertTrue(any('shower_floor'in x for x in r['pending']))
 def test_precut_hosts_and_gross_closet_are_not_occluders(self):
  m=model();del m['walls']['bed1.shield'];m['units'][0]['fixtures']['bed1.closet']=['1.5','.1','1.6','5.9'];r=examine(m);self.assertTrue(any('ALL_RAYS_NOT_PROVEN'in x for x in r['pending']));self.assertNotEqual(r['evidence']['status'],'PASS_SCOPED_PRIVACY')
 def test_union_partition_and_binding_and_missing_operations(self):
  m=model();before=digest(m);r=examine(m);self.assertEqual(digest(m),before);q=copy.deepcopy(m);q['units'][0]['rooms']['bed1']=[['.1','.1','3','5.9'],['3','.1','5.9','5.9']];t=examine(q);self.assertEqual(r['errors'],t['errors']);self.assertEqual(r['pending'],t['pending']);self.assertNotEqual(r['evidence']['model_hash'],t['evidence']['model_hash']);q['operations']={};self.assertTrue(any('OPEN_DOOR_STATE_MISSING'in x for x in examine(q)['pending']))

if __name__=='__main__':unittest.main()
