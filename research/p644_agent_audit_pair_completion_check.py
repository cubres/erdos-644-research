"""Standard-library exact certificate for the k=20 pair-completion counterexample."""
from itertools import combinations
from collections import Counter
import json

def main():
    code=[x for x in range(32) if bin(x).count('1')%2==0]
    w={x:10 if x==0 else 1 if bin(x).count('1')==2 else 4 for x in code}
    rows=[(i,b) for i in range(5) for b in (0,1)]
    def meets(x,r):return (x>>r[0])&1==r[1]
    pairs=list(combinations(code,2))
    def piercing(chosen):return [(x,y) for x,y in pairs if all(meets(x,r) or meets(y,r) for r in chosen)]
    def Q(chosen):return sum(w[x]*w[y] for x,y in piercing(chosen))
    assert sum(w.values())==40
    assert all(sum(w[x] for x in code if meets(x,r))==20 for r in rows)
    assert all(piercing(chosen) for chosen in combinations(rows,9))
    assert not piercing(rows)
    assert all(any(meets(x,r) for x in (0,15,17)) for r in rows)
    all_min=min(Q(chosen) for chosen in combinations(rows,6))
    paired_values={coords:Q([(i,b) for i in coords for b in (0,1)]) for coords in combinations(range(5),3)}
    assert set(paired_values.values())=={118}
    chosen=[(0,0),(0,1),(1,0),(1,1),(2,1),(3,1)]
    assert Q(chosen)==111 and all_min==111
    counts=Counter(tuple(sorted((bin(x).count('1'),bin(y).count('1')))) for x,y in piercing(chosen))
    assert counts=={(0,4):1,(2,2):3,(2,4):13,(4,4):1}
    out={'status':'PASS','n':40,'k':20,'tau':3,'property':'(9,2)',
         'all_six_minimum_Q':all_min,'every_three_distinct_complement_pairs_Q':118,
         'witness_rows_zero_based':chosen,'checked_six_subsets':210,'checked_nine_subsets':10,
         'scope':'Exact finite check; report also gives parameterized hand proof.'}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
