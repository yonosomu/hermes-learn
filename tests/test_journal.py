import tempfile, unittest
from pathlib import Path
from hermes_learn.journal import append_entry

class JournalTests(unittest.TestCase):

    def test_explicit_entries(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'session.md'
            append_entry(p, 'goal', 'Understand vectors')
            append_entry(p, 'next', 'Try an example')
            self.assertIn('## Goal', p.read_text())
            self.assertIn('## Next', p.read_text())

    def test_unknown_kind_rejected(self):
        with self.assertRaises(ValueError):
            append_entry('unused', 'transcript', 'secret')
