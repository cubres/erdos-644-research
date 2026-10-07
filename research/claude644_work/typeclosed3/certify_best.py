"""Exact certification (Fractions, all 715 supports, all assignments via pruned DFS) of the best families of the
cex climbs: 'no bad tuple' + exact tau*.  Usage: python3 certify_best.py logfile"""
import sys, ast, re, time
from fractions import Fraction as Fr
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from badcheck import full_check, verify_tuple, general_bad, general_bad_int, two_type_bad, fano_bad
from tc3lib import tau_star
fn = sys.argv[1]
lines = open(fn).read().splitlines()
blocks = []
for i, l in enumerate(lines):
    if l.startswith('restart') and i + 1 < len(lines) and lines[i + 1].startswith('   K'):
        x = ast.literal_eval(re.search(r'x (\[[^\]]*\])', l).group(1)); K = ast.literal_eval(lines[i + 1][5:])
        tau = float(re.search(r'tau\* ([0-9.]+)', l).group(1)); blocks.append((tau, x, K, l))
blocks.sort(key=lambda b: -b[0])
for tau, x, K, l in blocks[:3]:
    print('##', l[:120], flush=True)
    xr = [Fr(v).limit_denominator(10000) for v in x]
    Kr = []
    for c in K:
        cr = [Fr(v).limit_denominator(10000) for v in c]
        s = sum(cr); j = max(range(3), key=lambda i: cr[i]); cr[j] -= (s - 1)
        cr = [min(v, xr[i]) for i, v in enumerate(cr)]; Kr.append(tuple(cr))
    t0 = time.time()
    tau = tau_star(Kr, xr); pr = two_type_bad(Kr, xr); fa = fano_bad(Kr, xr)
    print('   exact tau* = %s = %.5f ; pair %s ; fano %s' % (tau, float(tau), pr, fa), flush=True)
    g = general_bad_int(Kr, xr, verbose=True)
    print('   general (exact integer DFS over 715 supports): %s   [%.0fs]' % (g, time.time() - t0), flush=True)
    if g:
        print('   verify:', verify_tuple(Kr, xr, *g))
    print('   x =', [str(v) for v in xr]); print('   K =', [[str(v) for v in c] for c in Kr], flush=True)
