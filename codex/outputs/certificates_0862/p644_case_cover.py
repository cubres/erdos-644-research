"""Exact tetrahedral coverage by static-template and adaptive budget regions."""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import json,time


def regions(data):
    out=[[tuple(map(F,f)) for f in row['forms']] for row in data]
    # x,y are the two intersections with the central edge; z is the other.
    base=[(F(0),F(2),F(0),F(1)),(F(0),F(0),F(2),F(1)),
          (F(1,3),F(2,3),F(2,3),F(1)),
          (F(2,5),F(4,5),F(2,5),F(3,5)),
          (F(2,5),F(2,5),F(4,5),F(3,5))]
    for excluded in range(3):
        perm=[i for i in range(3) if i!=excluded]+[excluded]
        fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def value(f,p):return f[0]+sum(a*b for a,b in zip(f[1:],p))


def unbalanced_regions():
    """Lemma 7.23: the first adaptive cut need not be balanced."""
    base=[(F(0),F(1),F(1),F(1)),
          (F(1,3),F(1),F(1,3),F(2,3)),
          (F(1,3),F(1,3),F(1),F(2,3)),
          (F(2,5),F(3,5),F(3,5),F(3,5)),
          (F(1,3),F(2,3),F(2,3),F(1))]
    out=[]
    for excluded in range(3):
        perm=[i for i in range(3) if i!=excluded]+[excluded];fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def triangular_region():
    """Lemma 7.25: three final requests with pairwise-overlapping labels."""
    out=[]
    for mask in range(8):
        n=sum((mask>>j)&1 for j in range(3));den=1+2*n
        out.append((F(n,den),)+tuple(F(1+2*((mask>>j)&1),den) for j in range(3)))
    out.append((F(1,3),F(2,3),F(2,3),F(2,3)))
    return out


def response_choice_regions():
    """Lemma 7.26: select the final allocation after the fourth response."""
    base=[(F(0),F(1),F(1),F(1)),
          (F(1),F(-1),F(0),F(1)),
          (F(1),F(0),F(-1),F(1)),
          (F(1),F(-1),F(1,2),F(0)),
          (F(1),F(1,2),F(-1),F(0)),
          (F(1,3),F(2,3),F(2,3),F(1,3))]
    out=[]
    for excluded in range(3):
        perm=[i for i in range(3) if i!=excluded]+[excluded];fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def gap_regions(h,low):
    """Conditional local regions when all pair sizes in [low,h] are absent."""
    h,low=F(h),F(low)
    # x is the selected anchor-pair intersection. The first four forms bound
    # the core and cuts, the next four bound the two split-partner requests.
    base=[(F(0),F(1),F(1),F(1)),
          (1-h,F(0),F(0),F(1)),(1-h,F(0),F(1),F(0)),
          (2-2*h,F(-1),F(0),F(0)),
          (F(1,3),F(1),F(0),F(0)),
          ((2-h)/3,F(2,3),F(-1,3),F(0)),
          ((2-h)/3,F(2,3),F(0),F(-1,3)),
          ((3-2*h)/3,F(1,3),F(-1,3),F(-1,3)),
          (2*low,F(0),F(1),F(1))]
    out=[]
    for large in range(3):
        perm=[large]+[j for j in range(3) if j!=large];fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def dominant_pair_regions():
    """Lemma 7.29: either separate the three pairs or split the dominant one."""
    out=[]
    for x in range(3):
        y,z=[j for j in range(3) if j!=x]
        fs=[(F(1,2),F(1,2),F(1,2),F(1,2))]
        for a,b in ((y,z),(z,y)):
            row=[F(1),F(0),F(0),F(0)];row[x+1]=-1;row[a+1]=1;row[b+1]=-1;fs.append(tuple(row))
        row=[F(1,3),F(0),F(0),F(0)];row[x+1]=1;fs.append(tuple(row))
        out.append(fs)
    return out


