"""Write a narrow, content-addressed handoff manifest; copy no environment."""
from pathlib import Path
import hashlib,json,sys,platform
import numpy,scipy,sympy
root=Path.cwd();base=root/'work/paper_push/three_cert';src=Path('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c');heavy=src.parent/'heavy'

def row(p,role):
    return {'path':str(p),'role':role,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
local=['resume_search.py','search_disjoint.py','strict_types.py','strong_blocker.py','fast_reps.py','v4_templates.py','mixed1321_templates.py','anchor_pair_request.py','fast_duals.py','progress_certify.py','conditional_check.py','strict_check.py','strict_certify.py','frontier_diagnostic.py','frontier_template_check.py','make_resume_manifest.py','balanced_1321_template.json','three_minimum_barrier_replay.py','fano_v4_partner_oracle.py','probe_fano_v4_partners.py','probe_fano_v4_focused.py','classify_broad_partner_probe.py','known_anchor_bad.py','v4_escape_boxes.py']
local += ['terminal_partner_search.py','repeated_response_oracle.py','check_endpoint_menu_barrier.py',
          'endpoint_u_all_support.py','endpoint_new_template.py','endpoint_interval_model.py',
          'certify_endpoint_interval.py','check_endpoint_interval.py','check_new223_facets.py','check_endpoint_cone.py']
external=[src/f for f in ['search6.py','b4core.py','b3core.py','exactcert.py','certify5.py','check5.py','suppmilp.py','supports.py']]
external +=[heavy/'heavylib.py',heavy/'astra_support_capacity_minimal.json']
external +=[heavy/f'reps{i}.npy' for i in range(1,10)]
external +=[src/'vcache.pkl']
external +=[src.parent/'w4_typeclosed_lib.py']
artifacts=['three_minimum_barrier_replay.fano_v4_partner.json','fano_v4_partner_probe.log','fano_v4_partner_probe.worst.json','fano_v4_partner_focused.json','fano_v4_partner_focused.worst.json','fano_v4_partner_focused.log','classify_broad_partner_probe.json','three_minimum_barrier_replay.json','slab_9d8.json','slab_9d8_fastcert.json','slab_9d8_fastcheck.log','u12_hard_v4_cert.json','u12_hard_v4_check.log']
for prefix in ['balanced_point_optimal20','balanced_point_anchor12']:
    artifacts +=[prefix+suf for suf in ['.sqlite','.status.json','.frontier.json','.frontier.pkl','.diagnostic.json','.diagnostic.log','.diagnostic.anchor_pair.json','.log']]
artifacts += ['balanced_point_optimal20.template_check.json','balanced_point_anchor12.diagnostic.existing_v4.json']
artifacts += ['critical_cube_partners'+s for s in ['.json','.sqlite','.sqlite-wal','.sqlite-shm','.status.json','.log']]
artifacts += ['check_endpoint_menu_barrier.json','endpoint_u_all_support.json','endpoint_u_all_support.log',
              'endpoint_new_template.template.json','endpoint_new_template.certificate.json','endpoint_new_template.log',
              'endpoint_interval_certificate.json','endpoint_223_terminal_cover.json','endpoint_223_terminal_pair.json',
              'check_new223_facets.json','check_endpoint_cone.json']
extra_artifacts = [root/'outputs'/f for f in [
    'paper_push_endpoint_counterstate.json','paper_push_endpoint_counterstate.fano_v4_partner.json',
    'paper_push_endpoint_counterstate.repeated_response.json','paper_push_endpoint_counterstate.repeated_full_menu.json',
    'paper_push_endpoint_counterstate.repeated_with223.json','paper_push_endpoint_repair.md','paper_push_new223.md']]
command='python3 work/paper_push/three_cert/resume_search.py 3/4,3/4,4/5 3/4,3/4,4/5 balanced work/paper_push/three_cert/balanced_point_anchor12 --seconds 300 --facet 1 --requests 12 --max-types 16 --optimal-blocker --strict-types --strong-blocker --disjoint --anchor-pair'
out={'status':'CHECKPOINTED_NO_ACTIVE_JOB_NEW223_INTERVAL_AND_CONE_PROVED_FULL_TH3_OPEN','cwd':str(root),
     'created':'2026-09-26','runtime':{'python':platform.python_version(),'executable':sys.executable,'numpy':numpy.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__},
     'resume_command':command,'resume_caution':'Command is documented, not running. Keep all flags and prefix to reuse matching SQLite completed subtrees. CPU budget may be changed. No complete theorem follows from a checkpoint.',
     'local_pipeline':[row(base/f,'task-local source') for f in local],
     'read_only_dependencies':[row(p,'original Claude dependency; preserve in place') for p in external if p.exists()],
     'artifacts':[row(base/f,'proof or preserved checkpoint') for f in artifacts if (base/f).exists()]+[row(p,'exact obstruction, quantified result, or independent theory report') for p in extra_artifacts if p.exists()],
     'report':row(root/'outputs/paper_push_three_cert.md','current coherent status and exact scope'),
     'proof_scope':'Balanced median>=9/8 exact-certified; full unbalanced and min>=6/7 hand results reported by root. NEW223 capacity formula complete by77520 exactbases, endpoint interval bound3/4−1.047t certified by24primal witnesses, fan-in cone bound3/4−g+j certified by600affine vertex checks. Full Th(3) and unrestricted3/4bound unresolved. Root owns separate unrestricted6/7bound.',
     'checking':{'ordinary':f'python3 {src}/check5.py CERT.json','extended':'python3 work/paper_push/three_cert/conditional_check.py CERT.json','producer':'python3 work/paper_push/three_cert/progress_certify.py TREE.json CERT.json',
                 'new223_complete':'python3 work/paper_push/three_cert/check_new223_facets.py',
                 'endpoint_interval':'python3 work/paper_push/three_cert/check_endpoint_interval.py',
                 'fanin_cone':'python3 work/paper_push/three_cert/check_endpoint_cone.py'},
     'discovery_limits':['Numerical template/request selection is not proof.','At >9 types with max-types>11, Fano menu contains <=3-color assignments only. V4/mixed menus retain all4-role assignments.','No complete capacity-point tree resulted from either focused timeout. Feasible frontier samples already fit some templates.',
                         'The initial one-response Fano partner oracle means one occurrence; repeated_response_oracle.py permits repeated occurrences of the single new type.',
                         'The near-critical cube tree finished withFAIL leaves; it proves no cube theorem. Its restricted menu has an exact obstruction, subsequently closed byNEW223 on the stated interval and cone.']}
(base/'resume_manifest.json').write_text(json.dumps(out,indent=2))
print('MANIFEST',len(out['local_pipeline']),'local files;',len(out['read_only_dependencies']),'read-only dependencies;',len(out['artifacts']),'artifacts')
