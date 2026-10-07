"""Exact bad tuple for the genuinely interval-valued two-part example."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json


def realization(s,t):
    lines=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    assert all(len(set(a)&set(b))==1 for i,a in enumerate(lines) for b in lines[i+1:])
    z=max(F(0),t-s/2);x=max(F(0),s/2-z/2);y=s
    masses={}
    for line in lines:
        mask=127-sum(1<<j for j in line);nb=sum(bool(mask&(1<<j)) for j in [0,1])
        mass=[x,y/4,z/2][nb]
        if mass:masses[mask]=mass
    for j in range(7):
        target=t if j<2 else s
        excess=sum(v for mask,v in masses.items() if mask>>j&1)-target
        assert excess>=0
        for mask in sorted(list(masses),reverse=True):
            if not(mask>>j&1) or not excess:continue
            take=min(masses[mask],excess);masses[mask]-=take;excess-=take
            new=mask^(1<<j);masses[new]=masses.get(new,F(0))+take
        assert excess==0
    return {str(m):str(v) for m,v in sorted(masses.items()) if v}


def main():
    capacities=[F(1,2),F(181,122)];s,t=F(1,10),F(41,122)
    parts=[realization(s,t),realization(1-s,1-t)]
    scale=1
    for part in parts:
        for value in part.values():
            d=F(value).denominator;scale=scale*d//gcd(scale,d)
    out={'capacities':list(map(str,capacities)),'intervals':[['0','29/244'],['41/122','41/122']],
         'row_types':[str(t)]*2+[str(s)]*5,'parts':parts,'integral_scale':scale,
         'transversal_coefficient':'187/244','two_type_upper':'79/122'}
    Path('logs/astra_two_intervals_example.json').write_text(json.dumps(out,indent=2))
    print('Saved exact tuple; rank',scale,'after scaling.',flush=True)


if __name__=='__main__':main()
