exec(open('work/paper_push/general/fork_single_lp.py').read().split('for i,(obj,const)')[0])
# q=bA, p=aB. Constants tracked separately.
D1=[(sb-eb+q/2-sa-p-ec,1),(-sa-2*sb-sc-2*ec-2*q-2*eb-p,4)]
# second D1 term divided by 2: q/2+sb-eb+(aC+3bC-sc-2ec)/2
D1[1]=(D1[1][0]/2,2)
D2=[(sb/2+q/2-sa-p-ec,1),(-sa-sb/2-sc/2-ec-p-q/2,2)]
# D2 high: q/2+sb/2+aC+bC-sc/2-ec
# exchange fails q>ea/2 OR 4ea+4eb-sa-sb-p-q<1
fails=[(ea/2-q,0),(4*ea+4*eb-sa-sb-p-q,1)]
for i,(d1,c1) in enumerate(D1):
 for j,(d2,c2) in enumerate(D2):
  for h,(f,fc) in enumerate(fails):
   constraints=ineq+[(-d1,c1-.75),(-d2,c2-.75),(f,fc)]
   # require an interior margin for all three own gaps, E, incoming arrows,
   # the failed pencil, and both bad costs plus the failed exchange branch.
   strict=[(2*ea-sa,0),(2*eb-sb,0),(2*ec-sc,0),(-ea-eb-ec,-.75),(sa+p+ec,1),(sb+q+ec,1),(2*sa+2*p+sc+2*ec,2),(-d1,c1-.75),(-d2,c2-.75),(f,fc)]
   AA=[list(a)+[0] for a,b in constraints]+[list(a)+[1] for a,b in strict]
   bb=[b for a,b in constraints]+[b for a,b in strict]
   sol=linprog([0]*9+[-1],A_ub=AA,b_ub=bb,bounds=[(0,None)]*9+[(0,.01)],method='highs')
   if sol.success and sol.x[-1]>1e-8:print('OPEN',i,j,h,'margin',sol.x[-1],'state',sol.x[:9])
