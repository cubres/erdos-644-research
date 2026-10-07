"""Exact continuous first-stage pair-interval elimination certificate."""
from fractions import Fraction as F
from itertools import permutations,combinations
from pathlib import Path
import json,time
from p644_case_cover import regions,value


def box_tetrahedra(low,high):
    result=[]
    for perm in permutations(range(3)):
        p=list(low);tetra=[tuple(p)]
        for i in perm:p[i]=high[i];tetra.append(tuple(p))
        result.append(tetra)
    return result


def certify_box(rs,budget,low,high,limit=10000,depth_limit=35):
    cache={};nodes=[];roots=[];pending=[]
    for tetra in reversed(box_tetrahedra(low,high)):pending.append((tetra,0,None,None))
    def at(p):
        if p not in cache:cache[p]=[max(value(f,p) for f in fs) for fs in rs]
        return cache[p]
    while pending:
        tet,depth,parent,slot=pending.pop();vs=[at(p) for p in tet]
        region=next((i for i in range(len(rs)) if max(v[i] for v in vs)<=budget),None)
        idx=len(nodes);nodes.append(None)
        if parent is None:roots.append(idx)
        else:nodes[parent]['children'][slot]=idx
        if region is not None:nodes[idx]={'region':region};continue
        middle=tuple(sum(p[j] for p in tet)/4 for j in range(3));cost=min(at(middle))
        if cost>budget:return {'status':'UNCOVERED','point':list(map(str,middle)),'cost':str(cost)}
        if depth>=depth_limit or len(nodes)>=limit:return {'status':'LIMIT'}
        a,b=max(combinations(range(4),2),key=lambda ab:sum((tet[ab[0]][j]-tet[ab[1]][j])**2 for j in range(3)))
        mid=tuple((tet[a][j]+tet[b][j])/2 for j in range(3))
        left=list(tet);left[a]=mid;right=list(tet);right[b]=mid
        nodes[idx]={'edge':[a,b],'children':[None,None]}
        pending.append((right,depth+1,idx,1));pending.append((left,depth+1,idx,0))
    return {'status':'COVERED','nodes':nodes,'roots':roots}


def run(budget=F(3499,4000),output='logs/astra_spectrum_cover.json'):
    data=json.loads(Path('logs/astra_static_template_facets.json').read_text());rs=regions(data)
    todo=[(F(i,200),F(i+1,200),0) for i in reversed(range(54,98))];rows=[];start=time.monotonic()
    while todo:
        a,b,depth=todo.pop();mid=(a+b)/2
        candidates=[]
        if mid<=F(37,100):candidates.append(2-budget-a-F(99,200))
        elif mid>=F(2,5):candidates.append(2-budget-a-F(37,100))
        else:candidates.extend([F(7,20),F(69,200),F(71,200)])
        candidates+=[(2-budget-a)/2]
        success=None
        for u in dict.fromkeys(candidates):
            v=2-budget-a-u
            if u<1-budget or u>1-b or v<0:continue
            q=certify_box(rs,budget,(a,F(0),F(0)),(b,u,v),limit=5000)
            if q['status']=='COVERED':success={'interval':[str(a),str(b)],'u':str(u),'v_at_left':str(v),'proof':q};break
        if success:
            rows.append(success)
            print('COVER',float(a),float(b),'nodes',len(q['nodes']),'seconds',round(time.monotonic()-start,1),flush=True)
        elif depth<6:
            todo.append((mid,b,depth+1));todo.append((a,mid,depth+1))
        else:
            print('FAILED',str(a),str(b),q,flush=True)
            Path('logs/astra_spectrum_cover_failure.json').write_text(json.dumps({'budget':str(budget),'interval':[str(a),str(b)],'last':q},indent=1))
            return {'status':'FAILED'}
    out={'status':'COVERED','budget':str(budget),'interval':['27/100','49/100'],
         'static_templates':[row['triangle'] for row in data],'slabs':rows}
    Path(output).write_text(json.dumps(out,separators=(',',':')))
    print('DONE',len(rows),'slabs;',sum(len(row['proof']['nodes']) for row in rows),'nodes;',round(time.monotonic()-start,1),'seconds',flush=True)
    return out


if __name__=='__main__':run()
