"""Parse the last 'restart' block(s) of a climb log (x and K lines), rationalise, and run the exact checks.
Usage: python3 check_log_family.py logfile [all]"""
import sys, ast, re
from fractions import Fraction as Fr
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from badcheck import full_check, verify_tuple
from fastlib import triple_window_value, classes_f
import numpy as np

fn = sys.argv[1]
lines = open(fn).read().splitlines()
blocks = []
for i, l in enumerate(lines):
    if l.startswith('restart') and i + 1 < len(lines) and lines[i + 1].startswith('   K'):
        x = ast.literal_eval(re.search(r'x (\[[^\]]*\])', l).group(1))
        K = ast.literal_eval(lines[i + 1][5:])
        tau = float(re.search(r'tau\* ([0-9.]+)', l).group(1))
        blocks.append((tau, x, K, l))
if not blocks:
    print('no blocks'); sys.exit()
sel = blocks if len(sys.argv) > 2 else [max(blocks, key=lambda b: b[0])]
for tau, x, K, l in sel:
    print('##', l[:110])
    xr = [Fr(v).limit_denominator(10000) for v in x]
    Kr = []
    for c in K:
        cr = [Fr(v).limit_denominator(10000) for v in c]
        # fix mass exactly 1 by adjusting the largest coordinate
        s = sum(cr); j = max(range(3), key=lambda i: cr[i]); cr[j] -= (s - 1)
        cr = [min(v, xr[i]) for i, v in enumerate(cr)]
        Kr.append(tuple(cr))
    print('   triple-window value %.4f classes %s' % (triple_window_value(np.array(K), np.array(x)), [list(map(int, s)) for s in classes_f(np.array(K), np.array(x))]))
    r = full_check(Kr, xr)
    if r['general']:
        print('   verified exactly:', verify_tuple(Kr, xr, *r['general']))
