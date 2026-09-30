import unittest, tempfile, json, os, importlib.util
from pathlib import Path
from unittest.mock import patch
from hermes_learn.core import QuizStore
from hermes_learn.install import install, uninstall

class SafetyTests(unittest.TestCase):

    def test_multi_unknown_skip_validation(self):
        with tempfile.TemporaryDirectory() as d:
            q = QuizStore(d)
            v = q.create('Choose', ['a', 'b', 'c'], [1, 3], 'Why', True)
            self.assertEqual(q.submit(v['id'], [3, 1])['status'], 'correct')
            self.assertEqual(q.submit(v['id'], [1])['status'], 'incorrect')
            self.assertEqual(q.submit(v['id'], status='unknown')['status'], 'unknown')
            self.assertNotIn('correct', q.submit(v['id'], status='skipped'))
            for a in ([0], [True], [1, 1], []):
                with self.assertRaises(ValueError):
                    q.submit(v['id'], a)

    def test_ancestor_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'real').mkdir()
            try:
                (p / 'link').symlink_to(p / 'real', target_is_directory=True)
            except OSError:
                self.skipTest('symlinks unavailable')
            with self.assertRaises(ValueError):
                install(p / 'link' / 'profile')

    def test_installed_plugin_self_contained(self):
        with tempfile.TemporaryDirectory() as d:
            h = Path(d).resolve()
            install(h)
            p = h / 'plugins/hermes-learn/__init__.py'
            spec = importlib.util.spec_from_file_location('installed_learn', p, submodule_search_locations=[str(p.parent)])
            import sys
            m = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = m
            spec.loader.exec_module(m)
            with patch.dict(os.environ, {'HERMES_HOME': d}):
                v = json.loads(m.quiz(dict(action='create', question='Which?', options=['x', 'y'], correct=[2], explanation='yes')))
                self.assertNotIn('correct', v)
                self.assertEqual(json.loads(m.quiz(dict(action='submit', id=v['id'], answers=[2])))['status'], 'correct')
            uninstall(h)
            self.assertTrue((h / 'learn-data/quizzes.sqlite3').exists())
