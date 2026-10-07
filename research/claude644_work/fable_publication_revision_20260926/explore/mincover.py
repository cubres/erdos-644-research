import numpy as np, itertools, sys
from lemmas import *
t=6/7; A=3/7; B=10/21; C=5/14; D=4/21; L=D
def closers(x,y,z,stage):
    out=set()
    for k,f in [('split',split),('asym1',asym1),('asym2',asym2),('four',four),('sym',sym),('s0',s0)]:
        if f(x,y,z)<=t+1e-9: out.add(k)
    if stage=='s2':
        if g0(x,y,z,A,B)<=t+1e-9: out.add('g0')
        if g1(x,y,z,A,B,t): out.add('g1')
        if g2(x,y,z,A,B,t): out.add('g2')
    if stage=='s3':
        if g0(x,y,z,L,C)<=t+1e-9: out.add('g0')
        if g1(x,y,z,L,C,t): out.add('g1')
        if g2(x,y,z,L,C,t): out.add('g2')
    if stage=='fin':
        M=max(x,y,z)
        if g0(x,y,z,M,0.5)<=t+1e-9: out.add('g0')
        if g1(x,y,z,M,0.5,t): out.add('g1')
        if g2(x,y,z,M,0.5,t): out.add('g2')
        if nc(x,y,z,M,t): out.add('nc')
    return out
def points(stage,N=24):
    if stage=='s1': xs=np.linspace(A+1e-7,B,N); ym=lambda x:C
    if stage=='s2': xs=np.linspace(D,C,N); ym=lambda x:A
    if stage=='s3': xs=np.linspace(B+1e-7,0.5,N); ym=lambda x:L-1e-7
    if stage=='fin': xs=np.linspace(0.05,A,N); ym=lambda x:x
    for x in xs:
        for y in np.linspace(0,ym(x),N):
            for z in np.linspace(0,y,N):
                yield (x,y,z)
if __name__=="__main__":
  stage=sys.argv[1]
  pts=list(points(stage))
  cl=[closers(*p,stage) for p in pts]
  bad=[p for p,c in zip(pts,cl) if not c]
  print(stage,'points',len(pts),'uncovered',len(bad), bad[:5])
  names=sorted(set().union(*cl))
  for r in range(1,5):
      found=[]
      for sub in itertools.combinations(names,r):
          s=set(sub)
          if all((c & s) for c in cl if c): found.append(sub)
      if found:
          print('min size',r,found[:15]); break
