import numpy as np
from scipy.optimize import linprog
# Variables sA,sB,sC,eA,eB,eC,aB,bA,cA (aC=1-sA-aB etc)
v=np.eye(9); sa,sb,sc,ea,eb,ec,p,q,r=v
z=np.zeros(9)
ineq=[]
def add(a,b=0): ineq.append((a,b))
for s,e in [(sa,ea),(sb,eb),(sc,ec)]:
 add(-s-e,-.75); add(2*e-s)
add(-ea-eb-ec,-.75)
for f in [ea+eb,ea+ec,eb+ec]:add(f,.75)
add(sa+p,1);add(sb+q,1);add(sc+r,1)
add(p-eb);add(q-ea);add(r-ea);add(-sc-r-eb,-1)
# incoming arrows aC,bC
add(sa+p+ec,1);add(sb+q+ec,1)
# failed a pencil, fitting b pencil; ec<=.25
add(2*sa+2*p+sc+2*ec,2);add(-2*sb-2*q-sc-2*ec,-2);add(ec,.25)
# target cost max clauses
objectives=[(sb-eb,0),(sb-eb-sa-p-ec,1),(-eb-sa-p-q-sc-ec,2),( -sb-eb-2*q-sc-ec,2),(-2*sa-2*sb-2*sc-3*ec-eb-2*p-3*q,5)]
for i,(obj,const) in enumerate(objectives):
 sol=linprog(-obj,A_ub=[a for a,b in ineq],b_ub=[b for a,b in ineq],bounds=[(0,None)]*9,method='highs')
 print(i, const-sol.fun,sol.x)
