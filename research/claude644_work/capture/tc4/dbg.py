import random
from h2resid import tau_star_w
exec(open('resid_stair.py').read().split("rng=random.Random")[0])
rng=random.Random(2); shown=0; cnt=0
for trial in range(200000):
    x0=rng.uniform(0.02,0.5); xj=rng.uniform(0.76,1.5); xk=rng.uniform(0.76,1.5)
    if xj+xk<=2.25: continue
    thj=rng.uniform(2*xj/3,min(1,xj)); thk=rng.uniform(2*xk/3,min(1,xk))
    eps0=(xj-thj)+(xk-thk)-0.75
    if eps0<=0: continue
    cnt+=1
    x=[x0,xj,xk]
    pA=rng.uniform(0,min(4*x0/7,1-thk)); qB=rng.uniform(0,min(4*x0/7,1-thj))
    if pA+qB<=x0: continue
    A=[(pA,1-pA-thk,thk),(0,1-thk-eps0/2-x0/2,thk+eps0/2+x0/2)]; B=[(qB,thj,1-qB-thj),(0,thj+eps0/2+x0/2,1-thj-eps0/2-x0/2)]
    t,u=tau_star_w(A+B,x)
    print(round(t,3),'x',[round(v,3) for v in x],'th',round(thj,3),round(thk,3),'eps0',round(eps0,3),'p,q',round(pA,3),round(qB,3),'u',[round(v,3) for v in u]); shown+=1
    if shown>8: break
print('eps0>0 count',cnt)
