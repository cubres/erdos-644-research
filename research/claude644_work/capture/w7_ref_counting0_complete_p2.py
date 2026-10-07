#!/usr/bin/env python3
"""w7_ref_counting0_complete_p2.py n k p pi [refined] -- phase 2 only of w7_ref_counting0_complete.py at a GIVEN
(p,pi) (use when (p,pi) is a proven lower bound, so feasibility => it is the lex minimum).  Exact re-check of witness."""
import sys
import w7_ref_counting0_complete as C
n, k, p, pi = map(int, sys.argv[1:5]); ref = len(sys.argv) > 5
res, idx = C.solve(n, k, phase2=(p, pi), refined=ref, time_limit=550)
print('n,k,p,pi', n, k, p, pi, 'refined', ref, 'status', res.status, res.message)
if res.x is not None:
    blocks = [set(v for v in range(n) if res.x[idx[('x', v, j)]] > .5) for j in range(7)]
    print(' blocks', [sorted(b) for b in blocks]); print(' exact:', C.exact_check(n, k, blocks))
