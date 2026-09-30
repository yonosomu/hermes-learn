import unittest, subprocess, sys, tempfile
from pathlib import Path

class SourcePluginTests(unittest.TestCase):

    def test_source_entrypoint_without_pythonpath(self):
        entry = Path(__file__).resolve().parents[1] / 'plugin/__init__.py'
        code = "import importlib.util,sys; s=importlib.util.spec_from_file_location('learn_external',sys.argv[1],submodule_search_locations=[str(__import__('pathlib').Path(sys.argv[1]).parent)]); m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);assert callable(m.register)"
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, '-I', '-c', code, str(entry)], cwd=d, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
