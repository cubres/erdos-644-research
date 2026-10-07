"""Append the completed private-family reports without replacing old research."""
from pathlib import Path
import hashlib

ROOT = Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd')
RESEARCH = Path('/Users/cubres/Documents/Clauding/erdos-hunt')
main = RESEARCH / 'note_644.md'
mirror = ROOT / 'outputs/note_644.md'
expected = 'e50ba41fed68dd41cdc5e7e07bab348fa556a8d2c5f373401aeea8e27cda7b6e'
old = main.read_bytes()
assert old == mirror.read_bytes(), 'Research copies diverged; do not overwrite.'
assert hashlib.sha256(old).hexdigest() == expected, 'Unexpected current note; do not overwrite.'

reports = [
    (187, 'agent_arbitrary_private_families.md',
     'Full hand proofs. The omission-core inequalities require the stated genuine localized certificates; neither localization nor small leakage is automatic. The complete-family example is an actual boundary example, while the three-disjoint-traces construction in subsection 6 is only a trace-level obstruction.'),
    (188, 'agent_nu2_global_residual_attack.md',
     'Full hand proofs. The bin requests are made against the entire actual family, and the critical-cover inequalities hold for every indicated subset of centers. The cross-only obstruction deliberately fails the full seven-edge property and is not a counterexample to the problem. No general disjoint-edge upper bound is asserted.'),
    (189, 'agent_critical_kernel_literature_bridge.md',
     'The cited primary critical-order and covering-clutter results were read at the relevant theorem statements. The blocker, strong-stability, and asymptotic-constant obstructions are hand arguments. The literature search was bounded; failure to find a later resolution is not an exhaustive status certificate.'),
    (190, 'root_private_pair_residual_and_outside_cores.md',
     'Full hand proofs using actual rows and actual residual subfamilies. The outside-intersection conclusions and their scopes were independently checked by the private-family agent. A residual can retain its exact transversal number without lowering its rank, so these reductions alone do not preserve a fixed excess above three quarters.'),
    (191, 'root_common_partition_sublinear_pruning.md',
     'Full hand proofs. The private-family agent independently checked the three-wise intersection, greedy outside transversal, and actual pruning argument. The disjoint-edge agent independently checked the normalization example, including the assertion about every minimum cover. The pruning is excess-preserving in the stated common-partition branch; subsequent critical-cover normalization remains an unproved step.'),
]

parts = []
for number, filename, scope in reports:
    source = ROOT / 'outputs' / filename
    raw = source.read_text()
    title, body = raw.split('\n', 1)
    assert title.startswith('# ')
    shifted = []
    for line in body.splitlines():
        if line.startswith('#'):
            line = '##' + line
        shifted.append(line)
    parts.append('\n\n### 7.%d %s\n\nSource report: [%s](%s).\n\n%s\n\nRoot integration and scope: %s\n' % (
        number, title[2:], filename, source, '\n'.join(shifted).strip(), scope))

addition = ''.join(parts).encode()
with main.open('ab') as out:
    out.write(addition)
with mirror.open('ab') as out:
    out.write(addition)
new = main.read_bytes()
assert new == mirror.read_bytes()
print('INTEGRATED sections 7.187-7.191')
print('SHA256', hashlib.sha256(new).hexdigest())
print('Added bytes', len(addition))
