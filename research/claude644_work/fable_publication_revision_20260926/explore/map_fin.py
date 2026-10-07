import numpy as np, sys
from oracle import triple_static
t = 6/7
def formulas(x,y,z):
    S=x+y+z
    out={}
    def perms(a,b,c): 
        import itertools; return set(itertools.permutations((a,b,c)))
    out['split']=min(max((1+S)/2, 1-a+abs(b-c), 1/3+a) for a,b,c in perms(x,y,z))
    out['asym1']=min(max(S,0.5+b,(1+2*a-b+c)/2,(1+2*a+b+3*c)/3) for a,b,c in perms(x,y,z))
    out['asym2']=min(max(S,1/3+a,1-a+c,(1+2*a+3*b+c)/3) for a,b,c in perms(x,y,z))
    out['four']=min(max(a+b,0.5+a,0.5+b,1+a-b-c,1-a+b-c,1-S/3,(3+S)/5,(1+a+b+2*c)/3,(2+3*c)/4) for a,b,c in perms(x,y,z))
    m,yy,zz=sorted((x,y,z),reverse=True)
    out['sym']=max(1+m-yy-zz,(1+m)/2,(2+m+yy-zz)/3,(3+S)/5)
    return out
M = float(sys.argv[1])
N=10
print('M=',M)
for y in np.linspace(0,M,N+1):
    line=[]
    for z in np.linspace(0,y,N+1)[:]:
        f=formulas(M,y,z); st=triple_static(M,y,z)
        best=min(f.values())
        tag = min(f,key=f.get)[:2] if best<=t+1e-9 else '--'
        line.append('%.3f%s%s'%(st,'s' if st<=t+1e-9 else ' ',tag))
    print('y=%.3f '%y+' '.join(line),flush=True)
