"""Independent dominance check by angular breakpoints, not polygon facets."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


def below(first,second):
    points={F(0),F(1)}
    for (a,b),(c,d) in combinations(second,2):
        denominator=a-b-c+d
        if denominator:
            t=(d-b)/denominator
            if 0<t<1:points.add(t)
    def value(poly,t):return max(a*t+b*(1-t) for a,b in poly)
    return all(value(first,t)<=value(second,t) for t in points)


def main():
    base=Path(__file__).parent;data=json.loads((base/'logs/astra_support_capacity_minimal.json').read_text())
    minimal=[[tuple(map(F,p)) for p in row['vertices']] for row in data['minimal_functions']]
    assert len(minimal)==42 and data['total_assignments']==54214 and data['distinct_functions']==11865
    assert all(not below(a,b) for i,a in enumerate(minimal) for j,b in enumerate(minimal) if i!=j)
    assert len(data['dominators'])==11865
    for key,index in data['dominators'].items():
        poly=[tuple(map(F,p.split(','))) for p in key.split(';')]
        assert 0<=index<len(minimal) and below(minimal[index],poly)
    print('PASS: 11865 exact dominations and pairwise incomparability of the 42 retained functions, using angular breakpoints.')


if __name__=='__main__':main()
