"""One focused endpoint-union request on the exact ten-row sample.

Loads component-request certificate 3. The next cut contains all endpoints
of the old ten-row piercing graph, equivalently its actual complement
avoids that 73/200-set. No additional request menu is searched.
"""
from itertools import combinations,product
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def load_state():
    row=json.loads(Path('outputs/agent_core_second_components.jsonl').read_text().splitlines()[2])
    oldw=[78,11,11,11,14,75,25,75,36,39,25]
    atoms={}
    for t,w,g in zip(row['exact']['types'],oldw,map(F,row['exact']['g'])):
        if w-g:atoms[tuple(map(int,t+'0'))]=F(w)-g
        if g:atoms[tuple(map(int,t+'1'))]=g
    types=sorted(atoms);w=[atoms[t] for t in types]
    u=[atoms[t] if tuple(1-b for b in t) in atoms else F(0) for t in types]
    return types,w,u


def masks(types):
    return [sum(1<<(2*j+b) for j,b in enumerate(t)) for t in types]


def min_p6(types,masses):
    pm=masks(types);minimum=None;minrows=None
    q=2*len(types[0])
    for inds in combinations(range(q),6):
        wanted=sum(1<<i for i in inds);ends=set()
        for i,j in combinations(range(len(types)),2):
            if ((pm[i]|pm[j])&wanted)==wanted:ends.update([i,j])
        total=sum(masses[i] for i in ends)
        if minimum is None or total<minimum:minimum=total;minrows=inds
    return minimum,minrows


def check7(types,w,g,exact=False):
    support=[]
    for t,m,x in zip(types,w,g):
        for bit,mass in [(0,m-x),(1,x)]:
            if mass>(0 if exact else 1e-6):support.append(t+(bit,))
    pm=masks(support);unions={a|b for a,b in combinations(pm,2)}
    q=2*(len(types[0])+1)
    for subset in combinations(range(q),7):
        wanted=sum(1<<j for j in subset)
        if not any((z&wanted)==wanted for z in unions):return list(subset)
    return None


def interior(A,b,n):
    active=np.ones(len(b))
    for _ in range(len(b)+1):
        r=linprog(np.r_[np.zeros(n),-1],A_ub=np.c_[A,active],b_ub=b,
                  A_eq=[np.r_[np.ones(n),0]],b_eq=[200],
                  bounds=[(None,None)]*n+[(0,1)],method='highs')
        if not r.success:return None
        if r.x[-1]>1e-7 or not any(active):return r.x[:n]
        forced=(active>0)&(r.ineqlin.marginals < -1e-8)
        if not any(forced):raise RuntimeError('Zero strict slack without forced rows')
        active[forced]=0
    raise RuntimeError('Interior iteration failed')


def exact_check(types,w,u,g):
    assert sum(g)==200 and sum(u)==73
    assert all(0<=a<=x<=m for a,x,m in zip(u,g,w))
    pts=[]
    for t,m,x in zip(types,w,g):
        for bit,mass in [(0,m-x),(1,x)]:
            if mass:pts.append((t+(bit,),mass))
    q=6
    pair={(i,j):sum(m for t,m in pts if t[i] and t[j]) for i,j in combinations(range(q),2)}
    assert all(x<=64 or 86<=x<=114 or x>=136 for x in pair.values())
    triples=[]
    for tri in combinations(range(q),3):
        s=abs(sum(m for t,m in pts if all(t[i]==0 for i in tri))-
              sum(m for t,m in pts if all(t[i]==1 for i in tri)))
        e=sum((pair[p]-100)**2 for p in combinations(tri,2))
        assert s<=64 and (s<64 or e>=196)
        triples.append({'cuts':tri,'s':str(s),'energy':str(e)})
    assert check7(types,w,g,True) is None
    # A six-row endpoint union is always a global transversal in a (7,2) family.
    minp,minrows=min_p6([t for t,m in pts],[m for t,m in pts])
    return {'verified':'EXACT_FRACTION','types':[''.join(map(str,t)) for t in types],
            'w':[str(x) for x in w],'u':[str(x) for x in u],'g':[str(x) for x in g],
            'triples':triples,'seven_subfamilies':792,'min_p6':str(minp),'min_p6_rows':minrows}


def run():
    types,fw,fu=load_state();w=np.array(list(map(float,fw)));u=np.array(list(map(float,fu)))
    oldmin,oldrows=min_p6(types,fw)
    n=len(w);q=len(types[0]);rows=np.array(types,float).T
    pairs=list(combinations(range(q),2))
    eq=np.array([[int(t[i]==t[j]) for t in types] for i,j in pairs],float)
    ov=eq@w/2
    bands=[(0,64),(86,114),(136,200)]
    lower=rows@u;upper=np.minimum(rows@w,lower+200-sum(u))
    choices=[[j for j,(lo,hi) in enumerate(bands) if lo<=upper[i]+1e-8 and hi>=lower[i]-1e-8]
             for i in range(q)]
    counts={'modes':0,'infeasible':0,'bad7':0,'lex_unresolved':0};fail7=[]
    for mode in product(*choices):
        counts['modes']+=1
        lo=[bands[j][0] for j in mode];hi=[bands[j][1] for j in mode]
        A=np.r_[np.eye(n),-np.eye(n),eq,-eq,rows,-rows]
        b=np.r_[w,-u,ov+64,64-ov,hi,-np.array(lo)]
        g=interior(A,b,n)
        if g is None:counts['infeasible']+=1;continue
        bad=check7(types,w,g)
        if bad:counts['bad7']+=1;fail7.append({'mode':mode,'rows':bad});continue
        newov=rows@g;ss=abs(eq@g-ov)
        ee=np.array([(ov[p]-100)**2+(newov[i]-100)**2+(newov[j]-100)**2
                     for p,(i,j) in enumerate(pairs)])
        if any(ss[p]>=64-1e-6 and ee[p]<196-1e-5 for p in range(len(pairs))):
            counts['lex_unresolved']+=1;continue
        fr=[F(float(x)).limit_denominator(1000000) for x in g]
        try:certificate=exact_check(types,fw,fu,fr)
        except AssertionError:certificate='ROUNDING_FAILED'
        return {'status':'HAS_RESPONSE','mode':mode,'counts':counts,
                'old_min_p6':str(oldmin),'old_min_p6_rows':oldrows,'exact':certificate}
    return {'status':'UNRESOLVED' if counts['lex_unresolved'] else 'NO_RESPONSE_NUMERICAL',
            'counts':counts,'bad7_modes':fail7}


if __name__=='__main__':
    print(json.dumps(run()),flush=True)
