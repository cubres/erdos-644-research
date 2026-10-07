from pathlib import Path
import hashlib,json

root=Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd')
source=Path('/Users/cubres/Documents/Clauding/erdos-hunt')
previous=root/'work/bundle_replay_4/erdos644_astra_checkpoint/MANIFEST.json'
files=set(json.loads(previous.read_text()))
files.update('''p644_triple_tree.py p644_tree_robust.py p644_partial_core_cases.py p644_padded_pair.py p644_padded_dominant.py p644_spectrum_partial.py p644_spectrum_padded.py p644_interval_padded.py p644_interval_closure.py p644_gap_finish.py p644_astra_partial_tree_obstruction.py p644_astra_maxsmall_check.py p644_astra_interval_bound_check.py'''.split())
patterns=['astra_triple_tree*.json','astra_tree_robust*.json','astra_partial_core*.json','astra_padded*.json','astra_gap_high*.json','astra_gap_middle*.json','astra_interval_padded*.json','astra_maxsmall_partial*.json','astra_maxsmall_padded*.json','astra_static_partial_hole.json','astra_static_template_facets_v3.json','astra_static_middle_probe.json','astra_static_narrow_probe.json','astra_matching_partial_hole.json','astra_spectrum_partial*.json','astra_spectrum_padded*.json']
for pattern in patterns:
    files.update(str(p.relative_to(source)) for p in (source/'logs').glob(pattern))
target=root/'outputs/certificates_0862'
assert not target.exists()
payload={}
for name in sorted(files):
    assert Path(name).suffix in ['.py','.json','.md']
    assert not Path(name).is_absolute() and '..' not in Path(name).parts
    src=root/'outputs/VERIFICATION.md' if name=='README.md' else source/name
    assert src.is_file(),str(src)
    payload[name]=src.read_bytes()
for name,data in payload.items():
    dst=target/name;dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as f:f.write(data)
manifest={name:hashlib.sha256(data).hexdigest() for name,data in payload.items()}
with (target/'MANIFEST.json').open('x') as f:json.dump(manifest,f,indent=2,sort_keys=True)
for name,digest in manifest.items():assert hashlib.sha256((target/name).read_bytes()).hexdigest()==digest
print('PASS',len(manifest),'content files plus manifest; all copies verified in',target)
