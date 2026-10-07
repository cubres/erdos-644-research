from farkas import *
from lib2 import FUNCS
Q=F(3,4)
names={}
D=[('al>=0',([0,0,1,0],0)),('be-al>=0',([0,0,-1,1],0)),('1-be>=0',([0,0,0,-1],1)),
   ('T1: x-al-3/4>=0',([1,0,-1,0],-Q)),('T2: y+be-7/4>=0',([0,1,0,1],-1-Q)),('T3: x+y+al-be-7/4>=0',([1,1,1,-1],-1-Q)),
   ('fit x-be>=0',([1,0,0,-1],0)),('fit y+al-1>=0',([0,1,1,0],-1))]
def tf(k):
    out=[]
    for u,v in FUNCS[k-1]:
        out.append((f'T{k} part1 {u}s+{v}t<=x',([1,0,-u,-v],0)))
        out.append((f'T{k} part2 {u}(1-s)+{v}(1-t)<=y',([0,1,u,v],-(u+v))))
    return out
def neg(c): return ([-F(a) for a in c[0]],-F(c[1]))
import sys
chain=[int(a) for a in sys.argv[1].split(',')]
cons=list(D)
for k in chain[:-1]:
    fac=tf(k); failing=[]
    for nm,f in fac:
        r=implies([c for _,c in cons],f)
        if r: print(f'  [{nm}] implied by', {cons[i][0]:str(l) for i,l in r[0].items()}, 'slack',r[1])
        else: failing.append((nm,f))
    print(f'Template {k}: facets that can fail:',[n for n,_ in failing])
    if len(failing)!=1: print('NOT A CHAIN'); break
    nm,f=failing[0]
    cons.append(('NOT('+nm+')',neg(f)))   # weak version of strict violation
k=chain[-1]
print('Final template',k)
for nm,f in tf(k):
    r=implies([c for _,c in cons],f)
    print(f'  [{nm}]', 'implied by' if r else 'NOT IMPLIED', r and {cons[i][0]:str(l) for i,l in r[0].items()}, r and r[1])