def partial_core_regions():
    """Lemma 7.31: four response cases for the surviving triple cell."""
    base=[(F(0),F(1),F(1),F(0)),
          (F(1,2),F(1),F(0),F(0)),(F(1,2),F(0),F(1),F(0)),
          (F(1),F(1),F(-1),F(-1)),(F(1),F(-1),F(1),F(-1)),
          (F(1),F(-1,3),F(-1,3),F(-1,3)),
          (F(3,5),F(1,5),F(1,5),F(1,5)),
          (F(1,3),F(1,3),F(1,3),F(2,3)),
          (F(1,2),F(0),F(0),F(3,4))]
    out=[]
    for z in range(3):
        perm=[j for j in range(3) if j!=z]+[z];fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def padded_pair_regions():
    """Lemma 7.32: cut the F-private part, split B and distribute C."""
    from itertools import permutations
    base=[(F(0),F(1),F(1),F(1)),
          (F(1,2),F(0),F(1),F(0)),
          (F(1,2),F(1),F(-1,2),F(1,2)),
          (F(1,3),F(2,3),F(1,3),F(1))]
    out=[]
    for perm in permutations(range(3)):
        fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def padded_dominant_regions():
    """Lemma 7.33: split B and distribute A when the simple third is full."""
    from itertools import permutations
    base=[(F(0),F(1),F(1),F(1)),
          (F(1,3),F(1),F(0),F(0)),
          (F(1),F(-1),F(0),F(1)),
          (F(1,3),F(2,3),F(1),F(1,3))]
    out=[]
    for perm in permutations(range(3)):
        fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def cover(cap=F(377,1000),budget=F(437,500),max_nodes=100000,max_depth=35):
    data=json.loads(Path('logs/astra_static_template_facets.json').read_text());rs=regions(data)
    verts=[(F(0),)*3,(cap,F(0),F(0)),(cap,cap,F(0)),(cap,)*3]
    cache={};nodes=[];start=time.monotonic();pending=[(verts,0,None,None)]
    def at(p):
        if p not in cache:cache[p]=[max(value(f,p) for f in fs) for fs in rs]
        return cache[p]
    while pending:
        tetra,depth,parent,slot=pending.pop();vs=[at(p) for p in tetra]
        region=next((i for i in range(len(rs)) if max(v[i] for v in vs)<=budget),None)
        idx=len(nodes);nodes.append(None)
        if parent is not None:nodes[parent]['children'][slot]=idx
        if region is not None:nodes[idx]={'region':region};continue
        middle=tuple(sum(p[j] for p in tetra)/4 for j in range(3));cost=min(at(middle))
        if cost>budget:
            print('UNCOVERED POINT',list(map(str,middle)),str(cost),flush=True)
            return {'status':'UNCOVERED','point':list(map(str,middle)),'cost':str(cost)}
        if depth>=max_depth or len(nodes)>=max_nodes:
            print('LIMIT',len(nodes),depth,flush=True);return {'status':'LIMIT'}
        a,b=max(combinations(range(4),2),key=lambda ij:sum((tetra[ij[0]][j]-tetra[ij[1]][j])**2 for j in range(3)))
        midpoint=tuple((tetra[a][j]+tetra[b][j])/2 for j in range(3))
        left=list(tetra);left[a]=midpoint;right=list(tetra);right[b]=midpoint
        nodes[idx]={'edge':[a,b],'children':[None,None]}
        pending.append((right,depth+1,idx,1));pending.append((left,depth+1,idx,0))
        if len(nodes)%1000<2:print('PROGRESS',len(nodes),len(pending),round(time.monotonic()-start,1),flush=True)
    out={'status':'COVERED','cap':str(cap),'budget':str(budget),'nodes':nodes,
         'static_templates':[row['triangle'] for row in data]}
    Path('logs/astra_small_cap_cover.json').write_text(json.dumps(out,separators=(',',':')))
    print('COVERED',len(nodes),'nodes;',len(cache),'points;',round(time.monotonic()-start,1),'seconds',flush=True)
    return out


if __name__=='__main__':cover()
