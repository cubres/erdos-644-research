"""Write a narrow, content-addressed handoff manifest; copy no environment."""
from pathlib import Path
import hashlib,json,sys,platform
import numpy,scipy,sympy
root=Path.cwd();base=root/'work/paper_push/three_cert';src=Path('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c');heavy=src.parent/'heavy'

def row(p,role):
    return {'path':str(p),'role':role,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
local=['resume_search.py','search_disjoint.py','strict_types.py','strong_blocker.py','fast_reps.py','v4_templates.py','mixed1321_templates.py','anchor_pair_request.py','fast_duals.py','progress_certify.py','conditional_check.py','strict_check.py','strict_certify.py','frontier_diagnostic.py','frontier_template_check.py','make_resume_manifest.py','balanced_1321_template.json','three_minimum_barrier_replay.py']
external=[src/f for f in ['search6.py','b4core.py','b3core.py','exactcert.py','certify5.py','check5.py','suppmilp.py','supports.py']]
external +=[heavy/'heavylib.py',heavy/'astra_support_capacity_minimal.json']
external +=[heavy/f'reps{i}.npy' for i in range(1,10)]
external +=[src/'vcache.pkl']
artifacts=['three_minimum_barrier_replay.json','slab_9d8.json','slab_9d8_fastcert.json','slab_9d8_fastcheck.log','u12_hard_v4_cert.json','u12_hard_v4_check.log']
for prefix in ['balanced_point_optimal20','balanced_point_anchor12']:
    artifacts +=[prefix+suf for suf in ['.sqlite','.status.json','.frontier.json','.frontier.pkl','.diagnostic.json','.diagnostic.log','.diagnostic.anchor_pair.json','.log']]
artifacts += ['balanced_point_optimal20.template_check.json','balanced_point_anchor12.diagnostic.existing_v4.json']
command='python3 work/paper_push/three_cert/resume_search.py 3/4,3/4,4/5 3/4,3/4,4/5 balanced work/paper_push/three_cert/balanced_point_anchor12 --seconds 300 --facet 1 --requests 12 --max-types 16 --optimal-blocker --strict-types --strong-blocker --disjoint --anchor-pair'
out={'status':'PAUSED_AT_REQUESTED_CAP_NO_COMPLETE_POINT_CERTIFICATE','cwd':str(root),
     'created':'2026-09-26','runtime':{'python':platform.python_version(),'executable':sys.executable,'numpy':numpy.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__},
     'resume_command':command,'resume_caution':'Command is documented, not running. Keep all flags and prefix to reuse matching SQLite completed subtrees. CPU budget may be changed. No complete theorem follows from a checkpoint.',
     'local_pipeline':[row(base/f,'task-local source') for f in local],
     'read_only_dependencies':[row(p,'original Claude dependency; preserve in place') for p in external if p.exists()],
     'artifacts':[row(base/f,'proof or preserved checkpoint') for f in artifacts if (base/f).exists()],
     'report':row(root/'outputs/paper_push_three_cert.md','current coherent status and exact scope'),
     'proof_scope':'Balanced median>=9/8 exact-certified; full unbalanced and min>=6/7 hand results reported by root. Full Th(3) and unrestricted Erdos644 unresolved.',
     'checking':{'ordinary':f'python3 {src}/check5.py CERT.json','extended':'python3 work/paper_push/three_cert/conditional_check.py CERT.json','producer':'python3 work/paper_push/three_cert/progress_certify.py TREE.json CERT.json'},
     'discovery_limits':['Numerical template/request selection is not proof.','At >9 types with max-types>11, Fano menu contains <=3-color assignments only. V4/mixed menus retain all4-role assignments.','No complete capacity-point tree resulted from either focused timeout. Feasible frontier samples already fit some templates.']}
(base/'resume_manifest.json').write_text(json.dumps(out,indent=2))
print('MANIFEST',len(out['local_pipeline']),'local files;',len(out['read_only_dependencies']),'read-only dependencies;',len(out['artifacts']),'artifacts')
