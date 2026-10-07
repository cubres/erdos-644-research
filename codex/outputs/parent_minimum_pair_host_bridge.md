# Minimum-pair anchoring and an actual residual good triple

Status: **hand proved reductions for k-uniform families**. These do not give
the final three-quarter upper bound. The subsequent certificate is allowed
to omit the original anchors.

Let tau(H)>T, with T an integer, and put b=k−T. Choose actual edges A,B
attaining the global minimum intersection m. Then m≤b: a T-subset of any
edge has an avoiding edge, whose intersection with that edge is at most b.
Write X=A∩B and V=(A∪B)\X, so |V|=2k−2m.

Among actual edges C avoiding X, choose one minimizing

    S=m+|A∩C|+|B∩C|.

Such an edge exists because m≤T. Only this fixed pair is retained in the
minimum; no minimum over all good triples is assumed. Put

    p=k−S+m,    Δ=2k−S−T=k+b−S,    K=2k−m−T.

The chosen C has p points outside V. Every actual edge D avoiding X obeys

    |D∩V|≥S−m=k−p,    |D\V|≤p,    p≤Δ.

The first inequality is fixed-pair minimality. The last follows from
Δ−p=b−m≥0. In particular, the outside error is controlled by the same
quantity as the near-full-host omission error; an arbitrary balanced
minimum-S anchor need not have this property.

For every set Z disjoint from X∪V, and every W⊂V of size K+|Z|≤|V|,
the deletion X∪(V\W)∪Z has size T. An actual avoiding edge D therefore
satisfies

    D∩V⊂W,  D∩Z=empty,  |D\V|≤p,  |W\D|≤Δ+|Z|.

All cardinalities here are integers. If the stated host size is impossible,
that host request is simply unavailable.

## A new actual good triple after deletion

Let H_X={D∈H:D∩X=empty}. Since a transversal of H_X together with X covers
H,

    tau(H_X)≥tau(H)−m>T−m.

If T−m≥floor((k+1)/2), H_X contains three actual edges with empty common
intersection. Otherwise it would be three-wise intersecting, and the
standard greedy intersection-chain theorem would give

    tau(H_X)≤floor((k+1)/2).

Thus a hypothetical family with tau>(3/4+epsilon)k has such a triple for
all sufficiently large k, since m≤k−T and T−m≥2T−k.

The same argument works for ANY deletion set X of size at most k−T,
without a minimum-pair hypothesis. This is a global source of replacement
triples, not an assumed closure property.

For the minimum-pair host above, any two edges D,E of H_X satisfy

    |D∩E|≥|D∩V|+|E∩V|−|V|≥2m−2p.

Consequently the new residual good triple has every pair core at least
2m−2p and each private part at most k−4m+4p. In the example
m=.24k, S=1.22k, T=.75k, these values are p=.02k, Δ=.03k,
|V|=1.52k, and pair overlaps at least .44k.

This does not invoke tau≤2k−S_new+1 for the original family: that cover
bound requires an appropriate minimum for the NEW anchor, and cannot be
applied merely because a high-S triple exists. Nor does it claim that the
five rows consisting of both old anchors and the new triple suffice.
The spanning-seed obstruction shows that old anchors may have to be omitted
from the final seven-edge contradiction.
