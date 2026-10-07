"""Full G3 discovery for fixed eight-row weighted states.
All six- and seven-tuples involving G3 are imposed. Existing subfamilies
must be checked separately. Tuples whose preceding rows have a common
point are automatically safe since k > the endpoint minimum.
"""
from itertools import combinations
from p644_agent_alternative_full_response import Model
from p644_agent_alternative_third_scan import cells_for

class ThirdModel(Model):
 def __init__(self,g,M=20,h=0,epsilon=1e-5):
  self.k=28*M+3;self.m=24*M;self.q=144*M*M;self.epsilon=epsilon
  self.cells=[(name,mask,0,w) for name,mask,w in cells_for(g,M,h)]
  self.n=len(self.cells);self.principal_count=self.n
  import numpy as np
  self.weights=np.array([c[3] for c in self.cells])
  self.graphs=[];self.graph_names=[];self.seven_graphs=[];self.seven_names=[]
  for count in [5,6]:
   for rows in combinations(range(8),count):
    mask=sum(1<<i for i in rows)
    if any(c[1]&mask==mask for c in self.cells):continue
    graph=[[j for j,other in enumerate(self.cells) if j!=i and ((c[1]|other[1])&mask)==mask]
           for i,c in enumerate(self.cells)]
    name=''.join(str(i+1) for i in rows)
    if count==5:self.graphs.append(graph);self.graph_names.append(name)
    else:self.seven_graphs.append(graph);self.seven_names.append(name)
  self.build()

if __name__=='__main__':
 import json
 g=dict(zip(['A+','C-','D+','D-','E-','F+','F-'],[60,120,60,0,120,60,0]));h=20
 m=ThirdModel(g,20,h)
 deletion={'A+2':60,'B+n':110,'E-2':120,'E-n':40,'F+2':60,'F+n':40,'p4n':2}
 r=m.solve(deletion,30)
 print(json.dumps(r,indent=2))
