"""Faster discovery of the same exact midpoint-subdivision certificates.

Floating point only ranks candidate regions. Every accepted leaf is verified
using Fraction arithmetic; an uncovered point is likewise checked exactly.
The independent standard-library replay does not import this module.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,time
import numpy as np
from p644_case_cover import regions,value,unbalanced_regions,triangular_region,response_choice_regions
from p644_spectrum_cover import box_tetrahedra


def certify_box(rs,budget,low,high,limit=100000,depth_limit=70):
    starts=np.cumsum([0]+[len(fs) for fs in rs])[:-1]
    forms=np.array([[float(x) for x in f] for fs in rs for f in fs])
    fb=float(budget);cache={};exact_cache={};nodes=[];roots=[];pending=[]
    for tetra in reversed(box_tetrahedra(low,high)):pending.append((tetra,0,None,None))
    def numeric(p):
        if p not in cache:cache[p]=np.maximum.reduceat(forms[:,0]+forms[:,1:]@np.array(list(map(float,p))),starts)
        return cache[p]
    def exact_ok(p,i):
        key=(p,i)
        if key not in exact_cache:exact_cache[key]=max(value(f,p) for f in rs[i])<=budget
        return exact_cache[key]
    while pending:
        tet,depth,parent,slot=pending.pop()
        maxcost=np.maximum.reduce([numeric(p) for p in tet]);eligible=np.flatnonzero(maxcost<=fb+1e-10)
        region=next((int(i) for i in eligible if all(exact_ok(p,int(i)) for p in tet)),None)
        idx=len(nodes);nodes.append(None)
        if parent is None:roots.append(idx)
        else:nodes[parent]['children'][slot]=idx
        if region is not None:nodes[idx]={'region':region};continue
        middle=tuple(sum(p[j] for p in tet)/4 for j in range(3))
        if min(numeric(middle))>fb+1e-10:
            cost=min(max(value(f,middle) for f in fs) for fs in rs)
            if cost>budget:return {'status':'UNCOVERED','point':list(map(str,middle)),'cost':str(cost),'nodes_tried':len(nodes)}
        if depth>=depth_limit or len(nodes)>=limit:return {'status':'LIMIT','nodes_tried':len(nodes),'depth':depth,'tetrahedron':[[str(x) for x in p] for p in tet]}
        a,b=max(combinations(range(4),2),key=lambda ab:sum((tet[ab[0]][j]-tet[ab[1]][j])**2 for j in range(3)))
        ratio=F(1,2)
        if False:
            # Exact facet-aligned edge cuts prevent endless dyadic refinement
            # when two sufficient regions meet on a rational boundary.
            ordering=sorted(range(len(rs)),key=lambda i:(-sum(numeric(p)[i]<=fb+1e-10 for p in tet),maxcost[i]))
            for i in ordering[:6]:
                cuts=[]
                for f in rs[i]:
                    fv=[value(f,p)-budget for p in tet]
                    for aa,bb in combinations(range(4),2):
                        if fv[aa]*fv[bb]<0:
                            rr=-fv[aa]/(fv[bb]-fv[aa])
                            cuts.append((min(rr,1-rr),aa,bb,rr))
                if cuts:
                    _,a,b,ratio=max(cuts);break
        mid=tuple((1-ratio)*tet[a][j]+ratio*tet[b][j] for j in range(3))
        left=list(tet);left[a]=mid;right=list(tet);right[b]=mid
        nodes[idx]={'edge':[a,b],'children':[None,None]}
        if ratio!=F(1,2):nodes[idx]['weight']=str(ratio)
        pending.append((right,depth+1,idx,1));pending.append((left,depth+1,idx,0))
    return {'status':'COVERED','nodes':nodes,'roots':roots}


def run(budget=F(87,100),output=None,high=F(49,100),low=F(27,100)):
    if output is None:output='logs/astra_spectrum_response_choice_'+str(budget).replace('/','_')+'_'+str(high).replace('/','_')+'_'+str(low).replace('/','_')+'.json'
    data=json.loads(Path('logs/astra_static_template_facets.json').read_text());rs=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()
    todo=[(F(i,200),F(i+1,200),0) for i in reversed(range(int(low*200),int(high*200)))];rows=[];start=time.monotonic()
    while todo:
        a,b,depth=todo.pop();mid=(a+b)/2
        candidates=[]
        if mid<=F(37,100):candidates.append(2-budget-a-F(99,200))
        elif mid>=F(2,5):candidates.append(2-budget-a-F(37,100))
        else:candidates.extend([F(7,20),F(69,200),F(71,200)])
        candidates+=[(2-budget-a)/2]
        # Retain the same symmetry-breaking cap orientation but search nearby
        # cap values when the first few formulas leave a genuine hole.
        candidates += [F(i,1000) for i in range(330,401,5)]
        success=None;failures=[]
        for u in dict.fromkeys(candidates):
            v=2-budget-a-u
            if u<1-budget or u>1-b or v<0:continue
            q=certify_box(rs,budget,(a,F(0),F(0)),(b,u,v),limit=20000)
            if q['status']=='COVERED':success={'interval':[str(a),str(b)],'u':str(u),'v_at_left':str(v),'proof':q};break
            failures.append({'u':str(u),'v':str(v),'result':q})
        if success:
            rows.append(success)
            print('COVER',float(a),float(b),'nodes',len(q['nodes']),'seconds',round(time.monotonic()-start,1),flush=True)
        elif depth<6:
            todo.append((mid,b,depth+1));todo.append((a,mid,depth+1))
        else:
            result={'status':'FAILED','budget':str(budget),'interval':[str(a),str(b)],'failures':failures}
            Path(output+'.failure.json').write_text(json.dumps(result,indent=1))
            print('FAILED',str(a),str(b),'seconds',round(time.monotonic()-start,1),flush=True);return result
    out={'status':'COVERED','budget':str(budget),'interval':[str(low),str(high)],
         'static_templates':[row['triangle'] for row in data],'adaptive_version':4,'slabs':rows}
    Path(output).write_text(json.dumps(out,separators=(',',':')))
    print('DONE',len(rows),'slabs;',sum(len(row['proof']['nodes']) for row in rows),'nodes;',round(time.monotonic()-start,1),'seconds',flush=True)
    return out

if __name__=='__main__':
    import sys
    run(F(sys.argv[1]) if len(sys.argv)>1 else F(87,100),high=F(sys.argv[2]) if len(sys.argv)>2 else F(49,100),low=F(sys.argv[3]) if len(sys.argv)>3 else F(27,100))
