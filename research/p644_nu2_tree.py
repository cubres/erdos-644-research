"""Erdős #644 — matching number 2: case-tree harness at budget T (units of r/16, r = 16).

Edges 1 = A1, 2 = A2 (disjoint), 3 = A3 = the first requested edge.  Cells are intervals of
(a13, a23).  Scripts are lists of steps with affine pick sizes; the continuous MILP decides a whole
cell at once, and check_budget certifies legality (max avoided mass over the prefix <= T).
"""
import sys, time, itertools, json
from p644_strategy import *

R, T = 16, 12
A12 = mass(contains(1, 2)); A13 = mass(contains(1, 3)); A23 = mass(contains(2, 3))
Tr = (1, 2, 3)
IN1 = contains(1); IN2 = contains(2)
C13 = cellin(Tr, 1, 3); C23 = cellin(Tr, 2, 3); C1o = cellin(Tr, 1); C2o = cellin(Tr, 2); C3o = cellin(Tr, 3)

def script(steps, J, I13, I23, extra_hyps=(), intersecting=False):
    hyps = [(A12, 0, 0, (1, 2)), (A13, I13[0], I13[1], (1, 3)), (A23, I23[0], I23[1], (2, 3))] + list(extra_hyps)
    return Script(J, R, T, steps, intersecting=intersecting, hyps=hyps)

def show(out):
    """Pretty-print an adversary configuration: atoms grouped by side."""
    if 'atoms' not in out: return
    rows = []
    for (E, L), m in sorted(out['atoms'].items(), key=lambda kv: (1 not in kv[0][0], 2 not in kv[0][0], kv[0])):
        side = 'A1' if 1 in E else ('A2' if 2 in E else 'X ')
        rows.append(f"   {side} edges={''.join(str(e) for e in E):8s} picks={','.join(L) or '-':16s} mass={m}")
    print('\n'.join(rows))

def run(name, steps, J, I13, I23, extra_hyps=(), want=True, budget=True, tl=600):
    t0 = time.time()
    sc = script(steps, J, I13, I23, extra_hyps)
    out = solve(sc, time_limit=tl, want=want, continuous=True)
    line = f"{name} cell a13∈{I13} a23∈{I23}: {out['status']} [{time.time()-t0:.0f}s]"
    if budget and out['status'].startswith('PROVER'):
        rep = check_budget(sc, time_limit=tl)
        line += f" budget={rep} {'LEGAL' if all(v is None or v <= T + 1e-6 for v in rep.values()) else 'ILLEGAL'}"
    print(line, flush=True)
    if out['status'].startswith('ADVERSARY') and want: show(out)
    return out

# ---------- building blocks ----------
def base(s1, s2):
    """Step 3: A3 avoids S1 ⊆ A1 (s1 units) and S2 ⊆ A2 (s2 units)."""
    return {3: {'picks': [('S1', cellin((1, 2), 1), s1), ('S2', cellin((1, 2), 2), s2)], 'avoid': ['S1', 'S2']}}

def lemma7_steps(s1, s2):
    """Lemma 7 (a13, a23 <= 4): A4 avoids A13 ∪ Y4 (Y4 ⊆ A2', |Y4| = T - a13); A5 avoids A23 ∪ Y5;
    A6 avoids A13 ∪ (A4 ∩ A2); A7 avoids (A5 ∩ A1) ∪ A23."""
    st = base(s1, s2)
    st[4] = {'picks': [('Y4', C2o, Aff(T) - A13)], 'avoid': [C13, 'Y4']}
    st[5] = {'picks': [('Y5', C1o, Aff(T) - A23)], 'avoid': [C23, 'Y5']}
    st[6] = {'avoid': [C13, both(IN2, contains(4))]}
    st[7] = {'avoid': [both(IN1, contains(5)), C23]}
    return st, 7

if __name__ == '__main__':
    # sanity: Lemma 7 on the cell a13, a23 in [0,4]  (both sides), and its failure just outside
    run('L7', *lemma7_steps(6, 6), (0, 4), (0, 4))
    run('L7', *lemma7_steps(6, 6), (4, 5), (0, 4))
    run('L7', *lemma7_steps(6, 6), (0, 4), (4, 6))
