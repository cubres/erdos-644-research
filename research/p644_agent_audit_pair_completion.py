"""Exact integer probes for unrestricted versus paired six-row Q.
The even-parity code has support-level (7,2); positive weights preserve it.
Numerical search uses integers, and every reported Q is independently recomputed.
"""
from itertools import combinations
import argparse,json,random,time
import numpy as np


def setup(d=5):
    points=[v for v in range(1<<d) if bin(v).count('1')%2==0]
    rowsets=[{j for j,v in enumerate(points) if ((v>>i)&1)==b} for i in range(d) for b in range(2)]
    pps=list(combinations(range(len(points)),2))
    tuples=[];coeff=[];paired=[]
    for rows in combinations(range(2*d),6):
        common=set(range(len(points)))
        for r in rows:common &= rowsets[r]
        if common:continue
        tuples.append(rows)
        coeff.append([int(all(a in rowsets[r] or b in rowsets[r] for r in rows)) for a,b in pps])
        paired.append(all((r^1) in rows for r in rows))
    return points,rowsets,pps,tuples,np.array(coeff,dtype=np.int64),np.array(paired,dtype=bool)


def exact_report(w,data):
    points,rows,pps,tuples,co,paired=data
    products=np.array([w[a]*w[b] for a,b in pps],dtype=np.int64)
    q=co@products;allidx=int(np.argmin(q));pairindices=np.nonzero(paired)[0]
    pi=int(pairindices[np.argmin(q[paired])])
    assert all(sum(w[j] for j in row)==sum(w)//2 for row in rows)
    assert all(wi>0 for wi in w)
    def direct(idx):
        chosen=tuples[idx]
        return sum(w[a]*w[b] for a,b in pps if all(a in rows[r] or b in rows[r] for r in chosen))
    assert direct(allidx)==q[allidx] and direct(pi)==q[pi]
    return {'weights':w,'n':sum(w),'k':sum(w)//2,'minimum_all_Q':int(q[allidx]),
            'minimum_paired_Q':int(q[pi]),'minimizing_all_rows':tuples[allidx],
            'minimizing_paired_rows':tuples[pi], 'strict_counterexample':bool(q[allidx]<q[pi])}


def run(samples=10000,seed=644):
    start=time.time();rng=random.Random(seed);data=setup();points=data[0]
    characters=np.array([[1 if (((v>>i)^(v>>j))&1)==0 else -1 for v in points] for i,j in combinations(range(5),2)],dtype=np.int64)
    initial=exact_report([1]*16,data);best=initial
    # These characters have zero total and zero sum on every coordinate half.
    for it in range(samples):
        coefficients=np.array([rng.randint(-10,10) for _ in range(10)],dtype=np.int64)
        perturb=coefficients@characters
        w=(perturb+1-int(np.min(perturb))).tolist()
        candidate=exact_report(w,data)
        if candidate['strict_counterexample']:
            return {'support':'even parity on five coordinates','uniform':initial,'counterexample':candidate,
                    'iteration':it,'elapsed_seconds':time.time()-start,'seed':seed}
    return {'support':'even parity on five coordinates','uniform':initial,'samples':samples,
            'found_counterexample':False,'elapsed_seconds':time.time()-start,'seed':seed}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--samples',type=int,default=10000);a=p.parse_args()
    print(json.dumps(run(a.samples),indent=2))
