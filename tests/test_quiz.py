import unittest, tempfile
from pathlib import Path
from hermes_learn.core import QuizStore

class QuizTests(unittest.TestCase):

    def test_hidden_and_persisted(self):
        with tempfile.TemporaryDirectory() as d:
            q = QuizStore(Path(d))
            v = q.create('Pick', ['a', 'b'], [2], 'Because')
            self.assertNotIn('correct', v)
            self.assertNotIn('Because', str(v))
            r = QuizStore(Path(d)).submit(v['id'], [2])
            self.assertEqual(r['status'], 'correct')
            self.assertEqual(len(q.attempts(v['id'])), 1)
