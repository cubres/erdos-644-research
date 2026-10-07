"""Bounded second-response discovery with ALL relevant endpoint/seven-row constraints.

The original six rows have the weighted principal support described in the
report; three dust cells and private padding restore uniformity and pairwise
intersection. The first response is fixed. Second response masses may be
fractional. Feasible outputs are independently evaluated, and are NOT proofs
that every future response can coexist. Pair counts are evaluated explicitly.
"""
from itertools import combinations
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


class Model:
    def __init__(self, scale=160, example='alternate', epsilon=1e-5):
        self.scale = scale
        self.epsilon = epsilon
        self.k = 3.5*scale+3
        self.m = 3*scale
        self.q = 2.25*scale*scale
        if example == 'alternate':
            traces = [3/8, 3/2, 0, 7/8, 0, 5/8]
        elif example == 'symmetric':
            traces = [19/16, 19/16, 0, 9/16, 0, 9/16]
        elif example == 'original':
            traces = [0, 3/8, 1, 9/16, 1, 9/16]
        else:
            raise ValueError(example)
        self.cells=[]
        for name, mask, cap, trace in zip('ABCDEF',[19,44,14,21,41,50],[1.5,1.5,1,1,1,1],traces):
            if trace:
                self.cells.append((name+'+',mask,1,trace*scale))
            if trace<cap:
                self.cells.append((name+'-',mask,0,(cap-trace)*scale))
        self.principal_count=len(self.cells)
        for name, mask in [('u',7),('v',26),('w',38)]:
            self.cells.append((name,mask,0,1))
        for i, count in enumerate([2,0,1,2,2,2]):
            if count:
                self.cells.append(('p'+str(i+1),1<<i,0,count))
        self.n=len(self.cells)
        self.weights=np.array([c[3] for c in self.cells])
        self.graphs=[]
        self.graph_names=[]
        # Six-tuples containing only the second new row.
        for omitted in range(6):
            self.graphs.append(self.graph(63^(1<<omitted),False))
            self.graph_names.append('five_old_omit_'+str(omitted+1))
        # Six-tuples containing both new rows.
        for rows in combinations(range(6),4):
            self.graphs.append(self.graph(sum(1<<i for i in rows),True))
            self.graph_names.append('four_old_'+''.join(str(i+1) for i in rows))
        # Seven-tuples containing all six original rows, or five plus both new.
        self.seven_graphs=[self.graph(63,False)]
        self.seven_names=['six_old']
        for omitted in range(6):
            self.seven_graphs.append(self.graph(63^(1<<omitted),True))
            self.seven_names.append('five_old_first_omit_'+str(omitted+1))
        self.build()

    def graph(self, rows, require_first):
        return [[j for j,(_,other,flag2,_) in enumerate(self.cells)
                 if i!=j and ((mask|other)&rows)==rows and (not require_first or flag or flag2)]
                for i,(_,mask,flag,_) in enumerate(self.cells)]

    def build(self):
        n=self.n
        self.nv=2*n+len(self.graphs)*n+1
        self.margin_index=self.nv-1
        rows=[]; lower=[]; upper=[]
        def add(terms,lo=-np.inf,hi=np.inf):
            rows.append(terms);lower.append(lo);upper.append(hi)
        add({i:1 for i in range(n)},hi=self.k)
        for i,w in enumerate(self.weights):
            add({i:1,n+i:-w},hi=0)
            add({i:1,n+i:-self.epsilon},lo=0)
        for graph in self.seven_graphs:
            add({n+i:1 for i,nb in enumerate(graph) if nb},lo=1)
        for g,graph in enumerate(self.graphs):
            base=2*n+g*n
            for i,nb in enumerate(graph):
                if not nb:
                    add({base+i:1},hi=0)
                else:
                    terms={base+i:1,i:-1}
                    for j in nb:terms[n+j]=-self.weights[i]
                    add(terms,hi=0)
            terms={base+i:1 for i in range(n)}
            terms[self.margin_index]=-1
            add(terms,lo=self.m)
        matrix=lil_matrix((len(rows),self.nv))
        for r,row in enumerate(rows):
            for c,value in row.items():matrix[r,c]=value
        self.constraint=LinearConstraint(matrix.tocsr(),lower,upper)
        self.lb=np.zeros(self.nv);self.lb[-1]=-sum(self.weights)
        self.ub=np.r_[self.weights,np.ones(n),np.tile(self.weights,len(self.graphs)),sum(self.weights)]
        self.integer=np.zeros(self.nv);self.integer[n:2*n]=1
        self.objective=np.zeros(self.nv);self.objective[-1]=-1

    def evaluate(self, selected):
        output=[]
        for name,graph in zip(self.graph_names,self.graphs):
            endpoint=0.;pairs=0.
            for i,nb in enumerate(graph):
                if not nb:continue
                endpoint+=self.weights[i] if any(selected[j]>1e-8 for j in nb) else selected[i]
                for j in nb:
                    if i<j:
                        pairs+=self.weights[i]*selected[j]+self.weights[j]*selected[i]-selected[i]*selected[j]
            output.append({'tuple':name,'endpoint_mass':endpoint,'pair_count':pairs,
                           'lex_ok':bool(endpoint>self.m+1e-7 or (endpoint>=self.m-1e-7 and pairs>=self.q-1e-7))})
        seven=[]
        for name,graph in zip(self.seven_names,self.seven_graphs):
            seven.append({'tuple':name,'two_pierceable':any(selected[i]>1e-8 and nb for i,nb in enumerate(graph))})
        return output,seven

    def solve(self, deletion, seconds=10):
        ub=self.ub.copy()
        for i in range(self.n):
            ub[i]=max(0,self.weights[i]-deletion.get(self.cells[i][0],0))
            if ub[i]<self.epsilon:ub[self.n+i]=0
        res=milp(self.objective,integrality=self.integer,bounds=Bounds(self.lb,ub),
                 constraints=self.constraint,options={'time_limit':seconds,'mip_rel_gap':0})
        answer={'status':int(res.status),'message':res.message,'deletion':deletion,
                'cost':sum(deletion.values()),'margin':None if res.fun is None else -float(res.fun)}
        if res.x is not None:
            selected=res.x[:self.n]
            answer['selected']={self.cells[i][0]:float(x) for i,x in enumerate(selected) if x>1e-8}
            answer['six_checks'],answer['seven_checks']=self.evaluate(selected)
            answer['all_lex_ok']=all(row['lex_ok'] for row in answer['six_checks'])
            answer['all_seven_ok']=all(row['two_pierceable'] for row in answer['seven_checks'])
        return answer


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--example',default='alternate')
    parser.add_argument('--scale',type=int,default=160)
    parser.add_argument('--seconds',type=float,default=10)
    parser.add_argument('--delete',default='{}')
    args=parser.parse_args()
    model=Model(args.scale,args.example)
    deletion={name:float(value) for name,value in json.loads(args.delete).items()}
    for name,_,_,mass in model.cells[model.principal_count:]:deletion[name]=mass
    answer=model.solve(deletion,args.seconds)
    path=Path(__file__).resolve().parents[1]/'outputs'/('agent_full_response_'+args.example+'.json')
    path.write_text(json.dumps(answer,indent=2)+'\n')
    print(json.dumps({key:value for key,value in answer.items() if key not in ['six_checks','seven_checks','selected']}))
