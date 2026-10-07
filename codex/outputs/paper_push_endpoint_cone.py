"""Discovery only: tangent-cone endpoint fan-in with one budget-3/4 request.

delta_i>=0, gamma_i>2delta_i/3, sum gamma<sum delta=1;
A=(.5+g0,0,.5-g0), B=(0,.5+g1,.5-g1), C=(0,.5-g2,.5+g2),
U=(.5+v,.5-v-w,w), 0<=w<=delta2. Perturbations are scaled small.
"""
from fractions import Fraction as F
from itertools import product
import sys,json
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3')
from advlazy import Model

PENCIL=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))
def aff(c=0,**terms):
    r=[F(c)]+[F(0)]*8
    for j,v in terms.items():r[int(j)+1]=F(v)
    return tuple(r)
def combine(*terms):return tuple(sum(c*f[j] for c,f in terms)for j in range(9))
ZERO=aff();X=[aff(F(3,4),**{str(i):1}) for i in range(3)]
A=[aff(F(1,2),**{'3':1}),ZERO,aff(F(1,2),**{'3':-1})]
B=[ZERO,aff(F(1,2),**{'4':1}),aff(F(1,2),**{'4':-1})]
C=[ZERO,aff(F(1,2),**{'5':-1}),aff(F(1,2),**{'5':1})]
U=[aff(F(1,2),**{'6':1}),aff(F(1,2),**{'6':-1,'7':-1}),aff(**{'7':1})]
T=[A,B,C,U]

def templates():
    for ass in product(range(3),repeat=6):
        r=ass+(3,);forms=[]
        for i in range(3):
            forms.append(combine(*[(1,T[j][i])for j in r],(-4,X[i])))
            for pp in PENCIL:forms.append(combine(*[(1,T[r[j]][i])for j in pp],(-2,X[i])))
        yield ('F',)+ass,forms
    for d,a,b in product(range(3),repeat=3):
        forms=[]
        for i in range(3):
            forms += [combine((1,T[a][i]),(1,T[b][i]),(1,U[i]),(-2,X[i])),
                      combine((2,T[d][i]),(1,T[b][i]),(1,U[i]),(-2,X[i])),
                      combine((4,T[d][i]),(1,T[a][i]),(1,T[b][i]),(1,U[i]),(-4,X[i]))]
        yield ('V4',d,a,b),forms

def tangent_templates():
    unique={}
    for key,fs in templates():
        if any(f[0]>0 for f in fs):continue
        active=tuple(sorted(set(tuple(f[1:]) for f in fs if f[0]==0 and any(f[1:]))))
        unique.setdefault(active,key)
    return [(key,fs)for fs,key in unique.items()]

if __name__=='__main__':
    m=Model();vs=[m.var(0,1)for _ in range(6)]+[m.var(-10,10),m.var(0,1)]
    m.add({i:1 for i in range(3)},lo=1,hi=1)
    eps=.00001
    for i in range(3):m.add({i:-2/3,i+3:1},lo=eps)
    m.add({i:1 for i in range(3,6)},hi=1-eps)
    m.add({7:1,2:-1},hi=0)
    ts=tangent_templates();seen=set();print('distinct tangent templates',len(ts),flush=True)
    for it in range(100):
        r=m.solve(20)
        if r.x is None:print('STATUS',r.status,r.message,flush=True);break
        new=[(key,fs)for key,fs in ts if key not in seen and all(sum(float(c)*r.x[i]for i,c in enumerate(f))<=1e-8 for f in fs)]
        print('ITER',it,'new',len(new),'added',len(seen),'point',r.x[:8].tolist(),flush=True)
        if not new:
            print('TANGENT_SURVIVOR',r.x[:8].tolist(),flush=True);break
        for key,fs in new:
            seen.add(key);bs=[m.var(0,1,integer=True)for _ in fs];m.add({b:1 for b in bs},lo=1)
            for z,f in zip(bs,fs):
                row={i:float(c)for i,c in enumerate(f)if c};row[z]=-100
                m.add(row,lo=-100+eps)
    data={'templates':[{'key':k,'facets':fs}for k,fs in ts if k in seen]}
    with open('outputs/paper_push_endpoint_cone.json','w')as f:json.dump(data,f,default=str,indent=2)
