"""Standalone exact replay for the proposed c_7 <= 3499/4000 proof.

No numerical solver or discovery module is imported. Template budgets are
reconstructed by independent rational Gaussian elimination on the complete
label-price hyperplane arrangement. Every leaf of every tetrahedral cover
is checked. The hand lemmas and rounding argument are in note_644.md.
"""
from fractions import Fraction as F
from itertools import combinations,permutations,product
from pathlib import Path
import json


def minimal(L):return tuple(m for m in sorted(set(L)) if not any(n!=m and n&m==n for n in L))
def blocker(L):return minimal([m for m in range(1,16) if all(m&n for n in L)])


def solve4(rows,rhs):
    A=[list(map(F,row))+[F(b)] for row,b in zip(rows,rhs)]
    for j in range(4):
        pivot=next((i for i in range(j,4) if A[i][j]),None)
        if pivot is None:return None
        A[j],A[pivot]=A[pivot],A[j];d=A[j][j];A[j]=[v/d for v in A[j]]
        for i in range(4):
            if i==j:continue
            d=A[i][j]
            A[i]=[v-d*w for v,w in zip(A[i],A[j])]
    return tuple(row[-1] for row in A)


def static_region(triangle):
    assert len(triangle)==3
    triangle=[tuple(L) for L in triangle]
    for L in triangle:
        assert L and len(L)==len(set(L)) and all(isinstance(m,int) and 1<=m<=15 for m in L)
        assert L==minimal(L)
    assert all(a&b for i,j in combinations(range(3),2) for a,b in product(triangle[i],triangle[j]))
    labs=triangle+[blocker(triangle[2]),blocker(triangle[1]),blocker(triangle[0])]
    # Flooring all label masses and restoring each of six part totals adds
    # at most sum(|labels_p|-1) <= 9 points to any single request.
    assert all(labs) and sum(map(len,labs))<=15
    planes={tuple(int(i==j) for i in range(4)) for j in range(4)}
    for L in labs:
        for a,b in combinations(L,2):
            d=tuple(((a>>i)&1)-((b>>i)&1) for i in range(4))
            if not any(d):continue
            if next(v for v in d if v)<0:d=tuple(-v for v in d)
            planes.add(d)
    vertices=set()
    for three in combinations(sorted(planes),3):
        p=solve4([(1,1,1,1)]+list(three),[1,0,0,0])
        if p is not None and min(p)>=0:vertices.add(p)
    assert vertices
    forms=set()
    for p in vertices:
        cost=[min(sum(p[j] for j in range(4) if m>>j&1) for m in L) for L in labs]
        forms.add((cost[3]+cost[4]+cost[5],cost[0]-cost[3]-cost[4],
                   cost[1]-cost[3]-cost[5],cost[2]-cost[4]-cost[5]))
    return sorted(forms)


def adaptive_regions():
    answer=[]
    for z in range(3):
        x,y=[i for i in range(3) if i!=z];out=[]
        for largest in (x,y):
            row=[F(0)]*4;row[largest+1]=2;row[z+1]=1;out.append(tuple(row))
        row=[F(1,3)]+[F(0)]*3;row[x+1]=row[y+1]=F(2,3);row[z+1]=1;out.append(tuple(row))
        for largest in (x,y):
            row=[F(2,5)]+[F(0)]*3;row[x+1]=row[y+1]=F(2,5)
            row[largest+1]+=F(2,5);row[z+1]=F(3,5);out.append(tuple(row))
        answer.append(out)
    return answer


def unbalanced_regions():
    # Derive each coefficient directly from the five inequalities of
    # Lemma 7.23, without using a discovery module or its stored facets.
    answer=[]
    for z in range(3):
        x,y=[i for i in range(3) if i!=z]
        out=[(F(0),F(1),F(1),F(1))]
        for large,small in ((x,y),(y,x)):
            row=[F(1,3)]+[F(0)]*3
            row[large+1]=1;row[small+1]=F(1,3);row[z+1]=F(2,3)
            out.append(tuple(row))
        out.append((F(2,5),F(3,5),F(3,5),F(3,5)))
        row=[F(1,3)]+[F(2,3)]*3;row[z+1]=1;out.append(tuple(row))
        answer.append(out)
    return answer


def boxes(low,high):
    out=[]
    for perm in permutations(range(3)):
        p=list(low);tet=[tuple(p)]
        for j in perm:p[j]=high[j];tet.append(tuple(p))
        out.append(tet)
    return out


def check_tree(proof,root_tets,regions,budget):
    assert proof['status']=='COVERED' and len(proof['roots'])==len(root_tets)
    nodes=proof['nodes'];seen=set();cache={}
    def at(p,reg):
        key=(p,reg)
        if key not in cache:cache[key]=all(f[0]+sum(a*b for a,b in zip(f[1:],p))<=budget for f in regions[reg])
        return cache[key]
    todo=list(zip(proof['roots'],root_tets))
    while todo:
        idx,tet=todo.pop()
        assert isinstance(idx,int) and 0<=idx<len(nodes) and idx not in seen;seen.add(idx)
        node=nodes[idx]
        if set(node)=={'region'}:
            reg=node['region'];assert isinstance(reg,int) and 0<=reg<len(regions)
            assert all(at(p,reg) for p in tet),(idx,reg,tet)
        else:
            assert set(node) in ({'edge','children'},{'edge','children','weight'})
            a,b=node['edge'];assert isinstance(a,int) and isinstance(b,int) and 0<=a<b<4
            assert len(node['children'])==2
            weight=F(node.get('weight','1/2'));assert 0<weight<1
            mid=tuple((1-weight)*tet[a][j]+weight*tet[b][j] for j in range(3))
            left=list(tet);left[a]=mid;right=list(tet);right[b]=mid
            todo.extend(zip(node['children'],[left,right]))
    assert len(seen)==len(nodes)
    return len(nodes)


