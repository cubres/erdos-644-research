"""Exact checks of the explicit shift and non-Fano obstruction examples."""
from itertools import combinations,product
from pathlib import Path
import json


def main():
    rows=[('0135','24'),('0146','23'),('0234','16'),('0236','45'),
          ('0256','13'),('1234','05'),('1245','36'),('1256','04'),('3456','01')]
    H={frozenset(map(int,e)) for e,p in rows};V=frozenset(range(7))
    for e,p in rows:
        E=frozenset(map(int,e));P=frozenset(map(int,p))
        assert not E&P and all(P&F for F in H if F!=E)
    assert all(E&F for E,F in combinations(H,2))
    assert all(any(not frozenset(P)&E for E in H) for P in combinations(V,2))
    assert all({0,1,3}&E for E in H)
    shifted={((E-{1})|{0}) if 1 in E and 0 not in E and ((E-{1})|{0}) not in H else E for E in H}
    assert shifted==(H-{frozenset([1,2,4,5])})|{frozenset([0,2,4,5])}
    bad=[frozenset(map(int,e)) for e in ['0135','0146','0236','0245','1234','1256','3456']]
    assert set(bad)<=shifted
    assert all(sum(not frozenset(P)&E for E in bad)==1 for P in combinations(V,2))
    print('PASS: nine-edge intersecting shift obstruction; every proper subfamily is 2-pierceable; shifted Fano pair-cover checked')
    data=json.loads((Path(__file__).parent/'logs/astra_nonfano_two_type.json').read_text())
    cells=[]
    for cell,masses in data['cells']:
        assert all(x==int(x) and x>=0 for x in masses)
        cells.append((frozenset(cell),list(map(int,masses))))
    assert all(A|B!=V for (A,a),(B,b) in product(cells,repeat=2))
    assert all(sum(m[i] for C,m in cells)<=cap for i,cap in enumerate([40,139,99]))
    for j in range(7):
        counts=[sum(m[i] for C,m in cells if j in C) for i in range(3)]
        assert counts in [[20,0,80],[0,80,20]]
    print('PASS: explicit integer bad tuple for the intersecting non-Fano two-type family')


if __name__=='__main__':main()
