"""Explicit structured Markdown journal, never an automatic chat logger."""
from datetime import datetime, timezone
from pathlib import Path
KINDS = {'goal', 'prerequisites', 'lesson', 'question', 'attempt', 'feedback', 'misconception', 'sources', 'visual', 'reflection', 'next'}

def append_entry(path, kind, text):
    if kind not in KINDS:
        raise ValueError('unknown journal kind')
    if not isinstance(text, str) or not text.strip():
        raise ValueError('entry text required')
    p = Path(path)
    if p.suffix.lower() != '.md' or p.is_symlink():
        raise ValueError('regular .md target required')
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a', encoding='utf-8') as f:
        f.write('\n## ' + kind.title() + ' — ' + datetime.now(timezone.utc).isoformat() + '\n\n' + text + '\n')
    return {'path': str(p.resolve()), 'kind': kind}
