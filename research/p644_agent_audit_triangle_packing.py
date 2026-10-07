"""Exact auxiliary checks of the hand three-job packing lemma."""
import json

def pack(k,b,c,p):
    assert 0<=c<=b and 4*b<=k and all(x>=0 for x in p)and sum(p)<=k
    H=k-2*b;two=k-3*b+c
    out=[[0]*3 for _ in range(3)]
    if max(p)<=H:
        for j in range(3):out[j][j]=p[j]
        return out
    i=max(range(3),key=lambda j:p[j]);rest=sorted((j for j in range(3)if j!=i),key=lambda j:p[j])
    j,l=rest;R=p[j]+p[l]
    out[0][i]=H;out[1][i]=p[i]-H
    if R<=two:
        out[2][j]=p[j];out[2][l]=p[l]
    else:
        out[2][j]=p[j]
        z=min(p[l],two-out[1][i]);assert z>=0
        out[1][l]=z;out[2][l]=p[l]-z
    return out

def check(k,b,c,p):
    rows=pack(k,b,c,p);B=b-c;T=k-b
    assert [sum(row[j]for row in rows)for j in range(3)]==list(p)
    for row in rows:
        assert all(x>=0 for x in row)
        assert c+B*sum(x>0 for x in row)+sum(row)<=T,(k,b,c,p,rows)

if __name__=='__main__':
    count=0
    for k in range(1,65):
        b=k//4
        for c in range(b+1):
            for p0 in range(k+1):
                for p1 in range(k-p0+1):
                    p=(p0,p1,k-p0-p1);check(k,b,c,p);count+=1
    print(json.dumps({'status':'PASS','integer_instances':count,
                     'scope':'Auxiliary verification of the separately supplied hand packing proof.'},indent=2))
