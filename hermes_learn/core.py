"""Local quiz persistence; no network or transcript access."""
import json, re, sqlite3, uuid
from contextlib import contextmanager
from pathlib import Path

class QuizStore:

    def __init__(self, directory):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.db = directory / 'quizzes.sqlite3'
        with self.connect() as c:
            c.execute('CREATE TABLE IF NOT EXISTS quizzes (id TEXT PRIMARY KEY, body TEXT NOT NULL)')
            c.execute('CREATE TABLE IF NOT EXISTS attempts (id INTEGER PRIMARY KEY, quiz TEXT, body TEXT NOT NULL)')

    @contextmanager
    def connect(self):
        c = sqlite3.connect(self.db)
        try:
            with c:
                yield c
        finally:
            c.close()

    def create(self, question, options, correct, explanation='', multiple=False):
        if not isinstance(question, str) or not question.strip():
            raise ValueError('question required')
        if not isinstance(options, list) or len(options) < 2 or any((not isinstance(x, str) or not x.strip() for x in options)):
            raise ValueError('at least two text options required')
        if not correct or any((type(x) is not int or not 1 <= x <= len(options) for x in correct)) or len(set(correct)) != len(correct):
            raise ValueError('invalid correct indices')
        if not multiple and len(correct) != 1:
            raise ValueError('single choice requires one correct answer')
        body = dict(id=uuid.uuid4().hex, question=question, options=options, correct=correct, explanation=explanation, multiple=bool(multiple))
        with self.connect() as c:
            c.execute('INSERT INTO quizzes VALUES (?,?)', (body['id'], json.dumps(body)))
        return self.show(body['id'])

    def _get(self, ident):
        with self.connect() as c:
            row = c.execute('SELECT body FROM quizzes WHERE id=?', (ident,)).fetchone()
        if not row:
            raise ValueError('unknown quiz')
        return json.loads(row[0])

    def show(self, ident):
        return {k: v for k, v in self._get(ident).items() if k not in ('correct', 'explanation')}

    def submit(self, ident, answers=None, status='answer', note=''):
        q = self._get(ident)
        answers = [] if answers is None else answers
        if status not in ('answer', 'unknown', 'skipped'):
            raise ValueError('invalid status')
        if status == 'answer' and (not answers or any((type(x) is not int or not 1 <= x <= len(q['options']) for x in answers)) or len(set(answers)) != len(answers) or (not q['multiple'] and len(answers) != 1)):
            raise ValueError('invalid selection')
        if status != 'answer' and answers:
            raise ValueError('non-answer cannot contain selections')
        result = dict(id=ident, answers=answers, note=note, status=status if status != 'answer' else 'correct' if set(answers) == set(q['correct']) else 'incorrect')
        if status != 'skipped':
            result.update(correct=q['correct'], explanation=q['explanation'])
        with self.connect() as c:
            c.execute('INSERT INTO attempts (quiz,body) VALUES (?,?)', (ident, json.dumps(result)))
        return result

    def attempts(self, ident):
        self._get(ident)
        with self.connect() as c:
            return [json.loads(x[0]) for x in c.execute('SELECT body FROM attempts WHERE quiz=? ORDER BY id', (ident,))]
