# adversarial hill-climb: two sliced boxes over p parts; maximize lambda* (min capacity scale for small templates)
import random, sys, itertools
from scipy.optimize import linprog
exec(open('twoconvex.py').read().split("stats={")[0].replace("p=int(sys.argv[1]) if len(sys.argv)>1 else 3","p=int(sys.argv[1])"))
def lam_pair(x,boxA,boxB,facets):
    lA,hA=boxA; lB,hB=boxB
    # vars s,t,lam ; min lam ; u s_i + v t_i - lam x_i <= 0
    n=2*p+1; A=[];b=[]
    for i in range(p):
        for u,v in facets:
            row=[0.0]*n; row[i]=u; row[p+i]=v; row[-1]=-x[i]; A.append(row); b.append(0.0)
    Aeq=[[1.0]*p+[0.0]*p+[0.0],[0.0]*p+[1.0]*p+[0.0]]
    bounds=[(lA[i],hA[i]) for i in range(p)]+[(lB[i],hB[i]) for i in range(p)]+[(0,None)]
    c=[0.0]*(n-1)+[1.0]
    r=linprog(c,A_ub=A,b_ub=b,A_eq=Aeq,b_eq=[1,1],bounds=bounds,method='highs')
    return r.fun if r.status==0 else 9.0
def lamstar(x,boxes,T=SMALL):
    comps=[(boxes[0],boxes[1]),(boxes[1],boxes[0]),(boxes[0],boxes[0]),(boxes[1],boxes[1])]
    return min(lam_pair(x,A_,B_,f) for A_,B_ in comps for f in T.values())
def valid(x,raw):
    boxes=[]
    for l,h in raw:
        h=[min(x[i],h[i]) for i in range(p)]
        l,h=tighten(l,h)
        if any(l[i]>h[i]+1e-12 or l[i]<-1e-12 for i in range(p)) or sum(l)>1+1e-12 or sum(h)<1-1e-12: return None
        boxes.append((l,h))
    return boxes
def score(state):
    x,raw=state
    boxes=valid(x,raw)
    if boxes is None: return -9,None,None
    t=tau(x,boxes)
    if t<0.7501: return -9+t,t,None
    ls=lamstar(x,boxes)
    return ls,t,boxes
best_overall=0
for run in range(int(sys.argv[2])):
    random.seed(run*7+int(sys.argv[3]))
    x=[random.uniform(0.5,1.5) for _ in range(p)]
    raw=[([random.uniform(0,0.5) for _ in range(p)],[random.uniform(0.3,1) for _ in range(p)]) for _ in range(2)]
    st=(x,raw); sc,t,bx=score(st)
    tries=0
    while sc<-8 and tries<200:
        x=[random.uniform(0.5,1.7) for _ in range(p)]
        raw=[([random.choice([0,random.uniform(0,0.6)]) for _ in range(p)],[random.uniform(0.2,1) for _ in range(p)]) for _ in range(2)]
        st=(x,raw); sc,t,bx=score(st); tries+=1
    step=0.1
    for it in range(400):
        x,raw=st
        x2=[max(0.05,v+random.gauss(0,step)) for v in x]
        raw2=[([max(0,v+random.gauss(0,step)) if random.random()<0.5 else v for v in l],[max(0,v+random.gauss(0,step)) if random.random()<0.5 else v for v in h]) for l,h in raw]
        s2,t2,b2=score((x2,raw2))
        if s2>=sc: st,sc,t,bx=(x2,raw2),s2,t2,b2
        if it%100==99: step*=0.6
    print(f'run {run} lam*={sc:.4f} tau={t}', [round(v,3) for v in st[0]], flush=True)
    if sc>best_overall: best_overall=sc; print('   boxes',bx)
print('best',best_overall)
