"""Exact replay of four-request good-triple witnesses; no optimality claim."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def main():
    data=json.loads((Path(__file__).parent/'logs/astra_static_four.json').read_text())
    pairs=[(0,1),(0,2),(1,2),(0,5),(1,4),(2,3)]
    for C in data:
        assert C['status']=='EXACT_WITNESS'
        x,y,z=map(F,C['triple']);sizes=[x,y,z,1-x-y,1-x-z,1-y-z]
        parts=[{int(k):F(v) for k,v in row.items()} for row in C['parts']]
        assert len(parts)==6
        for row,size in zip(parts,sizes):
            assert size>=0 and sum(row.values())==size
            assert all(0<=k<16 and v>0 for k,v in row.items())
        for a,b in pairs:
            assert all(s&t for s,t in product(parts[a],parts[b]))
        budgets=[sum(v for row in parts for k,v in row.items() if k>>j&1) for j in range(4)]
        assert budgets==list(map(F,C['request_budgets']))
        assert max(budgets)==F(C['budget'])
    print(f'PASS: {len(data)} exact four-request witnesses; includes budget 6/7 at (1/2,1/4,1/4)')


if __name__=='__main__':main()
