import pathlib
import unittest

HTML = pathlib.Path(__file__).with_name("index.html").read_text()


class IdentitySourceTests(unittest.TestCase):
    def test_existing_schema_identity_links_are_checked(self):
        for text in ("OUTER_REQUEST_BODY_MISMATCH", "MEMBER_RUN_OR_KIND_MISMATCH", "MEMBER_REQUEST_BINDING_MISMATCH", "MEMBER_MODEL_DIGEST_MISMATCH"):
            self.assertIn(text, HTML)

    def test_identity_failure_is_terminal_fail_closed(self):
        self.assertIn("error?.kind==='identity'", HTML)
        self.assertIn("IDENTITY_REJECTED", HTML)
        self.assertIn("clearDisplayed()", HTML)

    def test_display_binding_contains_request_and_model_identity(self):
        self.assertIn("request_binding:{...x.binding}", HTML)
        self.assertIn("model_ids:modelIds", HTML)


if __name__ == "__main__": unittest.main()
