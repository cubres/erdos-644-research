# Referee w7 counting#1: the 'significance' list ("exactly which local structures give positive D").
# Build tuples from prescribed missing sets (rows 0..5) and compute exact costs with the independent evaluator.
from w7_ref_counting1_brk import analyse, audit
def build(missing):  # list of missing sets (tuples of row indices) -> rows bitmasks
    rows = [0]*6
    for v, ms in enumerate(missing):
        for i in range(6):
            if i not in ms: rows[i] |= 1 << v
    return len(missing), rows
cases = {
 # (a) G4 contains {0,1} and {0,2}; v has sigma={0,1} (missing {2,3,4,5}): eligible degree-2 with q>=1
 'elig_deg2': [(0,1),(0,2),(2,3,4,5),(3,4),(3,5)],
 # (b) eligible degree-3 with q<=1 (c<=0): v missing {0,1,2}; partner missing {3,4} (disjoint -> eligible)
 'elig_deg3_q_small': [(0,1,2),(3,4),(3,5),(4,5)],
 # (c) eligible degree-3 with q=3 (c=+2): v missing {0,1,2}, disjoint partner {3,4}, exact partners {0,3},{1,4},{2,5}
 'elig_deg3_q3': [(0,1,2),(3,4),(0,3),(1,4),(2,5)],
}
for name, ms in cases.items():
    n, rows = build(ms)
    out, (m, d, e, q, c, P, Pi, deg5, deg6) = audit(n, rows)
    print(name, 'deg5', deg5, 'deg6', deg6, 'audit ok', all(out.values()))
    for v in range(n): print('   missing', ms[v], 'd', d[v], 'e', e[v], 'q', q[v], 'c', c[v])
