#!/usr/bin/env python3
"""Exact affine regions for one full-budget response to the 3-minimum barrier.

Discovery output records rational polygons; this program is not by itself a
claim of a global three-part theorem.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
X = (F(106), F(106), F(112))
ZERO = (F(0), F(0), F(0))
T = [tuple((F(0), F(0), F(v)) for v in row)
     for row in ((71,69,0),(69,71,0),(65,0,75))]
T += [((F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(-1),F(-1),F(140)))]
DOMAIN = [(F(0),F(28)),(F(0),F(106)),(F(1),F(106)),(F(1),F(27))]

def form(coord, terms, cap=1):
    result = [F(0),F(0),-F(cap)*X[coord]]
    for role, coeff in terms:
        for j in range(3): result[j] += F(coeff)*T[role][coord][j]
    return tuple(result)

def val(f,p): return f[0]*p[0]+f[1]*p[1]+f[2]

def clip(poly, f):
    if not poly: return []
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        v,w=val(f,p),val(f,q)
        if v<=0: out.append(p)
        if (v<0<w) or (w<0<v):
            lam=v/(v-w)
            out.append(tuple(p[j]+lam*(q[j]-p[j]) for j in range(2)))
    return list(dict.fromkeys(out))

def area(poly):
    return abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1])))/2

def templates():
    data=json.load(open(ROOT/'heavy/astra_support_capacity_minimal.json'))
    for k,fun in enumerate(data['minimal_functions']):
        vertices=[tuple(map(F,v)) for v in fun['vertices']]
        for a,b in product(range(4),repeat=2):
            yield ('P',k,a,b),[form(i,[(a,u),(b,v)]) for i in range(3) for u,v in vertices]
    for a,b,c in product(range(4),repeat=3):
        yield ('T',a,b,c),[f for i in range(3) for f in
          (form(i,[(a,2),(b,1)],2),form(i,[(a,2),(c,1)],2),
           form(i,[(b,2),(c,1)],2),form(i,[(a,4),(b,2),(c,1)],4))]
    for d,a,b,c in product(range(4),repeat=4):
        yield ('V4',d,a,b,c),[f for i in range(3) for f in
          (form(i,[(a,1),(b,1),(c,1)],2),
           form(i,[(d,2),(b,1),(c,1)],2),
           form(i,[(d,4),(a,1),(b,1),(c,1)],4))]
    mixed=json.load(open('work/paper_push/three_cert/balanced_1321_template.json'))
    vertices=[tuple(map(F,v)) for v in mixed['maximal_projected']]
    for roles in product(range(4),repeat=4):
        yield ('M1321',)+roles,[form(i,list(zip(roles,v))) for i in range(3) for v in vertices]
    # The single-type pencil lemma is conditional on the available tau>105.
    for a in range(4):
        yield ('pencil',a),[form(i,[(a,3)],2) for i in range(3)]

def main():
    kept=[]
    for key,fs in templates():
        p=DOMAIN
        for f in fs:
            p=clip(p,f)
            if not p: break
        if p and area(p)>0:
            kept.append((key,fs,p))
    print('Nonempty full-dimensional template regions:',len(kept),flush=True)
    # A coarse mesh selects likely useful regions; the conclusion is determined
    # solely by exact polygon subtraction below, not by this discovery mesh.
    points=[(F(a,2),F(b)) for a in range(3) for b in range(27,107)
            if F(b)+F(a,2)>=28]
    remaining=set(range(len(points))); selected=[]
    while remaining:
        scored=[]
        for key,fs,p in kept:
            covered={j for j in remaining if all(val(f,points[j])<=0 for f in fs)}
            scored.append((len(covered),key,fs,p,covered))
        score,key,fs,p,cov=max(scored,key=lambda z:z[0])
        if not score: break
        selected.append((key,fs,p));remaining-=cov
        print('SELECT',key,'mesh remaining',len(remaining),flush=True)
    if remaining:
        print('UNCOVERED SAMPLE',points[min(remaining)],flush=True)
    pieces=[DOMAIN]
    for key,fs,p in selected:
        new=[]
        for piece in pieces:
            inside=piece
            for f in fs:
                if all(val(f,v)<=0 for v in inside):
                    continue
                outside=clip(inside,tuple(-c for c in f))
                if outside and area(outside)>0: new.append(outside)
                inside=clip(inside,f)
                if not inside or not area(inside):break
        pieces=new
    print('Exact uncovered polygons:',len(pieces),'area:',sum(map(area,pieces)),flush=True)
    if pieces: print('FIRST UNCOVERED',pieces[0],flush=True)
    payload={'selected':[{'key':key,'forms':fs,'polygon':p} for key,fs,p in selected],
             'uncovered':pieces}
    Path('outputs/paper_push_response_geometry.json').write_text(json.dumps(payload,default=str,indent=2))

if __name__=='__main__':main()
