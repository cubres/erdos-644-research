from pathlib import Path
import hashlib, json

root = Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd')
source = Path('/Users/cubres/Documents/Clauding/erdos-hunt')
files = set(json.loads((root/'outputs/certificates_0862/MANIFEST.json').read_text()))
files.update('''p644_interval_refine.py p644_gap_finish_31_36.py p644_partial_gap.py p644_astra_31_36_check.py p644_gap_matching.py p644_astra_gap_matching_check.py p644_gap_second_adaptive.py'''.split())
files.update('logs/'+name+'.json' for name in '''astra_interval_refine_31_36 astra_gap_high_31_36 astra_gap_middle_31_36 astra_partial_gap astra_gap_matching_grid astra_gap_matching astra_gap_second_adaptive astra_interval_padded_17_20 astra_interval_padded_6_7'''.split())
target = root/'outputs/certificates_31_36'
assert not target.exists()
payload = {}
for name in sorted(files):
    assert Path(name).suffix in ['.py', '.json', '.md']
    assert not Path(name).is_absolute() and '..' not in Path(name).parts
    src = root/'outputs/VERIFICATION.md' if name == 'README.md' else source/name
    payload[name] = src.read_bytes()
for name, data in payload.items():
    dst = target/name
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open('xb') as f:
        f.write(data)
manifest = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
with (target/'MANIFEST.json').open('x') as f:
    json.dump(manifest, f, indent=2, sort_keys=True)
for name, digest in manifest.items():
    assert hashlib.sha256((target/name).read_bytes()).hexdigest() == digest
print('PASS', len(manifest), 'content files plus manifest; all copies verified in', target)
