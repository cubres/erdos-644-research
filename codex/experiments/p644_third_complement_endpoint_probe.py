"""Bounded endpoint probe for the parent's complement-shaped third response.

Uses the proved four-major-class reduction and a linear formula for all
partial masses within a declared support. Does not check seven-row
robustness, which the independent root certificate handles.
"""
from itertools import combinations
from pathlib import Path
import json
import argparse


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--b',type=int,default=10)
    args=parser.parse_args(); b=args.b
    source=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text())
    affine=source['weights']; weights=[a*b+c for a,c in affine]
    masks=source['masks']; n=len(weights)
    G=set(source['G']); H=set(source['H']); E=G^H; B={1,11,13}
    major={0,2,3,5}; small=sorted(E-major)
    def bits(items):return sum(1<<i for i in items)
    eb=bits(E); bb=bits(B)
    def mass(z):
        total=0
        while z:
            bit=z&-z; total+=weights[bit.bit_length()-1];z^=bit
        return total
    def union_neighbors(z,nb):
        result=0
        while z:
            bit=z&-z;result|=nb[bit.bit_length()-1];z^=bit
        return result
    stats={'five_tuples':0,'four_major_neighbor_min':None,'support_cases':0}
    best=None; candidate=None
    for rows in combinations(range(9),5):
        full=sum(1<<r for r in rows)
        nb=[bits(j for j in range(n) if (masks[i]|masks[j])&full==full) for i in range(n)]
        eligible=bits(i for i,v in enumerate(nb) if v)
        major_force=mass(union_neighbors(bb|bits(major),nb))
        stats['five_tuples']+=1
        stats['four_major_neighbor_min']=min(stats['four_major_neighbor_min'] or major_force,major_force)
        if union_neighbors(bb,nb)==(1<<n)-1:continue
        for q in sorted(major):
            # Dropping more major classes is impossible for b>=1 except
            # trivial b=0, which the caller must not use.
            assert 2*(33*b-1)>37*b
            baseline_force=mass(union_neighbors(bb|bits(major-{q}),nb))
            if baseline_force>111*b:continue
            remaining=37*b-weights[q]
            for count in range(6):
                for zero_small in combinations(small,count):
                    zero=(q,)+zero_small
                    zero_mass=sum(weights[i] for i in zero)
                    if zero_mass>37*b:continue
                    stats['support_cases']+=1
                    support=bb|(eb&~bits(zero))
                    neighbors=union_neighbors(support,nb)
                    paid=(support&eligible)&~neighbors
                    capacity=(paid&eb)
                    residual=37*b-zero_mass
                    lower=mass(neighbors)+mass(paid)-min(residual,mass(capacity))
                    record={'rows':list(rows),'zero_types':list(zero),'lower':lower,
                            'neighbor_mass':mass(neighbors),'paid_mass':mass(paid),
                            'residual_cut':residual,'paid_cut_capacity':mass(capacity)}
                    if best is None or lower<best['lower']:best=record
                    if lower>=111*b:continue
                    # Realize the relaxed minimum, allowing a new zero class;
                    # recomputation below can only decrease endpoint mass.
                    cut=[0]*n
                    for i in zero:cut[i]=weights[i]
                    left=residual
                    order=[i for i in sorted(E) if capacity>>i&1]
                    order += [i for i in sorted(E) if not(capacity>>i&1)]
                    for i in order:
                        take=min(left,weights[i]-cut[i]);cut[i]+=take;left-=take
                    assert left==0 and sum(cut)==37*b
                    jmass=[weights[i] if i in B else weights[i]-cut[i] if i in E else 0 for i in range(n)]
                    jsupport=bits(i for i,v in enumerate(jmass) if v)
                    actualnb=union_neighbors(jsupport,nb)
                    endpoint=mass(actualnb)+sum(jmass[i] for i in range(n) if eligible>>i&1 and not(actualnb>>i&1))
                    if endpoint<111*b:
                        candidate={**record,'b':b,'X_masses':cut,'J_masses':jmass,
                                   'endpoint':endpoint,'target':111*b,
                                   'J_size':sum(jmass)}
                        break
                if candidate:break
            if candidate:break
        if candidate:break
    out={'b':b,'stats':stats,'best_lower':best,'candidate':candidate,
         'scope':'Endpoint optimization for complement-shaped J only; not universal response forcing.'}
    Path('outputs/agent_third_complement_endpoint_probe.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
