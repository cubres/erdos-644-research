"""Coverage check for a family of REGION certificates of the separated regime (std lib only).
Target: every x with x_i + x_j >= 3/2 for all pairs (separated regime).  Each certificate must be VALID
(run check_gen_cert.py on it first) and is either
  * unordered with pi0 = p and no region rows: covers {all pair sums >= 3/2 + p};
  * ordered ('order': true, sep mode, pi0 = 0) with 'pairs' = [[0, 1, lo, hi]] only: covers the ordered points with
    x_0 + x_1 in [lo, hi] (x_0 + x_1 is the smallest pair sum), hence, by the verified permutation invariance, all x
    whose smallest pair sum lies in [lo, hi].
The union must contain [3/2, infinity) for the smallest pair sum.
usage: python3 -S check_cover.py cert1.json cert2.json ..."""
import sys, json
from fractions import Fraction as F
iv = []
for fn in sys.argv[1:]:
    D = json.load(open(fn)); S = D['strategy']
    assert S.get('mode', 'sep') == 'sep' and not S.get('xbox') and not S.get('taubox'), fn
    if not S.get('order'):
        assert not S.get('pairs'), fn
        iv.append((F(3, 2) + F(D['pi0']), None, fn))
    else:
        assert F(D['pi0']) == 0 and len(S.get('pairs', [])) == 1, fn
        i, j, lo, hi = S['pairs'][0]; assert (i, j) == (0, 1), fn
        iv.append((F(lo), F(hi) if hi is not None else None, fn))
iv.sort(key=lambda r: r[0])
reach = F(3, 2); ok = True
for lo, hi, fn in iv:
    if lo > reach: print('GAP in smallest pair sum: [%s, %s)' % (reach, lo)); ok = False; break
    if hi is None: reach = None; break
    reach = max(reach, hi)
if ok and reach is not None:
    print('NOT COVERED above', reach); ok = False
for lo, hi, fn in iv: print('  %s: smallest pair sum in [%s, %s]' % (fn, lo, hi if hi is not None else 'inf'))
print('SEPARATED REGIME COVERED' if ok else 'NOT COVERED')
