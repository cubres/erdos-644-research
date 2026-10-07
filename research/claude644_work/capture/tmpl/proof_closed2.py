# exact chain certificates for closed two-part sets, vars (x,y,l,a,b,c)
import sys
from farkas import implies
from fractions import Fraction as F
from lib2 import FUNCS
X,Y,L,A,B,C=range(6); NM=['x','y','l','a','b','c']
def lin(d,const=0):
    v=[F(0)]*6
    for k,c in d.items(): v[k]=F(c)
    return (v,F(const))
Q=F(3,4)
def domain(l0,c1):
    D=[('l>=0',lin({L:1})),('a>=l',lin({A:1,L:-1})),('b>=a',lin({B:1,A:-1})),('c>=b',lin({C:1,B:-1})),('c<=1',lin({C:-1},1)),
       ('fit x>=c',lin({X:1,C:-1})),('fit y>=1-l',lin({Y:1,L:1},-1))]
    D+= [('l=0',lin({L:-1}))] if l0 else [('Tl: x-l>=3/4',lin({X:1,L:-1},-Q))]
    D+= [('c=1',lin({C:1},-1))] if c1 else [('Tc: y-1+c>=3/4',lin({Y:1,C:1},-1-Q))]
    D+= [('Tgap: N-1-(b-a)>=3/4',lin({X:1,Y:1,A:1,B:-1},-1-Q)),
         ('H: 7-4y-7a>0',lin({A:-7,Y:-4},7)),('H: 7b-4x>0',lin({B:7,X:-4})),
         ('G: N-7/4-(b-a)>0',lin({X:1,Y:1,B:-1,A:1},-F(7,4))),('G2: 2N-7/2-(c-l)>0',lin({X:2,Y:2,C:-1,L:1},-F(7,2)))]
    return D
def facets(k,s,t):
    out=[]
    for u,v in FUNCS[k-1]:
        d1={X:1}; d1[s]=d1.get(s,0)-u; d1[t]=d1.get(t,0)-v
        out.append((f'M{k}({NM[s]},{NM[t]}) part1 {u}{NM[s]}+{v}{NM[t]}<=x',lin(d1)))
        d2={Y:1}; d2[s]=d2.get(s,0)+u; d2[t]=d2.get(t,0)+v
        out.append((f'M{k}({NM[s]},{NM[t]}) part2 {u}(1-{NM[s]})+{v}(1-{NM[t]})<=y',lin(d2,-(u+v))))
    return out
def neg(c): return ([-a for a in c[0]],-c[1])
def run(l0,c1,chain):
    cons=domain(l0,c1)
    print(f'=== case l=0:{l0} c=1:{c1} chain {chain}')
    for (k,s,t) in chain[:-1]:
        fl=[]
        for nm,f in facets(k,s,t):
            r=implies([c for _,c in cons],f)
            if r: print(f'   holds: [{nm}] =', ' + '.join(f'{l}*[{cons[i][0]}]' for i,l in r[0].items()), f'+ {r[1]}')
            else: fl.append((nm,f))
        print(f' {k,NM[s],NM[t]} can fail only at:',[n for n,_ in fl])
        assert len(fl)==1
        cons.append(('NOT '+fl[0][0],neg(fl[0][1])))
    k,s,t=chain[-1]
    allok=True
    for nm,f in facets(k,s,t):
        r=implies([c for _,c in cons],f)
        if r: print(f'   FINAL holds: [{nm}] =', ' + '.join(f'{l}*[{cons[i][0]}]' for i,l in r[0].items()), f'+ {r[1]}')
        else: print('   FINAL NOT IMPLIED',nm); allok=False
    print(' RESULT', 'PROVED' if allok else 'FAILED')
if __name__=='__main__':
    run(False,False,[(21,A,B),(21,B,A),(9,B,A),(39,A,B)])
    run(True,True,[(21,A,B),(21,B,A)])
