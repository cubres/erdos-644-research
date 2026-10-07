"""Independent exact checker for the NEW five-old-pair response certificate.

Standard library only. Does not import any producer or optimization code.
Reconstructs the finite state, inequalities, residual upper bounds and root-box
coverage. The theorem is conditional on this state and a paired global Q minimum.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse,json,hashlib

F=Fraction
TYPES=[tuple(map(int,s)) for s in ['00001','00010','01100','01111','10011','11111','10100','10111','11000','11011']]
MASS=[F(s) for s in ['1/4','1/4','1/4','1/4','6/25','6/25','1/4','1/100','1/4','1/100']]
R_BINS=[0,1,2,4,5,8,9]
R_CAP=[F(s) for s in ['1/4','1/4','1/8','1/8','6/25','1/4','1/100']]
NR,NH=7,10
NVAR=NR+NH+NR*NH+1
OBJECTIVE=NVAR-1
TARGET=F(6,25)

def rat(x):
    assert isinstance(x,(str,int)) and not isinstance(x,bool), 'non-exact rational encoding'
    return F(x)

def prod(i,j):return NR+NH+i*NH+j

def matrix(box_low,box_high):
    rows=[]
    def add(label,terms,rhs):
        row={}
        for index,value in terms:
            row[index]=row.get(index,F(0))+F(value)
        rows.append((label,{i:v for i,v in row.items() if v},F(rhs)))
    add('rank_R',[(i,1) for i in range(NR)],1)
    add('rank_H',[(NR+j,1) for j in range(NH)],1)
    for i,b in enumerate(R_BINS):add('cell_%d'%b,[(i,1),(NR+b,1)],MASS[b])

    # Expand (ar*R_i+br)*(ah*H_j+bh)>=0. Replacing R_i H_j
    # by its product variable gives the four McCormick inequalities.
    def nonnegative_product(label,i,j,ar,br,ah,bh):
        add(label,[(prod(i,j),-ar*ah),(i,-ar*bh),(NR+j,-br*ah)],br*bh)
    for i in range(NR):
        low,high=box_low[i],box_high[i]
        for j in range(NH):
            width=MASS[j]
            nonnegative_product('mcc_lower0_%d_%d'%(i,j),i,j,1,-low,1,0)
            nonnegative_product('mcc_lower1_%d_%d'%(i,j),i,j,-1,high,-1,width)
            nonnegative_product('mcc_upper0_%d_%d'%(i,j),i,j,-1,high,1,0)
            nonnegative_product('mcc_upper1_%d_%d'%(i,j),i,j,1,-low,-1,width)
        add('rlt_R_%d'%i,[(prod(i,j),1) for j in range(NH)]+[(i,-1)],0)
    for j in range(NH):add('rlt_H_%d'%j,[(prod(i,j),1) for i in range(NR)]+[(NR+j,-1)],0)

    for a,b in combinations(range(5),2):
        terms=[(OBJECTIVE,1)]
        for i,old_bin in enumerate(R_BINS):
            for j in range(NH):
                # A point from each new disjoint edge must jointly hit both
                # sides of each retained old cut: the two bits must differ.
                hits=all({TYPES[old_bin][d],TYPES[j][d]}=={0,1} for d in (a,b))
                if hits:terms.append((prod(i,j),-1))
        add('Q_%d_%d'%(a,b),terms,0)

    intervals=list(zip(box_low,box_high))
    intervals += [(F(0),w) for w in MASS]
    intervals += [(F(0),box_high[i]*MASS[j]) for i in range(NR) for j in range(NH)]
    intervals += [(F(0),F(1))]
    assert len(rows)==316 and len(intervals)==NVAR==88
    return rows,intervals

def state_check(data):
    assert data['target']=='6/25'
    assert data['old_pair_labels']==[1,2,3,4,6]
    assert [tuple(x) for x in data['old_atom_types']]==TYPES
    assert list(map(rat,data['old_atom_masses']))==MASS
    assert data['R_atom_indices']==R_BINS
    assert list(map(rat,data['root_R_upper']))==R_CAP
    assert sum(MASS)==2 and all(0<=c<=MASS[i] for i,c in zip(R_BINS,R_CAP))
    assert sum(MASS)-sum(R_CAP)==F(3,4)
    for bit in range(5):
        assert sum(MASS[j] for j,t in enumerate(TYPES) if t[bit])==1
    qvalues=[]
    for cuts in combinations(range(5),3):
        q=sum(MASS[i]*MASS[j] for i,j in combinations(range(NH),2)
              if all(TYPES[i][b]!=TYPES[j][b] for b in cuts))
        qvalues.append(q)
    assert qvalues[0]==TARGET and qvalues[1:]==[F(1,4)]*9
    assert data['inequality_order']==[label for label,_,_ in matrix([F(0)]*NR,R_CAP)[0]]

def leaf_check(node,lo,hi):
    rows,bounds=matrix(lo,hi)
    remainder=[F(0)]*NVAR;remainder[OBJECTIVE]=1
    rhs=F(0);seen=set()
    for term in node['multipliers']:
        assert isinstance(term,list) and len(term)==2
        index,y=term;assert isinstance(index,int) and not isinstance(index,bool)
        y=rat(y)
        assert 0<=index<len(rows) and index not in seen and y>=0
        seen.add(index)
        _,row,b=rows[index];rhs+=y*b
        for var,c in row.items():remainder[var]-=y*c
    # Exact residual bound, including every variable; no tolerance and no
    # requirement that rationalized dual multipliers solve exact equalities.
    upper=rhs+sum(max(d*l,d*u) for d,(l,u) in zip(remainder,bounds))
    assert upper==rat(node['upper']), 'incorrect reported leaf bound'
    assert upper<TARGET, 'non-strict or insufficient leaf bound'
    return upper

def check(path):
    raw=Path(path).read_bytes();data=json.loads(raw)
    state_check(data);nodes=data['nodes'];visited=set();uppers=[];splits=empties=0
    def walk(index,lo,hi):
        nonlocal splits,empties
        assert isinstance(index,int) and not isinstance(index,bool) and 0<=index<len(nodes)
        assert index not in visited, 'cycle or reused tree node'
        visited.add(index);node=nodes[index]
        assert list(map(rat,node['lo']))==lo and list(map(rat,node['hi']))==hi
        assert len(lo)==len(hi)==NR and all(F(0)<=l<=u<=c for l,u,c in zip(lo,hi,R_CAP))
        kind=node['kind']
        if kind=='split':
            splits+=1;axis=node['axis'];mid=rat(node['mid'])
            assert isinstance(axis,int) and not isinstance(axis,bool) and 0<=axis<NR
            assert lo[axis]<mid<hi[axis]
            assert isinstance(node['children'],list) and len(node['children'])==2
            left_hi=hi.copy();left_hi[axis]=mid
            right_lo=lo.copy();right_lo[axis]=mid
            walk(node['children'][0],lo,left_hi)
            walk(node['children'][1],right_lo,hi)
        elif kind=='dual_leaf':uppers.append(leaf_check(node,lo,hi))
        elif kind=='rank_empty':
            assert sum(lo)>1, 'rank-empty claim must be strict'
            empties+=1
        else:raise AssertionError('unknown node kind')
    walk(0,[F(0)]*NR,R_CAP.copy())
    assert visited==set(range(len(nodes))), 'unvisited or extraneous node'
    assert len(nodes)==data['total_nodes']==2*splits+1
    assert len(uppers)==data['dual_leaves'] and empties==data['rank_empty_leaves']
    assert max(uppers)==rat(data['maximum_leaf_upper'])
    assert max(uppers)<F(239999,1000000), 'clean displayed bound failed'
    margin=TARGET-max(uppers)
    assert margin==rat(data['minimum_strict_margin'])
    return {'status':'PASS','certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'nodes':len(nodes),'splits':splits,'dual_leaves':len(uppers),'rank_empty_leaves':empties,
            'maximum_leaf_upper':str(max(uppers)),'strict_margin':str(margin),
            'strict_margin_decimal':float(margin),'clean_upper_bound':'239999/1000000',
            'scope':'Conditional exclusion for the fixed five-pair state; arbitrary outside mass permitted; no general upper bound.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('certificate',nargs='?',default='outputs/agent_global_outside_certificate.json');a=p.parse_args()
    print(json.dumps(check(a.certificate),indent=2))
