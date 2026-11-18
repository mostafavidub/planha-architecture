import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
HTML = (HERE / "index.html").read_text()


class FrontendSourceTests(unittest.TestCase):
    def test_revision_snapshot_and_binding_guards_exist(self):
        for text in ("inputRevision", "raw_snapshot", "sameSnapshot", "TERMINAL_SUPPRESSED_STALE", "POLL_RUN_ID_MISMATCH", "window.displayBinding"):
            self.assertIn(text, HTML)

    def test_one_shot_lock_is_not_weakened(self):
        self.assertIn("if(submissionLocked){record('DUPLICATE_SUBMIT_BLOCKED'", HTML)
        self.assertNotIn("submissionLocked=false;activeSubmission=null;button.disabled=false;if(sameSnapshot(sub))", HTML.split("if(!r.ok)")[0])

    def test_display_is_cleared_on_input(self):
        self.assertIn("form.addEventListener('input'", HTML)
        self.assertIn("clearDisplayed()", HTML)


if __name__ == "__main__":
    unittest.main()
