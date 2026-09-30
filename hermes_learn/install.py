"""Explicit, profile-aware, ownership-checked directory installation."""
import hashlib, json, os, re, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TARGETS = ('skills/teach', 'skills/visualize', 'plugins/hermes-learn')

def home(value=None):
    if value:
        return Path(value).expanduser().absolute()
    if os.environ.get('HERMES_HOME'):
        return Path(os.environ['HERMES_HOME']).expanduser().absolute()
    raise ValueError('set HERMES_HOME to the intended profile or pass --home; no implicit live-profile changes')

def disposable_cache(path):
    return (path.parent.name == '__pycache__' and
            re.fullmatch(r'.+\.(?:cpython-\d+|pypy\d+)(?:\.opt-\d+)?\.pyc', path.name))

def ignore_cache(directory, names):
    return [name for name in names if disposable_cache(Path(directory) / name)]

def fingerprint(path):
    p = Path(path)
    if p.is_symlink():
        raise ValueError('symlinks forbidden in install tree')
    result = {}
    for f in sorted(p.rglob('*')):
        if f.is_symlink():
            raise ValueError('symlinks forbidden in install tree')
        if f.is_file() and not disposable_cache(f):
            result[f.relative_to(p).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return result

def safe_targets(h):
    for rel in (*TARGETS, '.hermes-learn-install.json'):
        p = h / rel
        for q in (p, *p.parents):
            if q.is_symlink():
                raise ValueError('symlink in install path')
    return [h / r for r in TARGETS]

def install(target=None, dry_run=False):
    h = home(target)
    destinations = safe_targets(h)
    manifest = h / '.hermes-learn-install.json'
    if manifest.exists() or any((p.exists() for p in destinations)):
        raise FileExistsError('installation conflict; back up/move existing directories explicitly, never overwrite')
    sources = [ROOT / 'skills/teach', ROOT / 'skills/visualize', ROOT / 'plugin']
    if not all((p.is_dir() for p in sources)):
        raise ValueError('install from a complete source checkout')
    records = {rel: fingerprint(src) for rel, src in zip(TARGETS, sources)}
    runtime = ROOT / 'hermes_learn'
    records['plugins/hermes-learn'].update({'runtime/' + k: v for k, v in fingerprint(runtime).items()})
    plan = {'home': str(h), 'targets': list(TARGETS), 'dry_run': dry_run}
    if dry_run:
        return plan
    created = []
    try:
        for src, dst in zip(sources, destinations):
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.mkdir()
            created.append(dst)
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore_cache)
        shutil.copytree(runtime, destinations[-1] / 'runtime', ignore=ignore_cache)
        with manifest.open('x', encoding='utf-8') as f:
            json.dump(records, f, indent=2)
    except Exception:
        for p in created:
            shutil.rmtree(p)
        raise
    return plan

def uninstall(target=None, dry_run=False):
    h = home(target)
    destinations = safe_targets(h)
    manifest = h / '.hermes-learn-install.json'
    records = json.loads(manifest.read_text(encoding='utf-8'))
    if set(records) != set(TARGETS):
        raise ValueError('invalid ownership manifest')
    for rel, p in zip(TARGETS, destinations):
        if not p.is_dir() or fingerprint(p) != records[rel]:
            raise ValueError('installed files changed; preserve/back up edits before uninstall')
    plan = {'home': str(h), 'remove': list(TARGETS), 'dry_run': dry_run, 'data_preserved': True}
    if not dry_run:
        for p in destinations:
            shutil.rmtree(p)
        manifest.unlink()
    return plan
