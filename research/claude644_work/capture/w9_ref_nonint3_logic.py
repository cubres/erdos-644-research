"""Referee w9, nonint#3 (Lemma H). Exhaustive check of the badness logic of the anchored 7.97 tuple.
Rows: A (index 0), G1..G6 (index 1..6). Point classes:
  U\\C, label L in {12,34,56}: not in A, not in G_i (i in L), arbitrary in the other G_j;
  C, triple T in {135,146,236,245}: in A, not in G_i (i in T), arbitrary elsewhere;
  outside U: in no G_i (G_i inside U); in A or not.
Claim: for ANY realisation of the arbitrary bits, every pair (x,y) (x=y allowed) is missed by some row.
We enumerate all membership vectors of each class and all pairs. Mutation tests confirm the checker bites."""
import itertools
def vectors(inA, forced_out, allowed_in):
    res = []
    free = [j for j in range(1,7) if j not in forced_out and j in allowed_in]
    for bits in itertools.product([0,1], repeat=len(free)):
        s = {0} if inA else set()
        s |= {j for j,b in zip(free,bits) if b}
        res.append(frozenset(s))
    return res
def check(pairlabels, triplabels, verbose=False):
    allrows = set(range(1,7))
    V = []
    for L in pairlabels: V += vectors(False, {int(c) for c in L}, allrows)
    for T in triplabels: V += vectors(True, {int(c) for c in T}, allrows)
    V += [frozenset({0}), frozenset()]          # outside U, in A / not in A
    full = set(range(7))
    bad_pairs = [(a,b) for a in V for b in V if (a|b) >= full]
    return len(V), bad_pairs
n, bp = check(['12','34','56'], ['135','146','236','245'])
print('main: #vectors', n, 'pairs with union = all 7 rows:', len(bp))
assert not bp
# mutations (each should produce a 2-transversal somewhere)
muts = [ (['12','34','15'], ['135','146','236','245']),
         (['12','34','56'], ['135','146','236','246']),
         (['12','34','56'], ['13','146','236','245']),
         (['1','34','56'],  ['135','146','236','245']) ]
for pl, tl in muts:
    n, bp = check(pl, tl); print('mutation', pl, tl, '-> pierced pairs', len(bp))
    assert bp
# block membership: every i in exactly one pair label and exactly two triple labels
for i in '123456':
    assert sum(i in L for L in ['12','34','56']) == 1 and sum(i in T for T in ['135','146','236','245']) == 2
print('each block P_i = 1 pair-class + 2 triple-classes: OK')
