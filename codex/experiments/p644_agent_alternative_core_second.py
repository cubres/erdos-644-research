"""One bounded next response to the exact four-cut state in report section 12.

All original units are 1/200. The new cut and its complement are actual.
Retain all maximum-imbalance inequalities, all four global pair gaps, all
120 seven-row conditions, and check maximum-imbalance lexicography.

The relative-interior LP exposes every feasible point-type orientation in a
fixed overlap mode, so its support is sufficient to test existence of all
seven-row conditions in that mode. Numerical LP is discovery only; exact
positive responses are rechecked with Fraction in inspect().
"""
from itertools import combinations, product
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
import json

OLD_W=[89,11,11,89,25,75,75,25]
OLD_G=[11,0,0,75,0,75,39,0]
OLD_TYPES=list(product((0,1),repeat=3))
TYPES=[];W=[]
for z,w,g in zip(OLD_TYPES,OLD_W,OLD_G):
    for bit,mass in [(0,w-g),(1,g)]:
        if mass:TYPES.append(z+(bit,));W.append(mass)
W=np.array(W,float);N=len(W)
ROWS=np.array(TYPES,float).T
PAIRS=list(combinations(range(4),2))
EQUAL=np.array([[int(z[i]==z[j]) for z in TYPES] for i,j in PAIRS],float)
OVERLAPS=EQUAL@W/2
SUB7=list(combinations(range(10),7))
MASK7=[sum(1<<j for j in inds) for inds in SUB7]


def all7(g,tol=1e-7):
    support=[]
    for z,w,x in zip(TYPES,W,g):
        for bit,mass in [(0,w-x),(1,x)]:
            if mass>tol:
                q=z+(bit,)
                support.append(sum(1<<(2*j+b) for j,b in enumerate(q)))
    unions={x|y for x,y in combinations(support,2)}
    bad=[list(s) for s,m in zip(SUB7,MASK7) if not any((p&m)==m for p in unions)]
    return bad


def relative_interior(A,b,eq,rhs):
    """Repeated strict-feasibility LP; dual support removes forced equalities."""
    active=np.ones(len(b))
    for _ in range(len(b)+1):
        r=linprog(np.r_[np.zeros(N),-1],A_ub=np.c_[A,active],b_ub=b,
                  A_eq=np.c_[eq,np.zeros(len(rhs))],b_eq=rhs,
                  bounds=[(None,None)]*N+[(0,1)],method='highs')
        if not r.success:return None
        if r.x[-1]>1e-7 or not any(active):return r.x[:N]
        forced=(active>0)&(r.ineqlin.marginals < -1e-8)
        if not any(forced):
            raise RuntimeError('No forced constraint extracted from zero strict slack')
        active[forced]=0
    raise RuntimeError('Relative interior iteration exhausted')


def lex(g,tol=1e-5):
    ov=ROWS@g;imbal=abs(EQUAL@g-OVERLAPS)
    energy=np.array([(OVERLAPS[p]-100)**2+(ov[i]-100)**2+(ov[j]-100)**2
                     for p,(i,j) in enumerate(PAIRS)])
    bad=[p for p in range(6) if imbal[p]>=64-tol and energy[p]<196-tol]
    return bad,imbal,energy,ov


def response(u):
    u=np.clip(np.array(u,float),0,W)
    bands=[(0,64),(86,114),(136,200)]
    lower=ROWS@u;upper=np.minimum(ROWS@W,lower+200-sum(u))
    choices=[[j for j,(lo,hi) in enumerate(bands)
              if lo<=upper[i]+1e-8 and hi>=lower[i]-1e-8] for i in range(4)]
    status={'modes':0,'infeasible':0,'bad7':0,'lex_unresolved':0}
    for modes in product(*choices):
        status['modes']+=1
        lo=[bands[j][0] for j in modes];hi=[bands[j][1] for j in modes]
        A=np.r_[np.eye(N),-np.eye(N),EQUAL,-EQUAL,ROWS,-ROWS]
        b=np.r_[W,-u,OVERLAPS+64,64-OVERLAPS,hi,-np.array(lo)]
        g=relative_interior(A,b,np.array([np.ones(N)]),np.array([200]))
        if g is None:status['infeasible']+=1;continue
        bad=all7(g)
        if bad:status['bad7']+=1;continue
        bl,im,en,ov=lex(g)
        if bl:
            # We do not declare the mode infeasible: a boundary point could
            # have larger variance. This branch requires further analysis.
            status['lex_unresolved']+=1;continue
        return {'status':'HAS_RESPONSE','u':u.tolist(),'g':g.tolist(),'mode':modes,
                'imbalances':im.tolist(),'energies':en.tolist(),'overlaps':ov.tolist(),
                'counts':status}
    return {'status':'UNRESOLVED' if status['lex_unresolved'] else 'NO_RESPONSE_NUMERICAL',
            'u':u.tolist(),'counts':status}


