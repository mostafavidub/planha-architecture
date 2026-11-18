import sys,json,hashlib,traceback,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];H=Path(__file__).resolve().parent
p=H/'prereg.json';expected=sys.argv[1]
if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise ValueError('PREREG_CHANGED')
pins=json.loads(p.read_text())['files']
for n,h in pins.items():
 if hashlib.sha256((R/n).read_bytes()).hexdigest()!=h:raise ValueError('PREIMPORT_PIN:'+n)
sys.path.insert(0,str(R/'semantic_rules357'))
try:
 import test_role_registry_final_joint367_v4 as tests
 suite=unittest.defaultTestLoader.loadTestsFromModule(tests)
 with (H/'test_log.txt').open('x')as stream:result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
 for n,h in pins.items():
  if hashlib.sha256((R/n).read_bytes()).hexdigest()!=h:raise ValueError('POSTRUN_PIN:'+n)
 with (H/'tests.json').open('x')as stream:json.dump({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'successful':result.wasSuccessful()},stream)
 if not result.wasSuccessful():raise ValueError('FINAL_ROLE_TEST_FAILURE')
 # The setUpClass positive invokes real evaluate once, without monkeypatching.
 # Negative tests mutate deep copies only. Preserve that exact computed object.
 out=tests.FinalRoleJoint367.o
 with (H/'actual.json').open('x')as stream:json.dump(out,stream,indent=2)
 with (H/'actual_provenance.json').open('x')as stream:json.dump({'kind':'TEST_POSITIVE_REAL_REASSESSMENT','callsite':'test_role_registry_final_joint367_v4.FinalRoleJoint367.setUpClass','synthetic':False,'new_fresh':False},stream)
except BaseException:
 with (H/'error.txt').open('x')as stream:stream.write(traceback.format_exc())
 raise
