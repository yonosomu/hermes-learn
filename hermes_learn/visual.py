"""Source editing and optional local rasterization. No automatic installs."""
import re, shutil, subprocess, tempfile, xml.etree.ElementTree as ET
from pathlib import Path

def validate(path, source):
    if not source.strip():
        raise ValueError('empty diagram')
    if Path(path).suffix == '.svg':
        if re.search('<!DOCTYPE|<!ENTITY', source, re.I):
            raise ValueError('XML declarations forbidden')
        root = ET.fromstring(source)
        if root.tag.split('}')[-1] != 'svg':
            raise ValueError('svg root required')
        allowed = {'svg', 'g', 'path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'text', 'tspan', 'title', 'desc', 'defs', 'marker', 'linearGradient', 'radialGradient', 'stop', 'clipPath'}
        for e in root.iter():
            if e.tag.split('}')[-1] not in allowed:
                raise ValueError('unsupported SVG element')
            for k, v in e.attrib.items():
                if k.split('}')[-1].lower().startswith('on') or k.split('}')[-1] in ('href', 'style') or re.search('url\\(\\s*(?!#)', v, re.I):
                    raise ValueError('active/external SVG content forbidden')
    elif Path(path).suffix != '.mmd':
        raise ValueError('use .svg or .mmd')
    elif '%%{' in source or re.search('(^|[;\\n])\\s*click\\b', source, re.I):
        raise ValueError('Mermaid directives/click actions forbidden')

def write_source(path, source):
    p = Path(path)
    validate(p, source)
    if p.exists():
        raise FileExistsError('source exists; use exact edit or a new filename')
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf-8') as f:
        f.write(source)
    return {'path': str(p.resolve()), 'rendered': False}

def edit_source(path, old, new):
    p = Path(path)
    if p.is_symlink():
        raise ValueError('symlink target forbidden')
    s = p.read_text(encoding='utf-8')
    if not old or s.count(old) != 1 or old == new:
        raise ValueError('edit requires a unique nonempty changed match')
    s = s.replace(old, new, 1)
    validate(p, s)
    p.write_text(s, encoding='utf-8')
    return {'path': str(p.resolve()), 'rendered': False}

def render(source, output):
    p = Path(source)
    out = Path(output)
    validate(p, p.read_text(encoding='utf-8'))
    if out.suffix != '.png' or out.exists():
        raise ValueError('new .png output required')
    binary = shutil.which('mmdc' if p.suffix == '.mmd' else 'rsvg-convert')
    if not binary:
        return {'rendered': False, 'source': str(p.resolve()), 'reason': 'renderer unavailable: ' + ('mmdc' if p.suffix == '.mmd' else 'rsvg-convert')}
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='hermes-learn-', dir=out.parent) as d:
        stage = Path(d) / 'preview.png'
        args = [binary, '-i', str(p.resolve()), '-o', str(stage)] if p.suffix == '.mmd' else [binary, str(p.resolve()), '-o', str(stage)]
        r = subprocess.run(args, capture_output=True, text=True, timeout=120)
        if r.returncode or not stage.exists() or (not stage.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')):
            raise RuntimeError('renderer failed: ' + (r.stderr or r.stdout)[-4000:])
        with out.open('xb') as f:
            f.write(stage.read_bytes())
    return {'rendered': True, 'path': str(out.resolve()), 'inspected': False}
