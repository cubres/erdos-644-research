"""NUMERICAL discovery: K1 u K2 u C(Z,k), Z = Z1 u Z2, Zi subset Ui, |Zi|=z, |Ui|=1+d (rank 1).
Parts: Z1, P1=U1\\Z1, Z2, P2.  Types discretised.  Look for bad tuple."""
import sys
sys.path.insert(0,'..')
from fractions import Fraction as F
from w4_typeclosed_lib import bad_tuple_milp, tau_star
def run(d, z, nstep=8):
    x=[z, 1+d-z, z, 1+d-z]
    types=[]
    lo=max(F(0),1-(1+d-z)); 
    for i in range(nstep+1):
        a=lo+(z-lo)*F(i,nstep)
        types.append((a,1-a,F(0),F(0))); types.append((F(0),F(0),a,1-a))
    lo2=max(F(0),1-z)
    for i in range(2*nstep+1):
        a=lo2+(z-lo2)*F(i,2*nstep)
        types.append((a,F(0),1-a,F(0)))
    types=sorted(set(types))
    ts=tau_star(types,x)
    st,ass,cells=bad_tuple_milp(types,x,time_limit=300)
    print(float(d),float(z),'ntypes',len(types),'tau*',float(ts),st,[types[a] for a in ass] if ass else None,flush=True)
if __name__=='__main__':
    d=F(sys.argv[1]); z=F(sys.argv[2]); run(d,z,int(sys.argv[3]) if len(sys.argv)>3 else 8)
