import unittest, tempfile
from pathlib import Path
from hermes_learn.visual import write_source, edit_source, render

class VisualTests(unittest.TestCase):

    def test_source_and_exact_edit(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'x.mmd'
            write_source(p, 'graph TD\n A-->B')
            edit_source(p, 'B', 'C')
            self.assertIn('C', p.read_text())
            with self.assertRaises(ValueError):
                edit_source(p, 'missing', 'D')

    def test_svg_rejects_active_content(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                write_source(Path(d) / 'x.svg', '<svg><script>alert(1)</script></svg>')

    def test_missing_renderer_is_honest(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'x.mmd'
            write_source(p, 'graph TD; A-->B')
            with patch('hermes_learn.visual.shutil.which', return_value=None):
                r = render(p, Path(d) / 'x.png')
                self.assertFalse(r['rendered'])
                self.assertFalse((Path(d) / 'x.png').exists())
