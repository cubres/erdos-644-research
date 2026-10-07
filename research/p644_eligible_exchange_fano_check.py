"""Exact finite checks for the hand-proved one-exchange obstruction."""
from itertools import product

LINES=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))


def eligible_mass(cells,rows):
    target=sum(1<<j for j in rows)
    assert not any(m&target==target for m,w in cells if w)
    return sum(w for m,w in cells if w and any(v and (m|n)&target==target for n,v in cells))


def check():
    B=set(LINES[-1]);masks=[sum(1<<j for j,line in enumerate(LINES[:-1]) if i not in line) for i in range(7)]
    total=0
    for scale in (2,3,11):
        masses=[(2 if i in B else 1)*scale for i in range(7)];rank=6*scale;budget=5*scale-1
        old=list(zip(masks,masses));assert eligible_mass(old,range(6))==rank
        for removed in range(128):
            if sum(v for i,v in enumerate(masses) if removed>>i&1)>budget:continue
            cells=[];used=0
            for i,(mask,mass) in enumerate(old):
                take=0 if removed>>i&1 else 1;used+=take
                if mass>take:cells.append((mask,mass-take))
                if take:cells.append((mask|64,1))
            cells.append((64,rank-used))
            assert all(sum(w for mask,w in cells if mask>>j&1)==rank for j in range(7))
            assert any((a|b)==127 for a,w in cells for b,v in cells if w and v)
            for omit in range(7):assert eligible_mass(cells,[j for j in range(7) if j!=omit])>=rank
            total+=1
    print('PASS:',total,'whole-atom removal patterns at three scales; rank=6m, budget=5m-1, every six-row eligible mass at least6m. Partial removals are covered by choosing one surviving point per nonempty atom, as in the hand proof.')


if __name__=='__main__':check()
