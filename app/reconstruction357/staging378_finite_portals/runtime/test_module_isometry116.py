"""Independent saved rigid-reflection audit, no producer/transform imports."""
import json,unittest
from pathlib import Path
from checker114 import F,digest
B=Path(__file__).parent/'evidence'
def point(p):return [F(6)-F(p[0]),F(p[1])]
def rectangle(r):return [F(6)-F(r[2]),F(r[1]),F(6)-F(r[0]),F(r[3])]
def q(v):return list(map(F,v))
class Reflection(unittest.TestCase):
 def test_actual_saved_physical_fields(self):
  a=json.loads((B/'module116_6x4.2.json').read_text());b=json.loads((B/'module116_6x4.2_reflected.json').read_text())
  self.assertEqual(b['isometry_binding']['base_module_hash'],digest(a))
  for group in ('walls','wall_hosts'):
   self.assertEqual(set(a[group]),set(b[group]))
   for k,r in a[group].items():self.assertEqual(rectangle(r),q(b[group][k]))
  for group in ('fixtures','activities'):
   for k,r in a['unit'][group].items():self.assertEqual(rectangle(r),q(b['unit'][group][k]))
  for k,rs in a['unit']['rooms'].items():self.assertEqual([rectangle(r)for r in rs],[q(r)for r in b['unit']['rooms'][k]])
  for k,ps in a['unit']['routes'].items():self.assertEqual([point(p)for p in ps],[q(p)for p in b['unit']['routes'][k]])
  for x,y in zip(a['openings'],b['openings']):self.assertEqual(rectangle(x['rect']),q(y['rect']))
  for x,y in zip(a['external_ports'],b['external_ports']):self.assertEqual(rectangle(x['rect']),q(y['rect']));self.assertEqual(point(x['center']),q(y['center']))
  def panel(x,y):
   for k in ('closed_panel','open_panel','rail_envelope'):
    self.assertEqual(rectangle(x[k]),q(y[k]))
   self.assertEqual([-F(x['translation'][0]),F(x['translation'][1])],q(y['translation']))
   for ss,tt in zip(x['states'],y['states']):
    for k in ('actor_rect','panel_rect'):self.assertEqual(rectangle(ss[k]),q(tt[k]))
    self.assertEqual(point(ss['hand_point']),q(tt['hand_point']))
   for ss,tt in zip(x['continuous_actor_segments'],y['continuous_actor_segments']):
    for k in ('actor_start','actor_end'):self.assertEqual(rectangle(ss[k]),q(tt[k]))
    for k in ('hand_start','hand_end'):self.assertEqual(point(ss[k]),q(tt[k]))
  for x,y in zip(a['operations']['doors'],b['operations']['doors']):panel(x,y)
  for x,y in zip(a['operations']['closets'],b['operations']['closets']):
   for pp,qq in zip(x['panels'],y['panels']):panel(pp,qq)
   self.assertEqual([rectangle(r)for r in x['shell_rects']],[q(r)for r in y['shell_rects']])
if __name__=='__main__':unittest.main()
