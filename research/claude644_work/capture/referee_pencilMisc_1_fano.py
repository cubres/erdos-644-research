#!/usr/bin/env python3
"""Referee check 1: Fano facts used by the pencil lemmas (independent of the author's scripts).

Points: p0,a,a2,b,b2,c,c2 (a2 = a', etc.).
Checks
 (1) the seven lines form PG(2,2) (every pair of points on exactly one line);
 (2) m-lines miss p0; each non-p0 point lies on exactly one pencil line and two m-lines;
 (3) 'safe' characterisation: a line set is safe iff contained in the 4 lines missing a point;
 (4) Venn/Fano lemma, exhaustively on a tiny model: if every vertex's membership set sigma is safe,
     the 7 sets have no transversal of size <= 2 (checked by brute force over all sigma patterns
     realised on 2 vertices -- i.e. every pair of safe patterns, including equal ones);
 (5) protrusion pairing: an outside vertex lying in G_l2 only / G_l3 only / both, with the stated
     m-lines removed, has a safe sigma (for every subset of the allowed m-lines);
 (6) disjoint-pair / anchor labelling: F on b,b2,c,c2 serves l1; G on a,a2 serves l2 and l3;
     every label's allowed lines are exactly the lines missing it.
"""
import itertools

P = ['p0', 'a', 'a2', 'b', 'b2', 'c', 'c2']
LINES = {
    'l1': {'p0', 'a', 'a2'}, 'l2': {'p0', 'b', 'b2'}, 'l3': {'p0', 'c', 'c2'},
    'M1': {'a', 'b', 'c'}, 'M2': {'a2', 'b2', 'c'}, 'M3': {'a2', 'b', 'c2'}, 'M4': {'a', 'b2', 'c2'},
}
PENCIL = ['l1', 'l2', 'l3']
MLINES = ['M1', 'M2', 'M3', 'M4']

# (1)
for x, y in itertools.combinations(P, 2):
    n = sum(1 for L in LINES.values() if x in L and y in L)
    assert n == 1, (x, y, n)
assert all(len(L) == 3 for L in LINES.values())
# (2)
for M in MLINES:
    assert 'p0' not in LINES[M]
for x in P[1:]:
    assert sum(x in LINES[l] for l in PENCIL) == 1
    assert sum(x in LINES[l] for l in MLINES) == 2

def safe(S):
    U = set()
    for l in S:
        U |= LINES[l]
    return len(U) < 7

# (3)
missing = {p: frozenset(l for l in LINES if p not in LINES[l]) for p in P}
for r in range(8):
    for S in itertools.combinations(LINES, r):
        s = safe(S)
        t = any(set(S) <= missing[p] for p in P)
        assert s == t
        if r <= 2:
            assert s
        if r == 3:
            conc = any(all(p in LINES[l] for l in S) for p in P)
            assert s == (not conc)
        if r == 4:
            assert s == any(set(S) == missing[p] for p in P)
# (4) Venn/Fano: vertices x,y with safe sigma(x), sigma(y): some line's set misses both.
safes = [frozenset(S) for r in range(5) for S in itertools.combinations(LINES, r) if safe(S)]
for s1 in safes:
    for s2 in safes:
        # the pair {x,y} is covered by all 7 sets iff every line is in s1 or s2
        assert set(LINES) - (s1 | s2), (s1, s2)
# (5) protrusion pairing
# outside vertex in G_l2 only: M1,M4 avoid it  -> sigma subset {l2,M2,M3}
# in G_l3 only: M2,M3 avoid it -> sigma subset {l3,M1,M4}; in both: sigma subset {l2,l3}
# in neither (outside, label p0): sigma subset of m-lines
cases = [({'l2'}, {'M2', 'M3'}), ({'l3'}, {'M1', 'M4'}), ({'l2', 'l3'}, set()), (set(), set(MLINES))]
for forced, allowedM in cases:
    for r in range(len(allowedM) + 1):
        for S in itertools.combinations(sorted(allowedM), r):
            assert safe(forced | set(S)), (forced, S)
# the pairing is the one stated: M1,M4 are the m-lines through a ; M2,M3 through a2
assert {l for l in MLINES if 'a' in LINES[l]} == {'M1', 'M4'}
assert {l for l in MLINES if 'a2' in LINES[l]} == {'M2', 'M3'}
# (6)
for lab in ['b', 'b2', 'c', 'c2']:
    assert lab not in LINES['l1']
for lab in ['a', 'a2']:
    assert lab not in LINES['l2'] and lab not in LINES['l3']
# request sets for m-lines: pairs (F-class, G-class) each covered by exactly one m-line
for fl in ['b', 'b2', 'c', 'c2']:
    for gl in ['a', 'a2']:
        assert sum(1 for M in MLINES if fl in LINES[M] and gl in LINES[M]) == 1
print('all Fano checks passed')
