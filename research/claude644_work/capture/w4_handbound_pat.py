import numpy as np, itertools
from scipy.optimize import linprog
from w4_handbound_static import triple
EDGES=[('X','Y'),('X','Z'),('Y','Z'),('X','PC'),('Y','PB'),('Z','PA')]
def cells_of(x,y,z): return {'X':x,'Y':y,'Z':z,'PA':1-x-y,'PB':1-x-z,'PC':1-y-z}
def valid(pat):
    for c,d in EDGES:
        for L in pat[c]:
            for M in pat[d]:
                if not set(L)&set(M): return False
    return True
def pat_budget(pat,x,y,z,nreq=4):
    cells=cells_of(x,y,z)
    var=[(c,L) for c in pat for L in pat[c]]
    n=len(var)+1
    Aeq=[];beq=[]
    for c in pat:
        r=np.zeros(n)
        for i,(cc,L) in enumerate(var):
            if cc==c: r[i]=1
        Aeq.append(r);beq.append(cells[c])
    Aub=[];bub=[]
    for q in range(nreq):
        r=np.zeros(n)
        for i,(cc,L) in enumerate(var):
            if q in L: r[i]=1
        r[-1]=-1; Aub.append(r); bub.append(0)
    cost=np.zeros(n); cost[-1]=1
    res=linprog(cost,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*n)
    return res.fun if res.status==0 else 9
def pattern(x,y,z):
    v,sol=triple(x,y,z)
    return v,{c:[L for L,_ in sol[c]] for c in sol}
if __name__=="__main__":
    pts=[(0.3767,0.3767,z) for z in (0.1256,0.1883,0.2511,0.3139,0.3767)]+[(0.5,0.2108,0.2108),(0.5,0.23,0.1917),(0.5,0.23,0.23),(0.4958,0.23,0.21)]
    pats=[]
    for p in pts:
        v,pat=pattern(*p); pats.append(pat); print(p,round(v,4),pat)
    print('cross-eval')
    for i,pat in enumerate(pats):
        print(i,[round(pat_budget(pat,*p),4) for p in pts])
