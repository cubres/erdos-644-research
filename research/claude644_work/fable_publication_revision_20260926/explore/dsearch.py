"""random + local search over first requests d for a given triple (discovery)."""
import sys, random, json, time
from multiprocessing import Pool
from adaptive import evaluate
from oracle import triple_sizes
t = float(sys.argv[4]) if len(sys.argv)>4 else 6/7
x,y,z = map(float, sys.argv[1:4])
s = triple_sizes(x,y,z)
import os
GL, GH = (float(v) for v in os.environ.get('GAP','1,1').split(','))
def GAP(a,b,c):
    return all(not (GL < u <= GH) for u in (a,b,c))
def rand_d(rng):
    while True:
        w = [rng.random()**2 for _ in range(6)]
        # bias: pair cells often fully avoided
        for i in range(3):
            if rng.random()<0.5: w[i] = 10
        d = [0]*6; rem = t
        order = sorted(range(6), key=lambda i: -w[i]*rng.random())
        for i in order:
            amt = min(s[i], rem*min(1, w[i]/sum(w)*3)); d[i]=amt; rem-=amt
        for i in order:
            add=min(s[i]-d[i],rem); d[i]+=add; rem-=add
        if rem < 1e-9: return d
def job(seed):
    rng = random.Random(seed)
    d = rand_d(rng)
    v,h = evaluate(x,y,z,d,t,gap=GAP,nrand=25,climb=15,seed=seed)
    return (v,d,h)
if __name__=='__main__':
    n = int(sys.argv[5]) if len(sys.argv)>5 else 60
    with Pool(10) as p:
        res = p.map(job, range(n))
    res.sort(key=lambda r:r[0])
    for v,d,h in res[:8]:
        print('%.4f'%v, [round(a,3) for a in d], [round(a,3) for a in h])
