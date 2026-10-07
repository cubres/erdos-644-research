from pathlib import Path
import hashlib,json

root=Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd')
source=Path('/Users/cubres/Documents/Clauding/erdos-hunt')
files=set(json.loads((root/'outputs/certificates_086/MANIFEST.json').read_text()))
files.update('''p644_general_requests.py p644_gap_two_triples.py p644_interval_two_triples.py p644_astra_two_triple_obstruction_check.py p644_gap_trace_dichotomy.py p644_finish_six_sevenths.py p644_astra_six_sevenths_check.py'''.split())
files.update('logs/'+name+'.json' for name in '''astra_two_triples_first_probe astra_gap_two_triples astra_two_triples_hole_box astra_two_triples_endpoint_6_7 astra_interval_two_triples_6_7 astra_two_triples_boundary_probe astra_gap_trace_dichotomy astra_interval_finished_6_7'''.split())
target=root/'outputs/certificates_6_7'
assert not target.exists()
payload={}
for name in sorted(files):
    assert Path(name).suffix in ['.py','.json','.md']
    assert not Path(name).is_absolute() and '..' not in Path(name).parts
    src=root/'outputs/VERIFICATION.md' if name=='README.md' else source/name
    payload[name]=src.read_bytes()
for name,data in payload.items():
    dst=target/name;dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as f:f.write(data)
manifest={name:hashlib.sha256(data).hexdigest() for name,data in payload.items()}
with (target/'MANIFEST.json').open('x') as f:json.dump(manifest,f,indent=2,sort_keys=True)
for name,digest in manifest.items():assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest
print('PASS',len(manifest),'content files plus manifest; all copies verified in',target)
