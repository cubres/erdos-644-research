# Critical two-anchor counterexamples and an induced-core criterion

Status: hand proofs. The statements below do not give a general upper bound for Problem 644.

## The minimum-intersection inequality fails under both criticality conditions

For every positive integer m, put k=7m, s=5m-1, c=6m-1. Take U of size k+s=12m-1 and disjoint c-subsets C1,C2. Let K consist of all k-subsets E of U that contain neither C1 nor C2 in full, and set

    H = K union {C1,C2}.

This is a rank-k family; its two shorter anchors have size c. It has (7,2), is edge-critical for its transversal number, every pair of vertices extends to a minimum transversal, and

    tau(H)=5m,    nu(H)=2,    min_{E,F}|E intersect F|=0.

To obtain (7,2), start with the proved full-core construction in Section7.97, including its two privately padded k-anchors. A private padding point belongs only to its own anchor, so replacing it in a piercing pair by any point of that anchor's core trace preserves every edge it hit. Thus removing the padding from both anchors preserves (7,2). Passing to the subfamily K with these anchors preserves it as well.

We first prove tau(K)=s. Every (k+1)-subset W of U contains a k-subset that contains neither C1 nor C2. Indeed 2c>k+1, so W contains at most one entire Ci. If it contains one, omit a point of that Ci; if it contains neither, omit any point. Hence any set of at most s-1 vertices misses an edge of K. Conversely, if E is a k-subset containing C1, then U minus E is an s-point cover of K. More precisely, the s-point covers of K are exactly U minus E for k-subsets E containing at least one Ci.

Each such cover misses an anchor, so tau(H)>s. Any (s+1)-subset of U meeting both C1 and C2 covers H, giving tau(H)=s+1=5m.

For E in K, the s-set U minus E meets both anchors and all other core edges. Thus E is essential. For the first anchor, choose a k-set E containing C1. Since 2c>k, E cannot contain C2, so U minus E covers K and C2 while missing C1. The same argument works for the second anchor. Hence every edge is essential.

Every pair of vertices of U can be extended to an (s+1)-subset meeting both anchors: s+1>=5, so adding at most one point of each missing anchor leaves enough room. Such a set is a minimum cover. This proves the pair-extension property, equivalently irreducibility under one vertex identification preserving tau.

The disjoint anchors give minimum intersection zero, but

    3tau(H)-2k=m.

Consequently the proposed inequality 3tau<=2k+mu+O(1) remains false even after imposing edge criticality and pair extension, when the normal form allows rank at most k. No incidence-minimality claim is made here. The ground set is small, |U|=k+tau-1, so this example does not contradict a ground-set stability approach.

There are also k-UNIFORM edge-critical examples with the same transversal and disjoint anchors. Retain the private padding, delete two core k-edges Ej containing Cj, and keep every other core edge. The pruned core has only two s-point covers U minus E1 and U minus E2; each misses its corresponding anchor. Both anchors are therefore essential in a family of transversal s+1. Any inclusion-minimal subfamily with that transversal retains both anchors, is k-uniform and edge-critical, and inherits (7,2). This uniform example need not satisfy the pair-extension property.

## An induced-core criterion that would close the bound

Let H have rank at most k, transversal t, and the property that every pair of distinct vertices occurs in a minimum transversal. Write H[U] for the actual family edges contained in U.

**Lemma.** If tau(H[U])>=t-1, then |V(H) minus U|<=1.

If distinct u,v lie outside U, choose a minimum t-cover containing both. Removing u and v leaves at most t-2 points that still cover every edge contained in U, a contradiction. This proves the lemma.

In particular, take an essential edge E, and a disjoint (t-1)-set B covering every other edge. If

    tau(H[E union B])>=t-1,

then |V(H)|<=|E|+t<=k+t. The Fano-partition inequality from Section7.88 gives

    t <= |V(H)|-4 floor(|V(H)|/7)
      <= 3|V(H)|/7+24/7.

Therefore 4t<=3k+24, or t<=3k/4+6.

The unresolved step is the existence of such a critical pair (E,B) in a hypothetical asymptotic counterexample. Neither edge criticality nor the pair-extension condition alone supplies it. This criterion is a sufficient reduction, not a proof of that existence statement.
