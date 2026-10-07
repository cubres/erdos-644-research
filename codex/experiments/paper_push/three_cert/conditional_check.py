"""Exact checker allowing a witnessed restricted class outside balanced regimes.

The earlier revealed pattern must have i heavy and j light. REQ types witness
this directly. A MIN/RMIN limit's stored pattern comes from an actual fixed-
pattern subsequence, which also witnesses nonemptiness of that restricted class.
The infimum can therefore be revealed by the same closedness argument as usual.
"""
import sys,json
from fractions import Fraction as F
SRC='/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c'
sys.path.insert(0,SRC)
import b4core as bc
import check5 as old
from strict_types import install

original_chk=old.chk
enabled=False
patterns=[]
incoming={}
def core_chk(node,C,E,nt):
    if len(patterns)!=nt:old.fail('semantic pattern stack does not match revealed types')
    if node['k'] in ('MIN','RMIN','REQ'):
        for p,kid in node['kids']:incoming[id(kid)]=tuple(p)
    if node['k']!='RMIN' or old.REGIME[0] is True:
        return original_chk(node,C,E,nt)
    if not enabled:old.fail('conditional RMIN extension not declared')
    i,j=node['i'],node['j']
    if not(0<=i<3 and 0<=j<3 and i!=j):old.fail('RMIN index')
    # Use only the original semantic pattern labels on MIN/RMIN/REQ edges.
    # Arbitrary later facet inequalities cannot fabricate a class witness.
    witness=any(p[i] and not p[j] for p in patterns)
    if not witness:old.fail('RMIN without an earlier restricted-class witness')
    pats=[tuple(p) for p,_ in node['kids']]
    if sorted(pats)!=sorted(p for p in bc.PATS if p[i] and not p[j]):old.fail('RMIN patterns')
    tc,te=bc.type_region(nt)
    for pat,kid in node['kids']:
        chk(kid,C+tc+bc.pattern_region(nt,pat),
            E+te+[({bc.T(nt,i):F(1),bc.H(i,j):F(-1)},F(0))],nt+1)

def chk(node,C,E,nt):
    p=incoming.get(id(node))
    if p is not None:patterns.append(p)
    try:return core_chk(node,C,E,nt)
    finally:
        if p is not None:patterns.pop()

old.chk=chk
for path in sys.argv[1:]:
    D=json.load(open(path));ext=D.get('extensions',[])
    enabled='conditional-rmin' in ext
    if 'strict-types' in ext:install()
    if D.get('balanced') not in (True,'unb01','unb02','unb12'):old.fail('unknown regime')
    lo=[F(v) for v in D['box'][0]];hi=[F(v) for v in D['box'][1]]
    C,E=bc.base_region(D['balanced'],D['sorted'],(lo,hi),D.get('excess',False))
    old.N['leaf']=0;old.N['ineq']=0;old.REGIME[0]=D['balanced']
    patterns.clear();incoming.clear()
    chk(D['tree'],C,E,0)
    print('PASS',path,'extensions',ext,'leaves',old.N['leaf'],'inequalities',old.N['ineq'])
