"""Referee w9, claim heavyparts#0 (arc-CSP classification).  Independent of heavy/heavylib.py.
PRIMAL form: rows sit on the 7 POINTS of PG(2,2) (lines {i,i+1,i+3} mod 7); Lemma 7.63 per part i:
row <= x_i, sum over each LINE <= 2x_i, total <= 4x_i.  (Dual of the attacker's lines/pencils form.)
Part A: exhaustive CSP -- colourings of points by A,B,C with no monochromatic line (caps), the pattern
multiset on each line, minimal hitting sets of forbidden mixed patterns (ABC included), and for each
admissible pattern set the achievable colour-count vectors (needed for the per-part totals)."""
import itertools
from collections import defaultdict
LINES = [tuple(sorted(((i) % 7, (i+1) % 7, (i+3) % 7))) for i in range(7)]
assert len(set(LINES)) == 7 and all(len(set(a) & set(b)) == 1 for a, b in itertools.combinations(LINES, 2))
MIXED = ['AAB', 'AAC', 'ABB', 'BBC', 'ACC', 'BCC', 'ABC']   # sorted multisets; ABB=BBA, ACC=CCA, BCC=CCB
def patterns(col):
    return [''.join(sorted(col[p] for p in L)) for L in LINES]

def enumerate_caps():
    out = []   # (colouring, frozenset of patterns, counts)
    for col in itertools.product('ABC', repeat=7):
        pats = patterns(col)
        if any(p in ('AAA', 'BBB', 'CCC') for p in pats): continue
        out.append((col, frozenset(pats), (col.count('A'), col.count('B'), col.count('C'))))
    return out

CAPS = enumerate_caps()
PATSETS = defaultdict(set)
for col, ps, cnt in CAPS: PATSETS[ps].add(cnt)

def minimal_hitting():
    sets = list(PATSETS)
    hit = [F for r in range(len(MIXED)+1) for F in itertools.combinations(MIXED, r)
           if all(set(F) & s for s in sets)]
    return [F for F in hit if not any(set(G) < set(F) for G in hit)]

if __name__ == '__main__':
    print('cap colourings:', len(CAPS), ' distinct pattern sets:', len(PATSETS))
    mh = minimal_hitting()
    print('minimal hitting (unsat) forbidden sets:')
    for F in mh: print('   ', F)
    print('pattern sets -> achievable (nA,nB,nC):')
    for ps, cnts in sorted(PATSETS.items(), key=lambda z: sorted(z[0])):
        print('   ', sorted(ps), sorted(cnts))
    print('any pattern set avoiding ABC?', any('ABC' not in ps for ps in PATSETS))
    print('colour-count vectors overall:', sorted({c for _, _, c in CAPS}))
