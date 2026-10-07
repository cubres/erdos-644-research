# mutation + branch-coverage test for referee_w4_handbound_exh.py
import sys; sys.path.insert(0,'.')
import referee_w4_handbound_exh as X, w4_handbound_e2e_lemmas as L
from collections import Counter
# 1) branch coverage of L26 at the minimal T, exhaustive H
br=Counter()
orig=L.run_L26
def run_L26_count(g,x,y,z):
    out=orig(g,x,y,z); E,F,G,H=out[0],out[1],out[2],out[3]
    a=len(F&H); b=len(G&H); T=g.T
    br['b<=T-x' if b<=T-x else ('a<=T-y' if a<=T-y else 'both big')]+=1
    return out
X.ADAPT=(('L26',L.T_L26,run_L26_count),)
X.main(4,9,1); print('L26 branches',dict(br))
# 2) mutation: T one less than minimal must fail somewhere
X.ADAPT=tuple((n,(lambda f:(lambda r,x,y,z:f(r,x,y,z)-1))(Tf),run) for n,Tf,run in (('L26',L.T_L26,L.run_L26),('L32',L.T_L32,L.run_L32),('L31',L.T_L31,L.run_L31)))
X.main(5,6,1)
