# Independent brute-force check of the counterexample to the partner-pair corollary WITHOUT its side condition.
from itertools import combinations
H=[{0,1,2,3},{0,2,6,9},{0,3,9,10},{2,3,4,5},{2,4,6,8},{3,4,8,10},{6,7,8,9},{8,9,10,11}]
V=sorted(set().union(*H)); k=max(map(len,H))
def pierce(F,P): return all(E & P for E in F)
tau=next(s for s in range(len(V)+1) if any(pierce(H,set(c)) for c in combinations(V,s)))
is72=all(any(pierce(F,{x,y}) for x in V for y in V) for r in range(1,8) for F in combinations(H,r))
E1,F1,E2,F2={0,1,2,3},{2,3,4,5},{6,7,8,9},{8,9,10,11}
t=tau
partner=all(len(E&F)<=len(E)-t+1 for E,F in ((E1,F1),(E2,F2)))
cross=len(E1&E2)+len(F1&F2)+len(E1&F2)+len(F1&E2)
print('rank',k,'tau',tau,'(7,2):',is72,'partner pairs:',partner,'cross-overlap',cross,'claimed >=',2*t-k-1,
      '| side condition 2(k-t+1)<=t-1:',2*(k-t+1)<=t-1)
# Lemma Q hypotheses on this quadruple
I5=(E1&F1)|(E2&F2); I6=(E1&E2)|(F1&F2); I7=(E1&F2)|(F1&E2)
print('|I5|,|I6|,|I7| =',len(I5),len(I6),len(I7),' t-1 =',t-1,' 2t-k-2 =',2*t-k-2)
# S-bound corollary check on all 4-multisets
from itertools import combinations_with_replacement as cwr
Smin=min(sum(len(G[i]&G[j]) for i,j in combinations(range(4),2)) for G in cwr(H,4))
print('S_min',Smin,' stated bound',min(t,(3*(2*t-k-2))//2+1),' sharpened',min(t,-((-3*(2*t-k-1))//2)))
# edge-criticality: tau(H - E) for each E
for i,E in enumerate(H):
    G=H[:i]+H[i+1:]
    print('tau(H -',sorted(E),') =',next(s for s in range(len(V)+1) if any(pierce(G,set(c)) for c in combinations(V,s))))
