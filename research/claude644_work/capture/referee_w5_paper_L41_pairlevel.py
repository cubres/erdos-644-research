# Referee w5 (paper): pair-level exhaustive check of Lemma 5.2 (two large pair cells) as written,
# for all small r, m<=r/4, cells, T, and all response profiles of I consistent with the gap
# (|G&I|,|H&I| <= m after the lemma's derived bound <= r/2 is asserted).
import itertools, sys
from math import ceil
from referee_w5_paper_sec3_pairlevel import check_close, Fail, take
def run(R):
    n=0
    for r in range(4,R+1):
        hr=(r+1)//2  # ceil(r/2)
        for m in range(0,r//4+1):
            for x in range(r//2+1,r+1):
              for b in range(r//2+1,r+1):
                for y,z,a,c in itertools.product(range(m+1),repeat=4):
                    if x+y+c>r or x+z+a>r or y+z+b>r or b+a+c>r: continue
                    P=lambda t,k:[(t,i) for i in range(k)]
                    X=P('X',x);B=P('B',b);Y=P('Y',y);Z=P('Z',z);A=P('A',a);C=P('C',c)
                    PE=P('PE',r-x-y-c);PF=P('PF',r-x-z-a);PG=P('PG',r-y-z-b);PH=P('PH',r-b-a-c)
                    E=set(X+Y+C+PE);F=set(X+Z+A+PF);G=set(Y+Z+B+PG);H=set(B+A+C+PH)
                    for T in range(0,r+1):
                        if not (T>=hr+2*m and T>=x+m and 3*T>=2*x+b+hr+2*m): continue
                        s=y+z;t=a+c
                        p=hr-min(s,t); q=T-hr-max(s,t)
                        B0=take(B,p);X0=take(X,q)
                        Dreq=set(Y+Z+A+C+B0+X0)
                        if len(Dreq)!=T: raise Fail('I req size')
                        regs=[[u for u in X if u not in Dreq],[u for u in B if u not in Dreq],PE,PF,PG,PH]
                        for cnt in itertools.product(*[range(len(g)+1) for g in regs]):
                            if sum(cnt)>r: continue
                            I=set()
                            for g,k in zip(regs,cnt): I|=set(g[:k])
                            I|={('out',i) for i in range(r-len(I))}
                            if len(G&I)*2>r or len(H&I)*2>r: raise Fail('derived <=r/2 fails')
                            if len(G&I)>m or len(H&I)>m: continue  # gap
                            BI=[u for u in B if u in I]
                            rest=[u for u in B if u not in I]
                            nb1=min(b,T-x)
                            if nb1<len(BI): raise Fail('B1')
                            B1=BI+rest[:nb1-len(BI)]
                            R1=set(X)|set(B1); R2={u for u in X if u in I}|(set(B)-set(B1))
                            check_close([E,F,G,H,I],[R1,R2],T,r); n+=1
        print('r',r,'games',n,flush=True)
    print('ALL PASS',n)
run(int(sys.argv[1]) if len(sys.argv)>1 else 9)
