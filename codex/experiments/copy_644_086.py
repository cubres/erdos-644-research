from pathlib import Path
import hashlib,json

root=Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd')
source=Path('/Users/cubres/Documents/Clauding/erdos-hunt')
files=set(json.loads((root/'outputs/certificates_31_36/MANIFEST.json').read_text()))
files.update('''p644_interval_refine_lower.py p644_tree_gap_robust.py p644_tree_gap_probe.py p644_pairgap_probe.py p644_gap_one_trace.py p644_interval_one_trace.py p644_interval_finish_one_trace.py p644_astra_one_trace_check.py'''.split())
files.update('logs/'+name+'.json' for name in '''astra_interval_padded_43_50 astra_interval_refine_43_50 astra_interval_refine_6_7 astra_interval_one_trace_43_50 astra_interval_finished_43_50 astra_gap_middle_43_50 astra_gap_high_probe_43_50 astra_gap_high_probe_6_7 astra_tree_gap_robust astra_tree_gap_probe astra_pairgap_probe astra_gap_one_trace'''.split())
target=root/'outputs/certificates_086'
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
