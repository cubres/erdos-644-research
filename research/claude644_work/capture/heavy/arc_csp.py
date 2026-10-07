"""Fano-plane CSP behind super-heavy families: colour the 7 lines by classes {A,B,C} (rows super-heavy at that
class's part => each colour class is an ARC: no 3 concurrent lines).  A point 'pattern' is the multiset of the
colours of its 3 lines.  For each set F of forbidden mixed patterns, is there a colouring avoiding F?
Lists the MINIMAL forbidden sets F that make the CSP unsatisfiable (=> no Fano tuple, whatever the traces)."""
import itertools
from heavylib import LINES, PENCIL
PATS = ['AAB','AAC','BBA','BBC','CCA','CCB','ABC']
def pat(cols, q):
    return ''.join(sorted(cols[l] for l in PENCIL[q]))
norm = {''.join(sorted(p)): p for p in PATS}
cols_ok = []
for cols in itertools.product('ABC', repeat=7):
    pats = [pat(cols, q) for q in range(7)]
    if any(p in ('AAA','BBB','CCC') for p in pats): continue
    cols_ok.append(frozenset(norm[p] for p in pats))
print("arc colourings:", len(cols_ok), " distinct pattern sets used:", len(set(cols_ok)))
used = set(cols_ok)
unsat = []
for r in range(1, 8):
    for F in itertools.combinations(PATS, r):
        Fs = set(F)
        if any(Fs >= set(u) for u in unsat): continue
        if all(u & Fs for u in used): unsat.append(F)
print("minimal unsatisfiable forbidden sets:")
for F in unsat: print("  ", F)
