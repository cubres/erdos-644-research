# Common Fano-plane utilities for the lazy-labeling protrusion game.
# Steps are the 7 lines of the original Fano plane = the 7 points of the dual plane.
# In the dual plane, a "line" is a concurrent triple of original lines (= an original point).
# A vertex's membership pattern S (set of steps) is SAFE iff it contains no dual line.
import itertools
from fractions import Fraction

# dual Fano plane on points 0..6, lines = triples; standard labeling (difference set {0,1,3} mod 7)
LINES = [frozenset(((0 + i) % 7, (1 + i) % 7, (3 + i) % 7)) for i in range(7)]

def check_fano(lines):
    for a, b in itertools.combinations(range(7), 2):
        assert sum(1 for L in lines if a in L and b in L) == 1
    return True

check_fano(LINES)

def safe(S, lines=LINES):
    return not any(L <= S for L in lines)

def all_orders():
    return list(itertools.permutations(range(7)))

def relabel(lines, order):
    """order[t] = original point processed at time t. Return lines in time labels."""
    pos = {p: t for t, p in enumerate(order)}
    return [frozenset(pos[p] for p in L) for L in lines]

def canonical_orders(lines=LINES):
    """Representatives of orders modulo collineations: return list of time-labelled line systems (as sorted tuples), deduped."""
    seen = {}
    for order in itertools.permutations(range(7)):
        tl = tuple(sorted(tuple(sorted(L)) for L in relabel(lines, order)))
        if tl not in seen:
            seen[tl] = order
    return seen
