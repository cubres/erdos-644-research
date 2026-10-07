# A genuine near-complete host oracle from a minimum good triple

Status: **hand proved reduction; the final upper-bound bridge is open**.

Let a k-uniform family have a good triple A0,A1,A2 minimizing the sum S of
its three pairwise intersection sizes. Repetitions are allowed when the
common intersection is empty, as in the main note. Write Xi=Aj intersection
Ak, ai=|Xi|, and
\[
 p_i=k-a_j-a_k,\qquad V_i=(A_j\cup A_k)\setminus X_i.
\]
Thus pi is the size of the private part of Ai and |Vi|=2k−2ai.

For **every actual edge** D disjoint from Xi, minimality gives
\[
 |D\cap V_i|\ge S-a_i=k-p_i,\qquad |D\setminus V_i|\le p_i. \tag{1}
\]
Indeed Aj,Ak,D is a good triple, and its intersection sum is exactly
ai+|D intersection Vi|. This is a uniform bound on all outside portions,
rather than a containment assumption.

It also gives
\[
 \tau\le2k-S+1. \tag{2}
\]
To prove this, choose any subset W of Vi of size
|Vi|−(S−ai)+1. It meets all edges disjoint from Xi by (1), so Xi union W
is a transversal of size 2k−S+1.

Now assume tau>T for an integer T, and put
\[
 K=2k-a_i-T,\qquad \Delta=2k-S-T.
\]
For every set Z outside Vi union Xi and every host W contained in Vi with
\[
 |W|=K+|Z|\le|V_i|,
\]
the set Xi union (Vi minus W) union Z has size exactly T. Hence it has an
avoiding actual edge D, which obeys
\[
 D\cap V_i\subseteq W,\quad D\cap Z=\varnothing,\quad
 |D\setminus V_i|\le p_i,\quad |W\setminus D|\le\Delta+|Z|. \tag{3}
\]
The last inequality follows by subtracting the lower trace bound k−pi
from the host size. In particular, when Z is empty, **every K-point host**
contains the trace of an actual edge and misses at most Delta of its points.
This is stronger than existence of an edge with an arbitrary admissible
profile, and uses no type-closure hypothesis.

For the intermediate example a=(.49,.49,.24)k, choose i=2 and T=.76k.
Then Vi has size1.52k, pi=.02k, K=k, and Delta=.02k. Every k-point host in
Vi therefore contains at least .98k points of an actual edge, whose
outside portion has size at most .02k. The residual family of edges
avoiding Xi has transversal number greater than T−ai=.52k.

## Why balanced triples are the relevant target

If this residual family contained every k-set of Vi, and |Vi|≥3k/2,
we could take three rank-k edges formed from pairwise unions of three
disjoint k/2-point classes. They have empty common intersection and all
pairwise intersections k/2, so the new clustered-triple packing lemma would
give tau≤3k/4+O(1), including all other edges of the original family.
Thus the needed step concerns realizing a balanced good triple from (3),
or a version with errors charged below the assumed excess in tau.

The error cannot simply be omitted. At a fixed host, (3) allows an outside
portion of pi points; avoiding an earlier outside portion enlarges the
next host and its omission bound by the size of that avoidance. Three
independently chosen almost-full hosts may also have a common outside
point, so they need not be a good triple. Charging O(pi) to the final
budget does not prove the desired asymptotic coefficient when pi is
larger than the prescribed excess epsilon*k.

One possible global route is a dichotomy: either the host-realizing edges
have a small outside transversal (contradicting their large residual
transversal number when sufficiently small), or one can realize the
balanced host configuration with outside intersections under control.
The complete dichotomy, with an error depending on Delta or epsilon rather
than an uncontrolled multiple of pi, is not proved here.
