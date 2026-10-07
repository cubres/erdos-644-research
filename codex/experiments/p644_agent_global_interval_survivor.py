"""Exact interval survivor, plus the specified third whole-cell request.

The rational construction works for 1/8 <= c < 1/4.  It is a local
method obstruction; its finite family still has transversal number 2.
"""
from fractions import Fraction as F
import itertools
import json
from pathlib import Path


def base_atoms(c):
    out = []
    def add(old,g,j,w):
        if w:
            assert w > 0
            out.append((tuple(map(int,old))+(g,j),w))
    for old in ('000','011'):
        for g,j in itertools.product(range(2),repeat=2):
            add(old,g,j,F(1,8))
    for old in ('100','111'):
        add(old,1,0,F(1,8))
        add(old,1,1,c-F(1,8))
    add('101',0,1,F(1,4))
    add('101',1,1,F(1,4)-c)
    add('110',0,0,F(1,8)+c/2)
    for g,j in ((0,1),(1,0),(1,1)):
        add('110',g,j,F(1,8)-c/2)
    return out


def profile(atoms,pairs):
    eligible=set()
    q=F(0)
    for i,(s,x) in enumerate(atoms):
        for j in range(i+1,len(atoms)):
            t,y=atoms[j]
            if all(s[p]!=t[p] for p in pairs):
                q+=x*y
                eligible.update([i,j])
    return q,sum((atoms[i][1] for i in eligible),F(0))


def with_a_flip(atoms):
    return [(s+(1-s[3] if s[:3]==(0,0,0) else s[3],),w) for s,w in atoms]


def with_seventh_pair(atoms):
    def in_new(s):
        return s[:3]==(0,0,0) or (s[:3] in ((1,0,1),(1,1,0)) and s[3]==0)
    return [(s+(0 if in_new(s) else 1,),w) for s,w in atoms]


def check(atoms,c,global_pair=True,p_floor=None):
    n=len(atoms[0][0])
    for p in range(n):
        for bit in range(2):
            assert sum(w for s,w in atoms if s[p]==bit)==1
    values=[]
    for ps in itertools.combinations_with_replacement(range(n),3):
        q,p=profile(atoms,ps)
        assert q>=c,(ps,q,c)
        assert p>F(3,4),(ps,p,c)
        if p_floor is None:
            assert p>=1+2*c,(ps,p,c)
        else:
            assert p>=p_floor,(ps,p,c)
        values.append({'pairs':[i+1 for i in ps], 'Q':str(q),'P':str(p)})
    globalq,globalp=profile(atoms,tuple(range(n)))
    if global_pair:
        assert globalq>0
    return values,globalq,globalp


def all_six_and_seven(atoms):
    n=2*len(atoms[0][0])
    masks=[sum(1<<(2*i+b) for i,b in enumerate(s)) for s,w in atoms]
    unions=[(i,j,masks[i]|masks[j]) for i in range(len(atoms))
            for j in range(i,len(atoms))]
    seven_count=0
    for rs in itertools.combinations(range(n),7):
        target=sum(1<<r for r in rs)
        assert any(target&u==target for i,j,u in unions),rs
        seven_count+=1
    best=F(3)
    bestrows=None
    bestpairs=None
    for rs in itertools.combinations(range(n),6):
        target=sum(1<<r for r in rs)
        el=set()
        pairs=[]
        for i,j,u in unions:
            if target&u==target:
                el.update((i,j));pairs.append([i,j])
        p=sum((atoms[i][1] for i in el),F(0))
        if p<best:
            best,bestrows,bestpairs=p,[r+1 for r in rs],pairs
    target=(1<<n)-1
    cover=None
    for size in range(1,4):
        for indices in itertools.combinations(range(len(atoms)),size):
            mask=0
            for i in indices:mask|=masks[i]
            if mask==target:
                cover=list(indices);break
        if cover is not None:break
    assert cover is not None
    return {'all_seven_subsets_checked':seven_count,'minimum_unpaired_P6':str(best),
            'minimizing_six_rows':bestrows,'minimizing_six_pair_graph':bestpairs,
            'transversal_number':len(cover),'transversal_atom_indices':cover}


def main():
    c=F(6,25)
    a=base_atoms(c)
    values,q,p=check(a,c)
    expected = [c,F(1,4),F(1,4),F(1,4),F(1,4),F(1,4),F(1,4),
                F(7,32)+c/2,F(9,32)-c/8,F(9,32)-c/8]
    actual=[profile(a,ps)[0] for ps in itertools.combinations(range(5),3)]
    assert actual==expected
    assert q==c/4 and p==F(1,2)+2*c
    b=with_a_flip(a)
    values6,q6,p6=check(b,c)
    assert q6==c/8 and p6==F(1,4)+c
    # The third request is A_G, both old small cells, and H in101/110.
    def deleted(s):
        old=s[:3]
        return (old==(0,0,0) and s[3]==0) or old in ((1,0,0),(1,1,1)) or \
               (old in ((1,0,1),(1,1,0)) and s[3]==1)
    assert sum(w for s,w in b if deleted(s))==F(3,4)
    assert all(s[5]==1 for s,w in b if deleted(s))
    d=with_seventh_pair(b)
    values7,q7,p7=check(d,c,global_pair=False,p_floor=F(3,4))
    assert q7==p7==0
    def deleted4(s):
        old=s[:3]
        return (old==(0,1,1) and s[3]==0) or old in ((1,0,0),(1,1,1)) or \
               (old in ((1,0,1),(1,1,0)) and s[3]==1)
    assert sum(w for s,w in d if deleted4(s))==F(3,4)
    assert all(s[6]==1 for s,w in d if deleted4(s))
    all_rows=[all_six_and_seven(v) for v in (a,b,d)]
    assert [v['minimum_unpaired_P6'] for v in all_rows]==['37/25','31/25','99/100']
    # Interval identities are also checked at further rational parameters;
    # the accompanying report provides the symbolic mass table and formulas.
    for c2 in (F(1,8),F(3,20),F(1,5),F(6,25),F(249,1000)):
        check(base_atoms(c2),c2)
        check(with_a_flip(base_atoms(c2)),c2)
    out={'status':'EXACT LOCAL SURVIVOR, NOT A LARGE-TAU COUNTEREXAMPLE',
         'c':str(c),'interval':'1/8 <= c < 1/4',
         'five_pair_atoms':[{'bits':list(s),'mass':str(w)} for s,w in a],
         'five_pair_profiles':values,'five_pair_global_Q':str(q),'five_pair_global_P':str(p),
         'six_pair_atoms':[{'bits':list(s),'mass':str(w)} for s,w in b],
         'six_pair_profiles':values6,'six_pair_global_Q':str(q6),'six_pair_global_P':str(p6),
         'seven_pair_atoms':[{'bits':list(s),'mass':str(w)} for s,w in d],
         'seven_pair_profiles':values7,'seven_pair_global_Q':str(q7),'seven_pair_global_P':str(p7),
         'third_avoidance_mass':'3/4','fourth_avoidance_mass':'3/4',
         'all_row_checks':all_rows}
    Path('outputs/agent_global_interval_survivor.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if 'atoms' not in k and 'profiles' not in k},indent=2))
    print('New triples involving pair6:')
    for v in values6:
        if 6 in v['pairs'] and len(set(v['pairs']))==3:
            print(v)


if __name__=='__main__':
    main()
