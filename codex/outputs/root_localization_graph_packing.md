# Robust private-trace packing with exceptional center pairs

Status: hand proof. This is a conditional strengthening of the packing
lemma in `agent_pure_core_private_trace_packing.md`, not a bound for all
(7,2)-families. It identifies what must be controlled when some genuine
incidence witnesses leave their two-center residuals.

Fix an actual critical edge E_0 and its disjoint critical cover B. Let
W be a nonempty set of centers with exactly two private rows each.
Write X_b^0,X_b^1 for their nonempty, disjoint traces on E_0, and put
m=|W| and e_0=|E_0|. In particular e_0>=2.

Define a simple graph L on W. Join b,c when some actual row with
B-trace {b,c} has, at both center incidences, genuine pure-core
shortening certificates entirely in the actual residual H_{bc}.
Certificates are witnesses for the full actual family. No incidence
minimality of an induced residual is assumed.

The preceding packing lemma proves that, for an edge bc of L, the
2-by-2 matrix (X_b^i intersect X_c^j) has at most one nonempty entry.
Consequently the complete bipartite graphs K_b between X_b^0 and
X_b^1, regarded as sets of unordered pairs of E_0, are edge-disjoint
whenever bc is an edge of L.

## 1. Independence number replaces complete localization

Let a=alpha(L). Then

    sum_{b in W} |X_b^0||X_b^1| <= a binom(e_0,2).       (1)

Indeed, for each unordered pair uv of E_0, the centers b for which
uv belongs to K_b form an independent set in L. There are at most a
such centers. Sum this multiplicity bound over all binom(e_0,2) pairs.

In particular some ACTUAL private row F satisfies

    |E_0 intersect F| <= sqrt(a e_0(e_0-1)/(2m)).         (2)

Some product in (1) is at most the right-hand side divided by m, and
the smaller factor of that product is at most its square root. Thus
the sufficient asymptotic condition for a sublinear actual intersection
is alpha(L)=o(m). Requiring localization for every pair, as in the
original packing lemma, is stronger than needed.

For example, if the graph of exceptional pairs (the complement of L)
has maximum degree D, then a<=D+1. Equation (2) gives an o(k)
intersection whenever D=o(m) and e_0<=k. No such bound on D is
established here.

## 2. Failure has a common pair of actual E_0 points

Suppose every private trace has size at least delta*k, where delta>0
and the actual rank bound is k. Then there is a fixed unordered pair
uv of E_0 and a subset W' of W such that

    |W'| >= ceil(m delta^2 k^2 / binom(e_0,2)),          (3)

and uv is an edge of K_b for EVERY b in W'. To prove this, the sum of
the pair multiplicities is the left-hand side of (1), at least
m delta^2 k^2. Some pair therefore has at least the average displayed
in (3). Define W' to be its set of centers.

After independently naming the two private rows at each center, one
has u in X_b^0 and v in X_b^1 for every b in W'. All pairs of centers
in W' are exceptional: W' is independent in L. Since e_0<=k, the
lower bound in (3) is at least 2m delta^2.

The critical trace-expansion inequality supplies at least three actual
double-trace rows for every pair b,c in W'. For EACH such target row,
at least one center incidence has no pure localized certificate.
Choose a genuine certificate for that incidence. The earlier
three-row/pure-core dichotomy says that it either gives the
at-most-three-row isolation branch, or, if pure, contains an actual
row whose B-trace meets a center outside {b,c}.

Thus a failure of the desired small-intersection conclusion can be
concentrated on many centers whose private rows separate the SAME
two actual points u,v. This is more precise than an arbitrary set of
exceptional pairs, but it is not a contradiction. Escaping witness
rows can be private at a third center; no increase in trace size,
rank cost, or terminating exchange is inferred.

## 3. Remaining requirements

This argument neither forces many centers to have exactly two private
rows nor bounds alpha(L). It also does not show that the three-row
isolation alternative is impossible. These are actual missing global
steps. The result supplies a useful conditional packing inequality
and a concrete common-pair configuration on which to focus an attempt
to prove those steps. No general transversal coefficient changes.


## 4. The common-pair block gives actual residuals of known transversal number

The block in Section2 has a further consequence using the same global
critical cover, with no localization assumption. For any Y contained in
W' with |Y|>=2, define the ACTUAL subfamily

    K_Y = {F in H: F avoids (B minus Y) union {u,v}}.

Then

    tau(K_Y)=|Y|-1.                                  (4)

Here is the full cover argument. The critical edge E_0 contains u,v,
so is absent from K_Y. All other actual rows meet B. Thus a row of
K_Y has nonempty B-trace contained in Y. It cannot have singleton
trace {b}: the only two such private rows are respectively hit by
u and v. Every surviving trace therefore has size at least two,
and Y minus any one of its points covers K_Y. This proves the
upper bound |Y|-1.

For the reverse inequality, the fixed set

    (B minus Y) union {u,v}

has exactly (t-1-|Y|)+2=t+1-|Y| points; u,v are distinct points of
E_0 and E_0 is disjoint from B. Adjoining this fixed set to any
transversal of K_Y gives a transversal of all H. Hence

    t <= t+1-|Y|+tau(K_Y),

proving (4).

In particular, for every b,c in W' there exists an ACTUAL row with
B-trace exactly {b,c} that avoids both u and v. For the whole block,
K_{W'} is an actual intersecting (7,2)-subfamily with transversal
number |W'|-1. Thus the exceptional block supplies more than a
finite list of compatible witnesses: it supplies a subfamily with
a rigorously controlled transversal number.

No decrease of maximum row size has been proved. The block can be
only a fixed fraction of the original critical cover, so (4) alone
need not preserve the hypothetical excess above3k/4. Iterating this
residual operation without a rank decrease therefore does not prove
the desired coefficient. Both the exact reduction and this numerical
limitation are part of its stated scope.
