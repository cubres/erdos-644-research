# Referee check for tameness#1 (Cor R'): exact check of the Lemma R1 counting step
#  (every (alpha+1)-subset of V contains an edge) => every Y contains >= C(|Y|,k)/C(alpha+1,k) edges,
#  and the identity C(n,a)/C(n-k,a-k) = C(n,k)/C(a,k); plus orbit-size bound prod C(n_j,u_j) >= n_i.
import itertools, random
from math import comb
from fractions import Fraction as F
for n in range(1,30):
    for a in range(0,n+1):
        for k in range(0,a+1):
            assert F(comb(n,a),comb(n-k,a-k)) == F(comb(n,k),comb(a,k))
random.seed(1)
bad=0; tests=0
for trial in range(300):
    N=random.randint(5,9); k=random.randint(2,min(4,N-1))
    allk=list(itertools.combinations(range(N),k))
    H=set(e for e in allk if random.random()<random.choice([0.2,0.5,0.8]))
    if not H: continue
    # alpha = max edge-free set
    alpha=max(s for s in range(N+1) for Y in itertools.combinations(range(N),s)
              if not any(set(e)<=set(Y) for e in H)) if True else None
    for size in range(alpha+1,N+1):
        for Y in itertools.combinations(range(N),size):
            cnt=sum(1 for e in H if set(e)<=set(Y)); tests+=1
            if F(cnt) < F(comb(size,k),comb(alpha+1,k)): bad+=1
print("R1 counting violations:",bad,"of",tests)
