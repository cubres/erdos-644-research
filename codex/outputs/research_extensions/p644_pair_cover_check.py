"""Independent finite regressions for the two-request finishing formula.

Every simple graph on four labelled vertices and every zero/one mass vector
is checked against exhaustive assignments of minimal request-label families.
This supports the hand proof; it is not a substitute for that proof.
"""
from fractions import Fraction as F
from itertools import combinations,product


def concept_cost(adj,raw):
    n=len(adj);full=(1<<n)-1
    weights=[v if any(raw[j]>0 for j in range(n) if adj[i]>>j&1) else 0 for i,v in enumerate(raw)]
    def nonneighbors(a):
        out=full
        for i in range(n):
            if a>>i&1:out &= full^adj[i]
        return out
    mass=lambda a:sum(weights[i] for i in range(n) if a>>i&1)
    best=None
    for a in range(1<<n):
        b=nonneighbors(a)
        if nonneighbors(b)!=a:continue
        c=full^(a|b)
        value=max(mass(c|(a&~b)),mass(c|(b&~a)),F(mass(full)+mass(c),2))
        best=value if best is None else min(best,value)
    return best


def direct_cost(adj,raw):
    used=[i for i,m in enumerate(raw) if m>0 and any(raw[j]>0 for j in range(len(raw)) if adj[i]>>j&1)]
    families=[(1,),(2,),(3,),(1,2)]
    best=None
    for choice in product(range(4),repeat=len(used)):
        if any(not all(a&b for a in families[choice[i]] for b in families[choice[j]])
               for i,j in combinations(range(len(used)),2) if adj[used[i]]>>used[j]&1):continue
        one=sum(raw[used[i]] for i,q in enumerate(choice) if q in (0,2))
        two=sum(raw[used[i]] for i,q in enumerate(choice) if q in (1,2))
        flexible=sum(raw[used[i]] for i,q in enumerate(choice) if q==3)
        value=max(one,two,F(one+two+flexible,2))
        best=value if best is None else min(best,value)
    return best


def main():
    assert concept_cost([2,1],[1,0])==0
    assert concept_cost([2,1],[1,1])==F(3,2)
    edges=list(combinations(range(4),2));count=0
    for mask in range(64):
        adj=[0]*4
        for i,(a,b) in enumerate(edges):
            if mask>>i&1:adj[a]|=1<<b;adj[b]|=1<<a
        for masses in product((0,1),repeat=4):
            assert concept_cost(adj,masses)==direct_cost(adj,masses),(mask,masses)
            count+=1
    print('PASS:',count,'graph/mass cases and the zero-neighbor boundary regression.')


if __name__=='__main__':main()
