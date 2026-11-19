import copy,pathlib,tempfile,unittest
from unittest.mock import patch,Mock
import codec_environment402 as e
class Environment(unittest.TestCase):
 def rejected_before_codec(self,ctx,code):
  sentinel=Mock()
  with ctx:
   with self.assertRaisesRegex(ValueError,code):e.gated(sentinel)
  sentinel.assert_not_called()
 def test_actual_environment(self):
  r=e.verify_environment();self.assertEqual(len(r['versions']),5);self.assertFalse(r['os_image_immutable'])
 def test_python_patch_before_codec(self):
  self.rejected_before_codec(patch.object(e.platform,'python_version',return_value='3.11.0'),'PYTHON_PATCH')
 def test_wrong_package_before_codec(self):
  self.rejected_before_codec(patch.object(e.md,'version',return_value='0.0'),'PACKAGE_VERSION')
 def test_wrong_arch_before_codec(self):
  self.rejected_before_codec(patch.object(e.platform,'machine',return_value='aarch64'),'PLATFORM_ARCH')
 def test_wrong_abi_before_codec(self):
  self.rejected_before_codec(patch.object(e.sysconfig,'get_config_var',return_value='other'),'PYTHON_ABI')
 def test_no_venv_before_codec(self):
  self.rejected_before_codec(patch.object(e.sys,'prefix',e.sys.base_prefix),'ISOLATED_VENV_REQUIRED')
 def test_import_outside_venv_before_codec(self):
  from types import SimpleNamespace
  self.rejected_before_codec(patch.object(e.importlib,'import_module',return_value=SimpleNamespace(__file__='/tmp/outside-module.py')),'PACKAGE_IMPORT_OUTSIDE_VENV')
 def test_source_tamper_before_codec(self):
  original=pathlib.Path.read_bytes
  victim=e.ROOT/'studies/r4/paired_codec308.py'
  def altered(p):
   return b'changed' if p==victim else original(p)
  self.rejected_before_codec(patch.object(pathlib.Path,'read_bytes',altered),'CODEC_SOURCE_CHANGED')
 def test_lock_tamper_before_codec(self):
  original=pathlib.Path.read_bytes
  def altered(p):return b'{}' if p==e.LOCK else original(p)
  self.rejected_before_codec(patch.object(pathlib.Path,'read_bytes',altered),'ENVIRONMENT_LOCK_CHANGED')
 def test_wheel_corruption(self):
  lock=e.load_lock()
  with tempfile.TemporaryDirectory()as d:
   for row in lock['packages']:(pathlib.Path(d)/row['filename']).write_bytes(b'not a wheel')
   with self.assertRaisesRegex(ValueError,'WHEEL_HASH'):e.verify_wheels(d)
 def test_missing_wheels(self):
  with tempfile.TemporaryDirectory()as d:
   with self.assertRaisesRegex(ValueError,'WHEEL_SET'):e.verify_wheels(d)
 def test_shadow_repo_import_before_codec(self):
  from types import SimpleNamespace
  fixture=Mock();assess=Mock()
  shadow=SimpleNamespace(__file__='/tmp/shadow.py',fixture=fixture,assess=assess)
  shadow.svg=shadow;shadow.dxf=shadow
  with patch.object(e.importlib,'import_module',return_value=shadow):
   with self.assertRaisesRegex(ValueError,'REPO_IMPORT_PATH'):e.paired()
  fixture.assert_not_called();assess.assert_not_called()
 def test_shadow_encoder_before_codec(self):
  from types import SimpleNamespace
  fm=e.importlib.import_module('test_dxf_codec_study307');real=e.importlib.import_module('paired_codec308')
  encoder=Mock();shadow=SimpleNamespace(__file__='/tmp/shadow-codec.py',encode=encoder)
  pair=SimpleNamespace(__file__=real.__file__,assess=real.assess,make_report=real.make_report,svg=shadow,dxf=real.dxf)
  with patch.object(e.importlib,'import_module',side_effect=[fm,pair]):
   with self.assertRaisesRegex(ValueError,'REPO_IMPORT_PATH'):e.paired()
  encoder.assert_not_called()
 def test_baseline_mismatch(self):
  value=copy.deepcopy(e.load_lock()['baseline_pair']['expected']);value['svg_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'BASELINE_PAIR_NOT_REPRODUCED'):e.verify_baseline(value)
 def test_post_execution_change(self):
  observed=e.verify_environment();altered=copy.deepcopy(observed);altered['lock_digest']='changed'
  with patch.object(e,'verify_environment',side_effect=[observed,altered]):
   with self.assertRaisesRegex(ValueError,'ENVIRONMENT_CHANGED_AFTER_CODEC'):e.gated(lambda:None)
if __name__=='__main__':unittest.main()
