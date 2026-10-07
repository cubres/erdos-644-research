# Mutation test: drop each hypothesis term in turn; the pair-level checker must find a failure
# for (most) terms, showing the checker is sensitive and the hypotheses are used.
import referee_w5_paper_sec3_pairlevel as M
import itertools
def run(hyp, fn, R=8):
    for r in range(1,R+1):
        for x in range(r+1):
            for y in range(r+1-x):
                for z in range(r+1):
                    if x+z>r or y+z>r: continue
                    for T in range(0,r+3):
                        if hyp(r,x,y,z,T):
                            try: fn(r,x,y,z,T)
                            except M.Fail as e: return (r,x,y,z,T,str(e))
                            except Exception as e: return (r,x,y,z,T,'EXC '+repr(e))
    return None
def terms26(r,x,y,z,T):
    S=x+y+z
    return [3*T>=r+2*x+2*y+z, T>=S, T>=r-x+z, T>=r-y+z, 2*T>=2*r-2*x+y, 2*T>=2*r-2*y+x]
def terms32(r,x,y,z,T):
    S=x+y+z
    return [T<=r, T>=S, 2*T>=r+2*y, 2*T>=r+2*x-y+z, 3*T>=r+2*x+y+3*z]
def terms31(r,x,y,z,T):
    S=x+y+z
    return [T<=r, T>=x+y, 2*T>=r+2*x, 2*T>=r+2*y, T>=r+x-y-z, T>=r-x+y-z, 3*T>=3*r-S, 5*T>=3*r+S, 3*T>=r+x+y+2*z, 4*T>=2*r+3*z]
def termsS2(r,x,y,z,T):
    P=max(0,r+y-x-z-T); Q=max(0,r+x-y-z-T)
    return [x<=T, y<=T, T>=r-x+z+P+Q, T>=y+z+Q, 2*T>=r+y+2*z+P+2*Q]
for name,terms,fn in [('L26',terms26,M.L26),('L32',terms32,M.L32),('L31',terms31,M.L31),('S2',termsS2,M.S2)]:
    n=len(terms(1,0,0,0,0))
    for i in range(n):
        h=lambda r,x,y,z,T,i=i: all(t for j,t in enumerate(terms(r,x,y,z,T)) if j!=i)
        print(name,'drop term',i,'->',run(h,fn),flush=True)
