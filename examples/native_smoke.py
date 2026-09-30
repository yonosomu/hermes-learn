"""Run with Hermes's Python in a preinstalled isolated HERMES_HOME. Never enable globally."""
import json, os
from pathlib import Path
from hermes_cli.plugins import PluginManager, PluginContext, parse_manifest_file
import importlib.util, sys
from tools.registry import registry
home=Path(os.environ['HERMES_HOME'])
m=PluginManager(scope_key=str(home))
entry=home/'plugins/hermes-learn/__init__.py'
manifest=parse_manifest_file(entry.parent/'plugin.yaml',entry.parent,'standalone','')
spec=importlib.util.spec_from_file_location('learn_native_smoke',entry,submodule_search_locations=[str(entry.parent)])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
module.register(PluginContext(manifest,m))
def call(name,args):
 e=registry.get_entry(name,scope=m.scope_key)
 assert e is not None, name
 r=json.loads(e.handler(args));assert 'error' not in r,r
 return r
q=call('learn_quiz',dict(action='create',question='Pick the prerequisite direction',options=['Earlier to later','Later to earlier'],correct=[1],explanation='Prerequisites support later ideas.'))
assert 'correct' not in q and 'explanation' not in q
r=call('learn_quiz',dict(action='submit',id=q['id'],answers=[1]))
assert r['status']=='correct'
call('learn_journal',dict(path=str(home/'session.md'),kind='goal',text='Practice prerequisite reasoning'))
p=home/'native-diagram.svg'
call('learn_visual',dict(action='write',path=str(p),source='<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60"><circle cx="30" cy="30" r="20"/></svg>'))
r=call('learn_visual',dict(action='render',path=str(p),output=str(home/'native-diagram.png')))
assert p.exists()
assert (home/'session.md').exists()
print(json.dumps({'native_tools_invoked':3,'quiz_status':'correct','diagram':r},indent=2))
