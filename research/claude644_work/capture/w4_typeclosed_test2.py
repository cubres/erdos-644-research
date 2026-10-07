# sanity: covering clauses <=> tau* > T  for random grid type sets; and 7.79 pair-freeness via pair_matrix
import random, numpy as np
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, load_cap42
from w4_typeclosed_search import grid_types, residual_boxes
from w4_typeclosed_search2 import pair_matrix
rng=random.Random(5)
for trial in range(300):
    D=rng.choice([8,10,12]); p=3
    X=[rng.randint(D//3,D) for _ in range(p)]
    if sum(X)<D+2: continue
    G=grid_types(D,X)
    A=rng.sample(G,min(len(G),rng.randint(1,12)))
    T=rng.randint(0,sum(X))
    boxes=residual_boxes(X,T)
    cov=all(any(all(a[i]<=u[i] for i in range(p)) for a in A) for u in boxes)
    ts=tau_star(A,X)
    assert cov==(ts>T),(D,X,A,T,ts,cov)
print('covering<=>tau*>T verified on random instances')
T79=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
T640=[tuple(8*v for v in t) for t in T79]
bad=pair_matrix(T640,[513]*3,load_cap42())
print('7.79 pair-bad entries:',int(bad.sum()), ' tau*=',tau_star(T640,[513]*3))
