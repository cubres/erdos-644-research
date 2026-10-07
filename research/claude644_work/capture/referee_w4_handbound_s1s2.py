# Referee (independent) exact checks of S1, S2 templates and the S1 continuous closed form.
import itertools
from fractions import Fraction as F

def cells(r,x,y,z):
    # r-uniform good triple E,F,G with E&F&G empty; returns point lists per cell
    n=0; C={}
    for name,s in [('X',x),('Y',y),('Z',z),('U',r-x-y),('V',r-x-z),('W',r-y-z)]:
        C[name]=list(range(n,n+s)); n+=s
    E=set(C['X']+C['Y']+C['U']); Fe=set(C['X']+C['Z']+C['V']); G=set(C['Y']+C['Z']+C['W'])
    return C,E,Fe,G,n

def check_cover(reqs,E,Fe,G,n,T):
    if any(len(R)>T for R in reqs): return 'size'
    pts=range(n)
    for p in pts:
        for q in pts:
            if q<p: continue
            s={p,q}
            if s&E and s&Fe and s&G:
                if not any(s<=R for R in reqs): return ('uncovered',p,q)
    return True

def S1(r,x,y,z,T,x1,y1,z1):
    C,E,Fe,G,n=cells(r,x,y,z)
    X1,X2=C['X'][:x1],C['X'][x1:]; Y1,Y2=C['Y'][:y1],C['Y'][y1:]; Z1,Z2=C['Z'][:z1],C['Z'][z1:]
    RG=set(C['X']+C['W']+Y2+Z2); RF=set(C['Y']+C['V']+X2+Z2); RE=set(C['Z']+C['U']+X2+Y2)
    R0=set(X1+Y1+Z1)
    return check_cover([RG,RF,RE,R0],E,Fe,G,n,T)

def S2(r,x,y,z,T):
    pos=lambda a:max(a,0)
    P=r+y-x-z-T; Q=r+x-y-z-T
    C,E,Fe,G,n=cells(r,x,y,z)
    b1=pos(P); c13=pos(Q)
    lo=max(0,x+y+z+pos(Q)-T); hi=min(x,T-r+x-z-pos(P)-pos(Q))
    if lo>hi: return None
    x1=lo
    X01,X03=C['X'][:x1],C['X'][x1:]
    PB1,PB2=C['V'][:b1],C['V'][b1:]
    PC13,PC0=C['W'][:c13],C['W'][c13:]
    R0=set(C['X']+PC0); R2=set(C['Y']+PB2)
    R1=set(X01+C['Y']+C['Z']+C['U']+PB1+PC13); R3=set(X03+C['Y']+C['Z']+PC13)
    return check_cover([R0,R1,R2,R3],E,Fe,G,n,T)

def S2cond(r,x,y,z,T):
    pos=lambda a:max(a,0)
    P=r+y-x-z-T; Q=r+x-y-z-T
    return (T>=r-x+z+pos(P)+pos(Q) and T>=y+z+pos(Q) and 2*T>=r+y+2*z+pos(P)+2*pos(Q)
            and x<=T<=r and y<=T)

n1=n2=0; fails=[]
for r in range(1,9):
  for x in range(r+1):
    for y in range(r+1-x):
      for z in range(r+1-max(x,y)):
        if y+z>r: continue
        for T in range(0,r+1):
          # S1: every integer split satisfying hypotheses must work
          for x1 in range(x+1):
            for y1 in range(y+1):
              for z1 in range(z+1):
                if x1+y1+z1<=T and y1+z1>=r+x-T and x1+z1>=r+y-T and x1+y1>=r+z-T:
                  n1+=1; res=S1(r,x,y,z,T,x1,y1,z1)
                  if res is not True: fails.append(('S1',r,x,y,z,T,x1,y1,z1,res))
          if S2cond(r,x,y,z,T):
            n2+=1; res=S2(r,x,y,z,T)
            if res is not True: fails.append(('S2',r,x,y,z,T,res))
print('S1 cases',n1,'S2 cases',n2,'fails',len(fails),fails[:5])

# S1 continuous closed form vs exact primal min via basic solutions
def s1min(r,x,y,z,T):
    # min x1+y1+z1 s.t. 0<=v<=cap, pair sums >= a ; exact via enumerating basic feasible points
    caps=[x,y,z]; a=[r+x-T,r+y-T,r+z-T]  # a[0]: y1+z1, a[1]: x1+z1, a[2]: x1+y1
    rows=[]
    for i in range(3):
        e=[0,0,0]; e[i]=1; rows.append((e,F(0))); rows.append((e,F(caps[i])))
    rows.append(([0,1,1],F(a[0]))); rows.append(([1,0,1],F(a[1]))); rows.append(([1,1,0],F(a[2])))
    def feas(v):
        return all(0<=v[i]<=caps[i] for i in range(3)) and v[1]+v[2]>=a[0] and v[0]+v[2]>=a[1] and v[0]+v[1]>=a[2]
    best=None
    for tri in itertools.combinations(rows,3):
        M=[list(map(F,t[0]))+[t[1]] for t in tri]
        # gaussian elimination
        ok=True
        for c in range(3):
            piv=next((i for i in range(c,3) if M[i][c]!=0),None)
            if piv is None: ok=False;break
            M[c],M[piv]=M[piv],M[c]
            for i in range(3):
                if i!=c and M[i][c]!=0:
                    f=M[i][c]/M[c][c]; M[i]=[M[i][j]-f*M[c][j] for j in range(4)]
        if not ok: continue
        v=[M[i][3]/M[i][i] for i in range(3)]
        if feas(v):
            s=sum(v); best=s if best is None or s<best else best
    return best
def s1feas(r,x,y,z,T):
    m=s1min(r,x,y,z,T); return m is not None and m<=T
def s1closed(r,x,y,z,T):
    S=x+y+z
    return (5*T>=3*r+S and all(2*T>=r+w for w in (x,y,z)) and T>=r+x-y-z and T>=r+y-x-z and T>=r+z-x-y
            and 3*T>=2*r+x+y-z and 3*T>=2*r+x+z-y and 3*T>=2*r+y+z-x)
import random
random.seed(1); mism=0; cnt=0
N=24
for x in range(N+1):
  for y in range(N+1-x):
    for z in range(N+1-max(x,y)):
      if y+z>N: continue
      for T in range(0,N+1,1):
        cnt+=1
        if s1feas(N,x,y,z,T)!=s1closed(N,x,y,z,T):
            mism+=1
            if mism<5: print('mismatch',x,y,z,T,s1min(N,x,y,z,T))
for _ in range(20000):
    D=random.choice([97,200,360])
    while True:
        x,y,z=[F(random.randint(0,D),D) for _ in range(3)]
        if x+y<=1 and x+z<=1 and y+z<=1: break
    T=F(random.randint(D//2,D),D); cnt+=1
    if s1feas(1,x,y,z,T)!=s1closed(1,x,y,z,T):
        mism+=1
        if mism<8: print('mismatch',x,y,z,T,s1min(1,x,y,z,T))
print('S1 closed-form checks',cnt,'mismatches',mism)
