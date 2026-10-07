"""Independent standard-library replay of formal Johnson distributions."""
import json
from math import comb
from fractions import Fraction
from pathlib import Path

def C(n,r):return comb(n,r) if 0<=r<=n else 0

def P(k,i,j):
    # Use the alternative primary-source binomial formula to replay the producer.
    return sum((-1)**(i-h)*C(k-h,i-h)*C(k-j,h)*C(k+h-j,h) for h in range(i+1))

def check(path):
    data=json.loads(Path(path).read_text());k,T,M=[data[x]for x in ('k','T','M')]
    assert data['status']=='sat'
    a=[Fraction(s) for s in data['A']]
    allowed=lambda r:r<=M or T-M<=r<=k-T+M or r>=k-M
    assert len(a)==k+1 and a[0]==a[k]==1
    assert all(a[i]==a[k-i] and 0<=a[i]<=C(k,i)**2 for i in range(k+1))
    assert all(allowed(k-i) or a[i]==0 for i in range(k+1))
    for j in range(k+1):
        assert sum(a[i]*Fraction(P(k,i,j),C(k,i)**2) for i in range(k+1))>=0
    for j in range(T+1):
        assert sum(a[i]*C(k-i,j)*C(i,T-j) for i in range(k+1))>=C(k,j)*C(k,T-j)
    lower=Fraction(C(2*k,T),C(k,T))
    assert sum(a)>=lower
    return {'k':k,'T':T,'M':M,'status':'EXACT_FEASIBLE',
            'formal_size':str(sum(a)),'cofinal_lower':str(lower),
            'size_divided_by_lower':float(sum(a)/lower)}

if __name__=='__main__':
    root=Path(__file__).parent/'logs'
    print(json.dumps([check(root/name) for name in [
        'astra_agent_audit_johnson_cofinal_20_15_7.json',
        'astra_agent_audit_johnson_cofinal_40_30_13.json',
        'astra_agent_audit_johnson_cofinal_40_31_13.json']],indent=2))
