"""first-request search with branch-aware adversary (evaluate2). args: x y z t lo hi n"""
import sys, random
from multiprocessing import Pool
from adaptive import evaluate2
from oracle import triple_sizes
x,y,z,t=map(float,sys.argv[1:5]); lo=float(sys.argv[5]); hi=float(sys.argv[6]); n=int(sys.argv[7])
if lo<0: lo=hi=None
s=triple_sizes(x,y,z)
def rand_d(rng):
    while True:
        pr=[rng.random() for _ in range(6)]
        for i in range(3):
            if rng.random()<0.6: pr[i]+=3
        order=sorted(range(6),key=lambda i:-pr[i])
        d=[0]*6; rem=t
        for i in order:
            frac=1 if rng.random()<0.6 else rng.random()
            amt=min(s[i]*frac,rem); d[i]=amt; rem-=amt
        for i in order:
            a=min(s[i]-d[i],rem); d[i]+=a; rem-=a
        if rem<1e-9: return d
def job(seed):
    rng=random.Random(seed); d=rand_d(rng)
    v,h,br=evaluate2(x,y,z,d,t,lo=lo,hi=hi,nobj=12,climb=12,seed=seed,stop_above=t+0.01)
    return (v,d,h,br)
if __name__=='__main__':
    with Pool(10) as p: res=p.map(job,range(n))
    res.sort(key=lambda r:r[0])
    for v,d,h,br in res[:6]:
        print('%.4f'%v,[round(a,3) for a in d],[round(a,3) for a in h],br)
