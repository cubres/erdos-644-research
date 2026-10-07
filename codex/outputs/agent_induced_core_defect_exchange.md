# Induced-core defect: exact exchange constraints and a strengthened potential

Status: the exchange lemmas and bounds in this report are proved by hand. No defect descent sufficient for the 3/4 theorem is proved. This continues the trace lemma in `agent_centrality_induced_core_trace_lemma.md`; it does not rerun a certificate or alter the main note.

Let H have property (7,2), rank at most k, and transversal number t. The intended contradiction regime is t>(3/4+epsilon)k. Edge criticality supplies, for each actual edge E, a disjoint (t-1)-set B_E covering every other edge.

## 1. Constraints on exchanging a critical core

Fix U=E union B_E, e=|E|, q=tau(H[U]), and d=t-q. Thus |U|=e+t-1. The proved trace inequality gives, for every actual edge F,

    |F\U| <= |F|-6q+2|U|+8
             <= 3k-4t+6d+6
             < 6d-4epsilon k+6.                         (1)

Now suppose F is not contained in U, and let B_F be any critical (t-1)-cover disjoint from F. Every edge of H[U] belongs to H\{F}, so B_F intersect U covers H[U]. Consequently

    |B_F intersect U| >= q,
    |B_F\U| <= d-1.                                     (2)

These are simultaneous constraints on the actual edge F and its actual critical cover; neither assumes containment of a response in U.

For uniform edges |E|=|F|=k, put

    p_F=|F\U|,
    r_F=|B_F intersect U|-q >= 0,
    U_F=F union B_F.

The two cores have the same size k+t-1. Because F and B_F are disjoint, their exact exchange size is

    |U_F\U|=|U\U_F|=p_F+d-1-r_F.                        (3)

Thus the crude omitted-vertex bound is p_F+d-1, while surplus internal points in B_F reduce that loss one for one. If the original core maximizes q over critical pairs, q_F=tau(H[U_F])<=q. On the other hand,

    tau(H[U intersect U_F]) >= q-|U\U_F|,

so the new core retains at least q-(p_F+d-1-r_F) of the old transversal number. The bound follows by adjoining U\U_F to any transversal of the restricted old family. This charge is valid, but it does not give a positive gain from the newly admitted edge F.

The exact failure of the naive exchange is twofold. Removing active old vertices can remove entire internal edges. Moreover, even if a residual old family still has transversal number q, deletion can create new q-transversals, and F may hit those new transversals. An edge avoiding one chosen old minimum cover does not eliminate all minimum covers. There is no basis-exchange axiom for minimum transversals that would justify ignoring either effect.

## 2. It is useful to allow all bounded hosts

For proving the upper bound, an induced host need not remain a critical core after every exchange. Set

    N0=k+t-1.

If ANY vertex set U with |U|<=N0 contains an actual edge and satisfies q=tau(H[U])=t-d, the trace bound applied to an actual edge E contained in U gives

    6q <= 2|U|+|E|+8 <= 3k+2t+6,
    4t <= 3k+6d+6.                                      (4)

Therefore finding an arbitrary bounded host with d=o(k) is sufficient. This relaxation permits a genuinely valid strengthened extremal potential.

Choose U among all hosts of size at most N0 by first maximizing q=tau(H[U]), then minimizing the number b(U) of q-element transversals of H[U]. Remove vertices not lying in any edge of H[U] from the mathematical host. Such a vertex belongs to no minimum transversal, so neither q nor b changes. We may thus assume

    U = union H[U].

This is only a mathematical choice of host; it is not an operation deleting vertices or incidences from H. Let f=N0-|U| be the remaining host capacity.

## 3. Free-slot exchange lemma

For every minimum q-transversal C of H[U], every actual edge F disjoint from C satisfies

    |F\U| > f.                                         (5)

Proof. If |F\U|<=f, put U'=U union F. This remains an admissible host. It retains every old internal edge and adds F. Hence tau(H[U'])>=q, and maximality of q forces equality. Any q-element transversal of H[U'] must use all its q vertices inside U, since the old family H[U] already requires q points there. Thus its minimum-cover family is a subfamily of the old minimum-cover family. The old cover C is absent, because it misses F. Hence b(U')<b(U), contradicting the secondary optimization.

Since q<t, an actual F avoiding C always exists. Thus this lemma provides an exact descent whenever a response fits in the unused capacity; it needs no critical-cover extension assumption and no type closure.

Combining (5) with the trace bound gives

    N0-|U|+1 <= k-6q+2|U|+8,
    6q <= 3|U|+k-N0+7.

Writing q=t-d and N0=k+t-1,

    7t <= 3|U|+6d+8 <= 3k+3t+6d+5,
    4t <= 3k+6d+5.                                      (6)

This essentially reproduces the trace deficit inequality, rather than improving its asymptotic coefficient. Quantitatively, the elementary free-slot descent stalls at active hosts occupying nearly the entire available budget. It cannot by itself force d=o(k).

## 4. A precise sufficient active-vertex exchange

The preceding proof still works if one deletes active vertices W from U, provided the loss of minimum-cover information is controlled. More precisely, fix a minimum q-cover C of H[U] and an actual F disjoint from C. Suppose W is a subset of U\F such that

  (i) |(U\W) union F| <= N0;
  (ii) tau(H[U\W])=q;
  (iii) every q-element transversal of H[U\W] is also a transversal of H[U].

Then U'=(U\W) union F contradicts the extremal choice of U.

Indeed, (ii) and maximality force tau(H[U'])=q. Every q-cover of H[U'] lies entirely in U\W, since q points are already needed for H[U\W]. By (iii) it is an old q-cover. The chosen C is not a new q-cover, since it misses F (regardless of whether C also meets W). Thus the number of minimum covers strictly decreases.

Condition (iii) is the substantive missing ingredient. The weaker statement that deleting W preserves the transversal NUMBER does not suffice: it can leave q unchanged while admitting new q-covers. The strengthened potential records precisely the information that a valid active-vertex exchange must preserve or outweigh.

One could instead prove a quantitative version in which the added actual edges eliminate more new q-covers than deletion creates. Nothing in the present argument bounds those two populations. Treating a single escaping edge as an automatic unit gain in transversal number would be incorrect.

## 5. Why normalization remains essential, and the open step

Edge criticality alone does not imply retention of a high-transversal induced core. The private-padding construction identified by the other agent has property (7,2) and is edge critical near the 3/4 threshold, while every O(k)-vertex actual induced host has only O(log k) transversal number. Its padding is removed by incidence minimization, so it does not refute a theorem in the full minimum-vertex, incidence-minimal normal form. It does show why generic edge-critical compactness cannot supply the missing step.

The new exchange proof itself does not yet exploit that full normalization. Its current endpoint is exact:

* all escaping edges have the outside-rank bound (1);
* their critical covers satisfy (2), with the exact uniform swap charge (3);
* the lexicographic bounded-host potential excludes every response that fits in unused capacity;
* a response requiring deletion of active vertices must satisfy a minimum-cover retention or net-elimination statement such as (iii).

A proof must now use minimum-vertex and incidence-minimal structure to establish such an active exchange, or directly show that some bounded host has d=o(k). Neither has been derived here. The outside-rank and critical-cover bounds alone provide only an additive loss bound and do not yield an improvement in q. No supercritical counterexample to the desired defect descent is known from this investigation.
