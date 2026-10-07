"""Exact verification of a continuous oracle-row bad placement: given capacities x, types T, tau*, support index and
row roles, find cell masses by an LP that MAXIMISES the minimum slack, rationalise, and verify with Fractions:
  sum_j y_ij = x_i; found row l with type t: t_i <= w^l_i; oracle row: |w^l| > alpha* = N - tau*."""
import sys, json
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/tame')
from tc_lib import SUPPORTS
def verify(x, T, tau, idx, roles, den=10**6):
    cells=SUPPORTS[idx]; p=len(x); m=len(cells); N=sum(x); alpha=N-tau
    nv=p*m+1  # last = slack s (maximise)
    A=[];b=[];Aeq=[];beq=[]
    for i in range(p):
        r=np.zeros(nv); r[i*m:(i+1)*m]=1; Aeq.append(r); beq.append(float(x[i]))
    for l in range(7):
        if roles[l]=='O':
            r=np.zeros(nv)
            for i in range(p):
                for j in range(m):
                    if cells[j]>>l&1: r[i*m+j]=-1
            r[-1]=1; A.append(r); b.append(-float(alpha))
        else:
            t=T[int(roles[l][1:])]
            for i in range(p):
                r=np.zeros(nv)
                for j in range(m):
                    if cells[j]>>l&1: r[i*m+j]=-1
                r[-1]=1; A.append(r); b.append(-float(t[i]))
    c=np.zeros(nv); c[-1]=-1
    res=linprog(c,A_ub=np.array(A),b_ub=b,A_eq=np.array(Aeq),b_eq=beq,bounds=[(0,None)]*(nv-1)+[(None,1)],method='highs')
    if res.status!=0: return False,'LP fail'
    s=res.x[-1]
    # rationalise, fix row sums exactly on the largest cell
    y=[[F(round(res.x[i*m+j]*den),den) for j in range(m)] for i in range(p)]
    for i in range(p):
        jm=max(range(m),key=lambda j:y[i][j]); y[i][jm]+=x[i]-sum(y[i])
        if min(y[i])<0: return False,'neg'
    for l in range(7):
        w=[sum(y[i][j] for j in range(m) if cells[j]>>l&1) for i in range(p)]
        if roles[l]=='O':
            if not sum(w)>alpha: return False,('oracle fails',l,sum(w),alpha)
        else:
            t=T[int(roles[l][1:])]
            if not all(t[i]<=w[i] for i in range(p)): return False,('type fails',l)
    return True,(float(s),y)
if __name__=='__main__':
    x=[F(v) for v in json.loads(sys.argv[1])]; T=[[F(v) for v in t] for t in json.loads(sys.argv[2])]; tau=F(sys.argv[3])
    idx=int(sys.argv[4]); roles=json.loads(sys.argv[5])
    ok,info=verify(x,T,tau,idx,roles); print(ok, info if not ok else ('min slack %.4g'%info[0]))
    if ok:
        for i,row in enumerate(info[1]): print('part',i,[str(v) for v in row])
