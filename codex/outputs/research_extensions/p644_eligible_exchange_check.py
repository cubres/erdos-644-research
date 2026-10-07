"""Exact consistency check for the hand K3,3-core exchange obstruction."""
from itertools import combinations


def eligible_mass(cells,rows):
    target=sum(1<<j for j in rows)
    assert not any(m&target==target for m,w in cells if w)
    return sum(w for m,w in cells if w and any(v and (m|n)&target==target for n,v in cells))


def check():
    for rank in (4,5,8,20,101):
        cross=[((1<<i)|(1<<(3+j)),1) for i in range(3) for j in range(3)]
        old=[(7,rank-3),(56,rank-3)]+cross
        assert eligible_mass(old,range(6))==2*rank-6
        cells=[(7,rank-4),(7|64,1),(56,rank-4),(56|64,1),(64,rank-2)]+cross
        cells=[(m,w) for m,w in cells if w]
        assert all(sum(w for mask,w in cells if mask>>j&1)==rank for j in range(7))
        assert all(sum(w for mask,w in cells if mask>>i&1 and mask>>j&1)>0 for i,j in combinations(range(7),2))
        assert any((a|b)==127 for a,w in cells for b,v in cells if w and v)
        for omit in range(7):assert eligible_mass(cells,[j for j in range(7) if j!=omit])>=2*rank-6
    print('PASS: five ranks; all seven edges pairwise intersect; initial eligible size2k-6; every six-row eligible set at least2k-6 and every sixfold intersection empty. Avoidance for arbitrary D follows from |D|<k-3=|A|=|B|.')


if __name__=='__main__':check()
