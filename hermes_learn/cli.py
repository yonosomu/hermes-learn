"""Stdlib command-line interface. All successful outputs are JSON."""
import argparse, json, os, sys
from pathlib import Path
from .core import QuizStore
from .journal import append_entry, KINDS
from .visual import write_source, edit_source, render
from .install import install, uninstall

def data_home():
    return Path(os.environ.get('HERMES_HOME', str(Path.home() / '.hermes'))) / 'learn-data'

def main(argv=None):
    p = argparse.ArgumentParser(prog='hermes-learn')
    p.add_argument('--data', type=Path, default=None)
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('quiz')
    qs = q.add_subparsers(dest='action', required=True)
    c = qs.add_parser('create')
    c.add_argument('file', type=Path, help='JSON question, options, correct (1-based), explanation, multiple')
    for action in ('show', 'attempts'):
        a = qs.add_parser(action)
        a.add_argument('id')
    a = qs.add_parser('submit')
    a.add_argument('id')
    a.add_argument('--answers', type=int, nargs='+')
    a.add_argument('--status', choices=['answer', 'unknown', 'skipped'], default='answer')
    a.add_argument('--note', default='')
    j = sub.add_parser('journal')
    j.add_argument('path', type=Path)
    j.add_argument('kind', choices=sorted(KINDS))
    j.add_argument('text')
    v = sub.add_parser('visual')
    vs = v.add_subparsers(dest='action', required=True)
    a = vs.add_parser('write')
    a.add_argument('path', type=Path)
    a.add_argument('source', type=Path, help='UTF-8 source input')
    a = vs.add_parser('edit')
    a.add_argument('path', type=Path)
    a.add_argument('old')
    a.add_argument('new')
    a = vs.add_parser('render')
    a.add_argument('path', type=Path)
    a.add_argument('output', type=Path)
    for action in ('install', 'uninstall'):
        a = sub.add_parser(action)
        a.add_argument('--home', type=Path)
        a.add_argument('--dry-run', action='store_true')
    a = p.parse_args(argv)
    try:
        if a.command == 'quiz':
            store = QuizStore(a.data or data_home())
            if a.action == 'create':
                result = store.create(**json.loads(a.file.read_text(encoding='utf-8')))
            elif a.action == 'submit':
                result = store.submit(a.id, a.answers, a.status, a.note)
            else:
                result = getattr(store, a.action)(a.id)
        elif a.command == 'journal':
            result = append_entry(a.path, a.kind, a.text)
        elif a.command == 'visual':
            if a.action == 'write':
                result = write_source(a.path, a.source.read_text(encoding='utf-8'))
            elif a.action == 'edit':
                result = edit_source(a.path, a.old, a.new)
            else:
                result = render(a.path, a.output)
        else:
            result = (install if a.command == 'install' else uninstall)(a.home, a.dry_run)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        return 1
