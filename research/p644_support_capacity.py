"""Discover complete two-type capacity functions for bad-seven supports.

For a fixed support and row colouring, project its seven-dimensional cover
dual onto the two colour sums. Every vertex and supporting edge is certified
by rational primal/dual solutions. Independent replay remains required.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import multiprocessing
import time
import numpy as np
from scipy.optimize import linprog
from p644_support_lp_check import permutation_maps,colour_representatives


def capacity(parents,colour):
    incidence=np.array([[int(m>>j&1) for m in parents] for j in range(7)],dtype=float)
    first=[j for j in range(7) if not colour>>j&1];second=[j for j in range(7) if colour>>j&1]
    cache={};proof=[]
    def support(a,b):
        scale=a+b;key=(a/scale,b/scale)
        if key in cache:return cache[key]
        demand=[key[int(bool(colour>>j&1))] for j in range(7)]
        res=linprog(np.ones(len(parents)),A_ub=-incidence,b_ub=-np.array(demand,dtype=float),bounds=(0,None),method='highs')
        assert res.status==0
        for denominator in (1000,100000,10000000):
            y=[F(float(v)).limit_denominator(denominator) for v in res.x]
            w=[F(-float(v)).limit_denominator(denominator) for v in res.ineqlin.marginals]
            good=(all(v>=0 for v in y+w)
                  and all(sum(y[t] for t,m in enumerate(parents) if m>>j&1)>=demand[j] for j in range(7))
                  and all(sum(w[j] for j in range(7) if m>>j&1)<=1 for m in parents)
                  and sum(y)==sum(v*q for v,q in zip(w,demand)))
            if good:break
        else:raise RuntimeError('rational reconstruction failed')
        point=(sum(w[j] for j in first),sum(w[j] for j in second))
        record={'direction':list(map(str,key)),'primal':list(map(str,y)),'dual':list(map(str,w)),
                'point':list(map(str,point)),'value':str(sum(y))}
        proof.append(record);cache[key]=(point,sum(y));return cache[key]
    p,_=support(F(1),F(0));q,_=support(F(0),F(1))
    p=(p[0],F(0));q=(F(0),q[1]);points={p,q};edges=[]
    def visit(left,right):
        if left==right:return
        a=right[1]-left[1];b=left[0]-right[0]
        assert a>=0 and b>=0 and a+b>0
        point,value=support(a,b);line=(a*left[0]+b*left[1])/(a+b)
        if value==line:
            edges.append([list(map(str,left)),list(map(str,right))]);return
        assert value>line and left[0]>=point[0]>=right[0] and left[1]<=point[1]<=right[1]
        assert point not in points;points.add(point);visit(left,point);visit(point,right)
    visit(p,q)
    efficient=sorted(v for v in points if not any(v!=w and v[0]<=w[0] and v[1]<=w[1] for w in points))
    return {'vertices':[list(map(str,p)) for p in efficient],'all_vertices':[list(map(str,p)) for p in sorted(points)],
            'edges':edges,'lp_certificates':proof}


def worker(task):
    item,colours=task;out=[]
    for colour in colours:
        obj=capacity(item['maximal_cells'],colour)
        obj.update(truth_table=item['truth_table'],colour=colour);out.append(obj)
    return item['truth_table'],out


def run(workers=4,limit=None):
    root=Path('logs/astra_support_capacity');root.mkdir(exist_ok=True)
    data=json.loads(Path('logs/astra_full_support_catalog.json').read_text());maps=permutation_maps()
    items=sorted(data['orbits'],key=lambda a:(len(a['maximal_cells']),a['truth_table']))
    if limit is not None:items=items[:limit]
    tasks=[(q,colour_representatives(q['maximal_cells'],maps)) for q in items if not (root/(q['truth_table']+'.json')).exists()]
    started=time.time();count=0;functions={}
    for old in root.glob('*.json'):
        if old.name=='status.json':continue
        for row in json.loads(old.read_text()):functions[tuple(tuple(p) for p in row['vertices'])]=1
    print('Supports scheduled',len(tasks),'existing functions',len(functions),flush=True)
    with multiprocessing.get_context('spawn').Pool(workers,maxtasksperchild=10) as pool:
        for stem,rows in pool.imap_unordered(worker,tasks):
            (root/(stem+'.json')).write_text(json.dumps(rows,indent=2));count+=len(rows)
            for row in rows:functions[tuple(tuple(p) for p in row['vertices'])]=1
            status={'new_assignments':count,'different_functions':len(functions),'elapsed':time.time()-started}
            (root/'status.json').write_text(json.dumps(status,indent=2))
            print(stem,status,flush=True)
    print('FINISHED',count,'new assignments;',len(functions),'different functions',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=4);parser.add_argument('--limit',type=int)
    args=parser.parse_args();run(args.workers,args.limit)
