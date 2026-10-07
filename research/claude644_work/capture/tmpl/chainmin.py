import sys
exec(open('closed2.py').read().split('leaves=0\ndef rec')[0])
def valid(W,S,chain):
    viol=[]
    for cand in chain[:-1]:
        fl=[f for f in cand_facets(*cand) if (lambda mm: mm is not None and mm>1e-9)(maxeps(W,S,viol+[f]))]
        if len(fl)!=1: return False
        viol=viol+fl
    m=maxeps(W,S,viol)
    if m is None or m<=1e-9: return True
    last=chain[-1]
    fl=[f for f in cand_facets(*last) if (lambda mm: mm is not None and mm>1e-9)(maxeps(W,S,viol+[f]))]
    return len(fl)==0
def minimize(W,S,chain):
    changed=True
    while changed:
        changed=False
        for i in range(len(chain)):
            c2=chain[:i]+chain[i+1:]
            if c2 and valid(W,S,c2): chain=c2; changed=True; break
    return chain
L_,A_,B_,C_=2,3,4,5
chain=[(21,4,3),(1,4,2),(1,5,2),(21,5,2),(41,2,4),(19,2,2),(19,3,3),(19,4,4),(19,5,5),(20,2,2),(20,3,3),(20,4,4),(20,5,5),(1,3,2),(1,3,4),(1,3,5),(2,2,3),(2,2,4),(2,2,5),(2,4,3),(2,5,3),(9,3,4),(9,3,5),(10,4,3),(10,5,3),(21,4,2),(9,4,2),(21,2,4),(9,4,3),(39,3,4)]
W,S=domain((True,False))
print('valid',valid(W,S,chain))
m=minimize(W,S,chain); print('minimized',len(m),m)
