"""Exact cheapest single box request closed by the two V5 anchor orientations.

All mathematical decisions use fractions. This is a constructive application of
the hand lemma in paper_push_three_theory.md, not a feasibility heuristic.
"""
from fractions import Fraction as F
from itertools import product, combinations
import json
import sys


def thresholds(x, a, b):
    return tuple(min(2*z-2*v-w, 4*z-5*v-w) for z,v,w in zip(x,a,b))


def outside_witness_indices(u, r, s):
    """Return indices witnessing an uncovered unit response, else None.

    The box must be nonnegative and have total capacity at least one.
    """
    assert all(v >= 0 for v in u) and sum(u) >= 1
    for i in range(len(u)):
        if max(r[i],s[i]) < min(u[i],1):
            return i,i
        for j in range(len(u)):
            if i != j and u[i] > r[i] and u[j] > s[j] and max(0,r[i])+max(0,s[j]) < 1:
                return i,j
    return None


def optimal_request(x, a, b):
    x,a,b = [tuple(map(F,t)) for t in (x,a,b)]
    assert sum(a) == sum(b) == 1
    assert all(0<=v<=z and 0<=w<=z for z,v,w in zip(x,a,b))
    r,s = thresholds(x,a,b),thresholds(x,b,a)
    grids = [sorted({z}|{q for q in (v,w) if 0<=q<=z}) for z,v,w in zip(x,r,s)]
    # The universal N-1 bound is an infimum, so has no closed request box.
    best = {'cost':sum(x)-1,'request':None,'R':r,'S':s}
    for u in product(*grids):
        if sum(u)<1 or outside_witness_indices(u,r,s) is not None:
            continue
        cost=sum(x)-sum(u)
        if cost<=best['cost']:
            best = {'cost':cost,'request':u,'R':r,'S':s}
    return best


def print_result(label, r):
    print(label,json.dumps(r,default=str,sort_keys=True),'floatcost',float(r['cost']))


if __name__=='__main__':
    x=tuple(F(t,140) for t in (106,106,112))
    a=tuple(F(t,140) for t in (71,69,0))
    b=tuple(F(t,140) for t in (65,0,75))
    r=optimal_request(x,a,b)
    assert r['cost']==F(51,70)
    print_result('FIXED',r)
    for filename in sys.argv[1:]:
        data=json.load(open(filename)); x=tuple(map(F,data['capacities']))
        ts=[tuple(map(F,t)) for t in data['types']]
        results=[(optimal_request(x,ts[i],ts[j]),i,j) for i,j in combinations(range(len(ts)),2)]
        results.sort(key=lambda q:q[0]['cost'])
        for r,i,j in results[:6]:
            print_result(f'{filename} pair {i},{j}',r)
