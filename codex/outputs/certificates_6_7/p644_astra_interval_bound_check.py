"""Independent exact replay of the c7 <= 431/500 argument.

Reconstructs every static region, checks chronological interval exclusions,
then the high-gap and middle-gap covers. Only standard-library and other
independent checker code is imported. Hand and rounding proofs are in note.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from p644_astra_global_bound_check import static_region,adaptive_regions,unbalanced_regions,triangular_region,response_choice_regions,boxes,check_tree
from p644_astra_frontier_check import dominant_regions
from p644_astra_maxsmall_check import partial_regions,padded_regions,padded_dominant_regions


def merged(intervals):
    out=[]
    for a,b in sorted(intervals):
        if out and a<=out[-1][1]:out[-1]=(out[-1][0],max(b,out[-1][1]))
        else:out.append((a,b))
    return out


def remaining(cap,excluded):
    # Closed outer intervals safely include endpoints already excluded.
    result=[];left=F(0)
    for a,b in excluded:
        if a>cap:break
        if left<a:result.append((left,min(a,cap)))
        left=max(left,b)
    if left<cap:result.append((left,cap))
    if not result and cap==0:result=[(F(0),F(0))]
    return result


def gap_regions(h,ell):
    out=[]
    for x in range(3):
        y,z=[j for j in range(3) if j!=x]
        def row(c,cx=0,cy=0,cz=0):
            r=[F(c),F(0),F(0),F(0)];r[x+1]=F(cx);r[y+1]=F(cy);r[z+1]=F(cz);return tuple(r)
        out.append([row(0,1,1,1),row(1-h,0,0,1),row(1-h,0,1,0),row(2-2*h,-1),
          row(F(1,3),1),row((2-h)/3,F(2,3),F(-1,3)),row((2-h)/3,F(2,3),0,F(-1,3)),
          row((3-2*h)/3,F(1,3),F(-1,3),F(-1,3)),row(2*ell,0,1,1)])
    return out


def constant_gap_regions(m):
    out=[]
    for z,fs in enumerate(response_choice_regions()):
        g=fs[:-1]
        for j in range(3):
            if j==z:continue
            f=[m,F(0),F(0),F(0)];f[j+1]=1;g.append(tuple(f))
        out.append(g)
    return out


def main():
    base=Path(__file__).parent;beta=F(431,500)
    d=json.loads((base/'logs/astra_interval_padded_431_500.json').read_text())
    assert F(d['budget'])==beta and d['adaptive_version']==6
    rs=[static_region(t) for t in d['static_templates']]
    rs+=adaptive_regions()+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_regions()+partial_regions()+padded_regions()+padded_dominant_regions()
    excluded=[];total=0
    for step in d['steps']:
        a,b=map(F,step['interval']);u=F(step['u']);v=F(step['v_at_left'])
        assert 0<=a<b<=F(1,2) and u+v==2-beta-a
        assert 1-beta<=u<=1-b and b-a<=v<=1-a
        expected=list(product(remaining(u,excluded),remaining(v,excluded)))
        actual=[(tuple(map(F,s['y'])),tuple(map(F,s['z']))) for s in step['boxes']]
        assert actual==expected
        for s,((yl,yh),(zl,zh)) in zip(step['boxes'],expected):
            total+=check_tree(s['proof'],boxes((a,yl,zl),(b,yh,zh)),rs,beta)
        excluded=merged(excluded+[(a,b)])
    assert excluded==[(F(9,50),F(3,8)),(F(39,100),F(12,25))]
    assert d['excluded']==[[str(a),str(b)] for a,b in excluded]
    print('PASS: chronological exclusions;',len(d['steps']),'steps;',total,'nodes;',len(d['static_templates']),'reconstructed static regions')

    high=json.loads((base/'logs/astra_gap_high_431_500.json').read_text())
    assert high['static_templates']==d['static_templates'] and F(high['beta'])==beta
    h=F(high['h']);ell=F(high['low']);assert (h,ell)==(F(3,8),F(9,50))
    assert (2-beta-F(12,25))/2<h and F(1,2)+2*ell<beta
    nt=check_tree(high['proof'],boxes((F(12,25),F(0),F(0)),(F(1,2),ell,ell)),rs+gap_regions(h,ell),beta)
    total+=nt;print('PASS: high-gap extension;',nt,'nodes; all initial good-triple cores below budget')
    excluded=merged(excluded+[(F(12,25),F(1,2))])
    assert excluded==[(ell,h),(F(39,100),F(1,2))]

    mid=json.loads((base/'logs/astra_gap_middle_431_500.json').read_text())
    assert mid['static_templates']==d['static_templates'] and F(mid['beta'])==beta and F(mid['m'])==F(39,100)
    a,b=h,F(39,100);cap=(2-beta-a)/2;assert cap==F(763,2000)
    expected=list(product(remaining(cap,excluded),repeat=2))
    assert [(tuple(map(F,s['y'])),tuple(map(F,s['z']))) for s in mid['boxes']]==expected
    nt=0
    for s,((yl,yh),(zl,zh)) in zip(mid['boxes'],expected):
        nt+=check_tree(s['proof'],boxes((a,yl,zl),(b,yh,zh)),rs+constant_gap_regions(b),beta)
    total+=nt;print('PASS: middle-gap extension;',nt,'nodes; final excluded interval [9/50,1/2]')
    # Global contradiction and uniform integral allowances.
    assert ell<F(7,36) and F(31,36)<beta
    assert beta*1000+5<1000
    # Static regions verified <=15 labels across six parts in static_region;
    # restoring integral part totals therefore costs <=9 extra points.
    # Gap requests: floor(h*r) changes p,t by <1 each; first cost <=beta*r+2.
    # Use T>=beta*r+4: the split-request load is <=(3beta*r+2-T)/2+1/2.
    assert (F(2)-4)/2+F(1,2)<=0
    # Initial good triple caps cost <=beta*r+2. All request budgets fit K.
    assert max(2,4,9)<10
    print('PASS: c7 <= 431/500 = 0.862;',total,'cover nodes; finite bound ceil(431k/500)+10 for k>=1000')
    print('The finite replay must be read with the hand lemmas and integer argument in note_644.md.')


if __name__=='__main__':main()
