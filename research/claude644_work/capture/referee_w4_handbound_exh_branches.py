# Referee: branch coverage of L31/L32 under the exhaustive-H checker (referee_w4_handbound_exh.py)
import sys; sys.path.insert(0,'.')
import referee_w4_handbound_exh as X, w4_handbound_e2e_lemmas as L
from collections import Counter
br=Counter()
o31,o32=L.run_L31,L.run_L32
def c31(g,x,y,z):
    out=o31(g,x,y,z); E,F,G,H=out[:4]; T=g.T; r=g.r
    Z=F&G; Q=Z&H; a=len((F&H)-Q); b=len((G&H)-Q); c=len(E&H)
    a0=r+x+z-2*T; b0=r+y+z-2*T
    br['L31 '+('c<=T-z' if c<=T-z else 'a<a0' if a<a0 else 'b<b0' if b<b0 else 'interval')]+=1; return out
def c32(g,x,y,z):
    out=o32(g,x,y,z); E,F,G,H=out[:4]; T=g.T
    br['L32 '+('A small' if len(F&H)<=T-y-z else 'A big')]+=1; return out
X.ADAPT=(('L32',L.T_L32,c32),('L31',L.T_L31,c31))
X.main(int(sys.argv[1]),int(sys.argv[2]),1); print(dict(br))