def main():
    base=Path(__file__).parent
    data=json.loads((base/'logs/astra_spectrum_cover.json').read_text())
    assert data['status']=='COVERED'
    beta=F(data['budget']);assert beta==F(3499,4000)<F(7,8)
    assert list(map(F,data['interval']))==[F(27,100),F(49,100)]
    regions=[static_region(t) for t in data['static_templates']]+adaptive_regions()
    end=F(27,100);total=0
    for slab in data['slabs']:
        a,b=map(F,slab['interval']);u=F(slab['u']);v=F(slab['v_at_left'])
        assert a==end and a<b<=F(49,100);end=b
        assert u+v==2-beta-a and 1-beta<=u<=1-b and v>=b-a
        assert v<=1-a
        total+=check_tree(slab['proof'],boxes((a,F(0),F(0)),(b,u,v)),regions,beta)
    assert end==F(49,100)
    # Exact arithmetic for the subsequent hand-proved stages.
    low=F(3,20);h=F(49,100);mid=F(27,100)
    assert 0<2-beta-mid-h<=2-beta-low-h<=h
    assert F(127,150)<beta # all three pair intersections <=27r/100
    assert 1-(beta+h)/2<h
    extra=1-2*h;assert 0<=extra<low
    assert F(1,2)+2*low<beta
    new_pair=1-beta+F(1,2)+2*extra
    assert F(1,2)+new_pair/2<beta and 4*low<beta
    assert low<F(7,36) and F(31,36)<beta
    # An additional standalone small-cap certificate, if present.
    capdata=json.loads((base/'logs/astra_small_cap_cover.json').read_text())
    assert capdata['static_templates']==data['static_templates']
    cap=F(capdata['cap']);cb=F(capdata['budget'])
    assert cap==F(377,1000) and cb==F(437,500)
    tet=[(F(0),)*3,(cap,F(0),F(0)),(cap,cap,F(0)),(cap,)*3]
    capnodes=check_tree({'status':'COVERED','roots':[0],'nodes':capdata['nodes']},[tet],regions,cb)
    print('PASS:',len(data['slabs']),'gap-free slabs;',total,'exact cover nodes;',
          len(data['static_templates']),'independently reconstructed static templates; all global-stage constants checked')
    print('PASS: small-cap certificate;',capnodes,'nodes; cap 377/1000 at budget 437/500')
    print('CERTIFICATE SUPPORTS: c_7 <= 3499/4000, conditional on the hand lemmas and rounding proof in note_644.md')

    # Stronger complete cover using the unbalanced first adaptive cut.
    strong=json.loads((base/'logs/astra_spectrum_unbalanced_87_100_19_40.json').read_text())
    beta=F(strong['budget']);assert beta==F(87,100)
    assert strong['status']=='COVERED' and strong['adaptive_version']==2
    assert strong['static_templates']==data['static_templates']
    regions2=regions+unbalanced_regions()
    critical=(F(7,18),F(10,27),F(1,54))
    def point_budget(regions,p):
        return min(max(f[0]+sum(a*b for a,b in zip(f[1:],p)) for f in fs) for fs in regions)
    assert point_budget(regions,critical)==F(47,54)
    assert point_budget(regions2,critical)==F(13,15)
    low=F(9,50);h=F(19,40);mid=F(27,100)
    assert list(map(F,strong['interval']))==[mid,h]
    end=mid;total=0
    for slab in strong['slabs']:
        a,b=map(F,slab['interval']);u=F(slab['u']);v=F(slab['v_at_left'])
        assert a==end and a<b<=h;end=b
        assert u+v==2-beta-a and 1-beta<=u<=1-b and v>=b-a and v<=1-a
        total+=check_tree(slab['proof'],boxes((a,F(0),F(0)),(b,u,v)),regions2,beta)
    assert end==h
    assert 0<low<mid<h<F(1,2) and low<=F(7,36)
    assert 0<2-beta-mid-h<=2-beta-low-h<=h and h<=1-mid
    assert F(127,150)<beta and 1-(beta+h)/2<h
    extra=1-2*h;assert 0<=extra<low
    assert F(1,2)+2*low<beta
    new_pair=1-beta+F(1,2)+2*extra
    assert F(1,2)+new_pair/2<beta and 4*low<beta
    assert F(31,36)<beta
    # All finite rounding inequalities below are weakest at r=1000.
    r=F(1000)
    assert beta*r+5<r
    assert (F(1,2)+2*low)*r+2<=beta*r+4
    assert (F(1,2)+new_pair/2)*r+F(3,2)<beta*r+10
    assert F(31,36)*r+3<beta*r+10
    print('PASS: strengthened cover;',len(strong['slabs']),'gap-free slabs;',total,
          'exact nodes; unbalanced adaptive regions; all global and integer rounding constants checked')
    print('CERTIFICATE SUPPORTS: c_7 <= 87/100, with f(r,7) <= ceil(87r/100)+10 for r>=1000, conditional on the hand lemmas in note_644.md')


if __name__=='__main__':main()
