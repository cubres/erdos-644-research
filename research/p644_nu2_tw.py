"""ν=2 at budget T=12 (r=16): the tall/wide strategy.  Edges 1=A1, 2=A2 (disjoint);
3,4,5 = tall requests (column quarter q_j + 8 rows), 6..9 = wide requests (q4 ∪ q_j + the rows N_j
that tall answer j used).  Target: {3..9} is a bad 7-tuple."""
import sys, time
from p644_nu2_tree import *
import p644_strategy2 as S2

def in_edge_side(side, j):            # atoms of A_side (1 or 2) lying in edge j
    return both(contains(side), contains(j))
def notpicks(pred, *names):
    for n in names: pred = both(pred, notin(n))
    return pred

def tw_steps(variant='A'):
    st = {}
    # quarters of A1 as picks Q1..Q3 (Q4 = rest)
    st[3] = {'picks': [('Q1', IN1, 4), ('R1', IN2, 8)], 'avoid': ['Q1', 'R1']}
    N1 = in_edge_side(2, 3)                                        # A2 ∩ C3
    st[4] = {'picks': [('Q2', notpicks(IN1, 'Q1'), 4), ('R2', both(IN2, lambda E, L, p: 3 not in E), Aff(8) - mass(N1))],
             'avoid': ['Q2', N1, 'R2']}
    N2 = in_edge_side(2, 4)
    N12 = both(IN2, lambda E, L, p: (3 in E) or (4 in E))
    st[5] = {'picks': [('Q3', notpicks(IN1, 'Q1', 'Q2'), 4), ('Pa', N12, 8),
                       ('Pb', both(IN2, lambda E, L, p: (3 not in E) and (4 not in E)), Aff(8) - mass(inpick('Pa')))],
             'avoid': ['Q3', 'Pa', 'Pb']}
    N3 = in_edge_side(2, 5)
    Q4 = notpicks(IN1, 'Q1', 'Q2', 'Q3')
    st[6] = {'picks': [('H1', N1, 4)], 'avoid': [Q4, inpick('Q1'), 'H1']}
    st[7] = {'picks': [('H2', N2, 4)], 'avoid': [Q4, inpick('Q2'), 'H2']}
    st[8] = {'picks': [('H3', N3, 4)], 'avoid': [Q4, inpick('Q3'), 'H3']}
    N4p = both(IN2, lambda E, L, p: not ({3, 4, 5} & E))
    st[9] = {'picks': [('H4', N4p, 4)], 'avoid': [Q4, inpick('Q1'), 'H4']}
    return st, 9

if __name__ == '__main__':
    st, J = tw_steps()
    run('TW', st, J, (0, 16), (0, 16), budget=True, tl=1800)

def run2(name, st, J, tl=3600):
    t0 = time.time(); sc = script(st, J, (0, 16), (0, 16))
    out = S2.solve(sc, time_limit=tl, want=True, continuous=True, verbose=True)
    print(f"{name}: {out['status']} [{time.time()-t0:.0f}s]", flush=True)
    if out['status'].startswith('ADVERSARY'): show(out)
    elif out['status'].startswith('PROVER'):
        print('  budget:', S2.check_budget(sc, time_limit=tl, continuous=True), flush=True)
    return out
