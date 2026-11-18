import pathlib,unittest
HTML=pathlib.Path(__file__).with_name('index.html').read_text()
class SchemaTests(unittest.TestCase):
 def test_partial_states_precede_full_binding_gate(self):
  self.assertLess(HTML.index("if(value.state==='RUNNING')"),HTML.index('const outer=value.binding'))
  self.assertIn("kind:'partial_terminal'",HTML)
 def test_partial_never_renders_models(self):
  self.assertIn("identity.kind==='member_terminal'",HTML)
  self.assertIn('TERMINAL_PARTIAL_REPORTED',HTML)
 def test_full_identity_gates_remain(self):
  for value in ('MEMBER_RUN_OR_KIND_MISMATCH','MEMBER_MODEL_DIGEST_MISMATCH','OUTER_REQUEST_BODY_MISMATCH'):self.assertIn(value,HTML)
if __name__=='__main__':unittest.main()
