import unittest, tempfile, subprocess, sys, json
from pathlib import Path

class InterfaceTests(unittest.TestCase):

    def test_cli_quiz(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'quiz.json'
            p.write_text(json.dumps(dict(question='Which?', options=['a', 'b'], correct=[1], explanation='Reason')))
            r = subprocess.run([sys.executable, '-m', 'hermes_learn', '--data', d, 'quiz', 'create', str(p)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertNotIn('Reason', r.stdout)
            q = json.loads(r.stdout)
            r = subprocess.run([sys.executable, '-m', 'hermes_learn', '--data', d, 'quiz', 'submit', q['id'], '--answers', '1'], capture_output=True, text=True)
            self.assertEqual(json.loads(r.stdout)['status'], 'correct')

    def test_plugin_register(self):
        import plugin

        class Ctx:

            def __init__(self):
                self.tools = {}

            def register_tool(self, **kw):
                self.tools[kw['name']] = kw
        c = Ctx()
        plugin.register(c)
        self.assertEqual(set(c.tools), {'learn_quiz', 'learn_journal', 'learn_visual'})
