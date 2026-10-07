"""Exact integer threshold for Lemma D'' (anchored pencil with protruding anchor F and host H^(m)_U).
Q(N,f,g,m,t) := largest q_m NOT contradicted = min over admissible configurations of max(w+b+b', w+c+c'+min(g,m)).
(7,2) and tau(H)=t imply tau(H^(m)_U) <= Q.  We compare Q with the closed form
   B = max( ceil(f/2)+min(g,m) + s1 ,  N-2t+ceil(f/2)+g+2m+min(g,m) + s2 )
and report the least integer slacks s1,s2 making Q <= B over the scanned range, under the side condition
   m+g <= floor(f/2) - 1  and  ceil(f/2)+2m+g+2 <= t   (so that the balanced unbalanced-quartering exists)."""
import itertools, math, sys
def Q(N,f,g,m,t):
    best=None
    T=t-1; mg=min(g,m)
    for b in range(f+1):
        for bp in range(f+1-b):
            if abs((b+bp)-f/2)>1: continue   # host halves must be balanced (else host term only grows)
            for c in range(f+1-b-bp):
                cp=f-b-bp-c
                ra=T-max(b+c, bp+cp+2*m+g)
                rap=T-max(bp+c+m, b+cp+m+g)
                if ra<0 or rap<0: continue
                w=max(0,N-f-ra-rap)
                v=max(w+b+bp, w+c+cp+mg)
                if best is None or v<best: best=v
    return best
worst1=-99; worst2=-99; cnt=0; infeas=0
for f in range(2,19):
  for g in range(0,6):
    for m in range(0,6):
      if m+g>f//2-1: continue
      for t in range(math.ceil(f/2)+2*m+g+2, math.ceil(f/2)+2*m+g+14):
        for N in range(f, f+2*t+6,1):
          q=Q(N,f,g,m,t); cnt+=1
          if q is None: infeas+=1; continue
          A=math.ceil(f/2)+min(g,m); Bv=N-2*t+math.ceil(f/2)+g+2*m+min(g,m)
          # slack needed: q <= max(A+s1, Bv+s2); record minimal s2 with s1=1 fixed
          if q>max(A+1,Bv):
              worst2=max(worst2,q-Bv)
          worst1=max(worst1, q-max(A,Bv))
print("cases",cnt,"infeasible",infeas)
print("max of Q - max(A,B) :",worst1)
print("least s2 such that Q <= max(A+1, B+s2) :",worst2)
