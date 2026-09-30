"""Native Hermes registration using only the documented PluginContext API."""
import json, os
from pathlib import Path
try:
    from .runtime.core import QuizStore
    from .runtime.journal import append_entry
    from .runtime.visual import write_source, edit_source, render
except ModuleNotFoundError:
    import importlib.util, sys
    package_name = __name__ + '.runtime'
    source = Path(__file__).resolve().parent.parent / 'hermes_learn'
    spec = importlib.util.spec_from_file_location(package_name, source / '__init__.py', submodule_search_locations=[str(source)])
    module = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = module
    spec.loader.exec_module(module)
    from .runtime.core import QuizStore
    from .runtime.journal import append_entry
    from .runtime.visual import write_source, edit_source, render

def quiz(args, **kwargs):
    try:
        home = os.environ.get('HERMES_HOME')
        if not home:
            raise ValueError('HERMES_HOME required for profile-safe quiz storage')
        store = QuizStore(Path(home) / 'learn-data')
        action = args['action']
        if action == 'create':
            r = store.create(args['question'], args['options'], args['correct'], args.get('explanation', ''), args.get('multiple', False))
        elif action == 'submit':
            r = store.submit(args['id'], args.get('answers'), args.get('status', 'answer'), args.get('note', ''))
        elif action in ('show', 'attempts'):
            r = getattr(store, action)(args['id'])
        else:
            raise ValueError('invalid action')
        return json.dumps(r, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)

def journal(args, **kwargs):
    try:
        return json.dumps(append_entry(args['path'], args['kind'], args['text']), ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)

def visual(args, **kwargs):
    try:
        action = args['action']
        if action == 'write':
            r = write_source(args['path'], args['source'])
        elif action == 'edit':
            r = edit_source(args['path'], args['old'], args['new'])
        elif action == 'render':
            r = render(args['path'], args['output'])
        else:
            raise ValueError('invalid action')
        return json.dumps(r, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)

def schema(name, description, properties, required):
    return {'name': name, 'description': description, 'parameters': {'type': 'object', 'properties': properties, 'required': required, 'additionalProperties': False}}

def register(ctx):
    string = {'type': 'string'}
    ints = {'type': 'array', 'items': {'type': 'integer'}}
    specs = [('learn_quiz', quiz, schema('learn_quiz', 'Create/show hidden-key quizzes; submit only a real learner answer; attempts are persisted. Indices are 1-based. Keys in creation arguments are visible to tool inspectors; not secure testing.', {'action': {'type': 'string', 'enum': ['create', 'show', 'submit', 'attempts']}, 'id': string, 'question': string, 'options': {'type': 'array', 'items': string}, 'correct': ints, 'explanation': string, 'multiple': {'type': 'boolean'}, 'answers': ints, 'status': {'type': 'string', 'enum': ['answer', 'unknown', 'skipped']}, 'note': string}, ['action'])), ('learn_journal', journal, schema('learn_journal', 'Append one consented structured entry to an explicit Markdown study journal. Never automatically capture chat.', {'path': string, 'kind': {'type': 'string', 'enum': ['goal', 'prerequisites', 'lesson', 'question', 'attempt', 'feedback', 'misconception', 'sources', 'visual', 'reflection', 'next']}, 'text': string}, ['path', 'kind', 'text'])), ('learn_visual', visual, schema('learn_visual', 'Write new .svg/.mmd source, exact unique edit, or render to a new PNG using optional local renderer. Missing renderer returns source-only, never a fake image. Inspect returned images separately.', {'action': {'type': 'string', 'enum': ['write', 'edit', 'render']}, 'path': string, 'source': string, 'old': string, 'new': string, 'output': string}, ['action', 'path']))]
    for name, handler, s in specs:
        ctx.register_tool(name=name, toolset='hermes-learn', schema=s, handler=handler)