def inspect(u,g):
    u=[F(x) for x in u];g=[F(x) for x in g]
    assert sum(g)==200 and sum(u)<=150
    assert all(0<=a<=x<=int(w) for a,x,w in zip(u,g,W))
    ov=[sum(x for x,z in zip(g,TYPES) if z[i]) for i in range(4)]
    assert all(x<=64 or 86<=x<=114 or x>=136 for x in ov)
    for p,(i,j) in enumerate(PAIRS):
        a=F(int(OVERLAPS[p]));s=abs(sum(x for x,z in zip(g,TYPES) if z[i]==z[j])-a)
        assert s<=64
        e=(a-100)**2+(ov[i]-100)**2+(ov[j]-100)**2
        assert s<64 or e>=196
    support=[];points=[]
    for z,w,x in zip(TYPES,W,g):
        for bit,mass in [(0,F(int(w))-x),(1,x)]:
            if mass>0:
                full=z+(bit,)
                support.append(sum(1<<(2*j+b) for j,b in enumerate(full)))
                points.append((full,mass))
    pair_overlap={(i,j):sum(m for z,m in points if z[i] and z[j])
                  for i,j in combinations(range(5),2)}
    assert all(x<=64 or 86<=x<=114 or x>=136 for x in pair_overlap.values())
    all_triples=[]
    for triple in combinations(range(5),3):
        zero=sum(m for z,m in points if all(z[i]==0 for i in triple))
        one=sum(m for z,m in points if all(z[i]==1 for i in triple))
        s=abs(zero-one)
        energy=sum((pair_overlap[p]-100)**2 for p in combinations(triple,2))
        assert s<=64 and (s<64 or energy>=196)
        all_triples.append({'cuts':triple,'imbalance':str(s),'energy':str(energy)})
    unions={x|y for x,y in combinations(support,2)}
    assert all(any((p&m)==m for p in unions) for m in MASK7)
    return {'verified':'EXACT_FRACTION','types':[''.join(map(str,z)) for z in TYPES],
            'u':[str(x) for x in u],'g':[str(x) for x in g],
            'overlaps':[str(x) for x in ov],'seven_subfamilies':len(MASK7),
            'all_triples':all_triples,'all_ten_two_pierceable':1023 in unions}


def menu(limit=24):
    # Endpoint components of all eight old rows, then several whole-cell
    # orders and their reversals. Exactly one partial cell per request.
    orders=[]
    sizes=list(range(N))
    orders.extend([sizes,sizes[::-1],sorted(sizes,key=lambda i:W[i]),
                   sorted(sizes,key=lambda i:-W[i])])
    for i in range(4):
        orders.append(sorted(sizes,key=lambda j:(TYPES[j][i],j)))
        orders.append(sorted(sizes,key=lambda j:(-TYPES[j][i],j)))
    rng=np.random.default_rng(12644)
    orders.extend(rng.permutation(N).tolist() for _ in range(limit))
    seen=set()
    for order in orders:
        u=np.zeros(N);remaining=150
        for j in order:
            u[j]=min(W[j],remaining);remaining-=u[j]
            if remaining==0:break
        key=tuple(u)
        if key not in seen:
            seen.add(key);yield u
            if len(seen)>=limit:return


def component_menu():
    index={t:i for i,t in enumerate(TYPES)}
    components=[]
    for t,i in index.items():
        opposite=tuple(1-b for b in t)
        if opposite in index and i<index[opposite]:
            components.append([i,index[opposite]])
    for first,second in combinations(components,2):
        inds=first+second
        if sum(W[j] for j in inds)>150:continue
        u=np.zeros(N)
        for j in inds:u[j]=W[j]
        remaining=150-sum(u)
        for j in sorted(range(N),key=lambda j:(''.join(map(str,TYPES[j]))!='0110',j)):
            take=min(W[j]-u[j],remaining);u[j]+=take;remaining-=take
            if remaining==0:break
        yield u


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--components',action='store_true')
    args=p.parse_args()
    for count,u in enumerate(component_menu() if args.components else menu(),1):
        r=response(u)
        if r['status']=='HAS_RESPONSE':
            fr=[F(float(x)).limit_denominator(1000000) for x in r['g']]
            try:r['exact']=inspect([F(int(x)) for x in u],fr)
            except AssertionError:r['exact']='ROUNDING_FAILED'
        print(json.dumps({'request':count,**r}),flush=True)
