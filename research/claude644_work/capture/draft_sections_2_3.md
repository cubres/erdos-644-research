## 2. Two families of host inequalities

Throughout, H is a finite family of nonempty sets of rank at most k with property (7,2),
V = V(H), t = tau(H). For U subset V and an integer m >= 0,

    H^(m)_U = { G in H : |G \ U| <= m },        H^(0)_U = H[U].

### 2.1 Fano facts used

PG(2,2) has seven points and seven lines, three points per line, three lines per point, any
two lines meet in exactly one point. Index seven edges G_l by the lines l. For a vertex x put
sigma(x) = { l : x in G_l }.

**Fact F1 (Venn criterion; note Lemma 1.1).** G_1,...,G_7 have no transversal of size <= 2
iff for all vertices x,y (x = y allowed) some G_l misses both.

**Fact F2 (safe line sets).** Call a set S of lines *safe* if some point lies on no line of S.
If every vertex x has a point p(x) lying on no line of sigma(x), the seven edges have no
transversal of size <= 2. (For x,y take a line through p(x),p(y); it lies in neither sigma.)
Any <= 2 lines are safe; three lines are safe iff not concurrent; four lines are safe iff they
are exactly the four lines missing one point; five or more lines are never safe.

**Fact F3 (pencil).** Fix a point p0. The three lines through p0 form the *pencil*
l1 = {p0,a,a'}, l2 = {p0,b,b'}, l3 = {p0,c,c'}. Every other point lies on exactly one pencil
line. The remaining four lines ("m-lines") all miss p0; each contains exactly one point of
{a,a'}, one of {b,b'} and one of {c,c'}, and the four m-lines are the four such transversals
with an even number of primes: (a,b,c), (a',b',c), (a',b,c'), (a,b',c'). Each non-p0 point
lies on exactly two m-lines. The m-lines through a are (a,b,c),(a,b',c'); through a' they are
(a',b',c),(a',b,c').

(Concretely, with points 0..6 and lines 013,124,235,346,450,561,602, take p0=0,
a=1,a'=3,b=4,b'=5,c=2,c'=6; the m-lines are 124, 235, 346, 561.)

### 2.2 Lazy protrusion bounds (Lemma A, Lemma A_E)   [FULL PROOF]

**Lemma A.** For every U with |U| = N and every m >= 0,

    tau(H^(m)_U) <= N - 4 floor(N/7) + 3m.

*Proof.* Split U into classes V_p (p a point) of sizes floor(N/7) or ceil(N/7), and put
lambda(x) = p for x in V_p; so each line union L_l = union_{p in l} V_p has at most
N - 4floor(N/7) points. Vertices outside U stay unlabeled. Suppose
tau(H^(m)_U) >= N - 4floor(N/7) + 3m + 1. Order the lines l_1,...,l_7. For j = 1,...,7 choose
G_j in H^(m)_U disjoint from A_j = L_{l_j} union F_j, where F_j is the set of outside
vertices x such that sigma_{<j}(x) union {l_j} is not safe (sigma_{<j}(x) = lines l_i, i<j,
with x in G_i). An unsafe set has at least three lines, so every x in F_j lies in at least
two of G_1,...,G_{j-1}; hence |F_j| <= (1/2) sum_{i<j}|G_i \ U| <= 3m. Thus
|A_j| < tau(H^(m)_U) and G_j exists. Every labeled x satisfies p(x) := lambda(x) not on any
line of sigma(x). Every outside x has safe sigma(x): at its last membership step it was not in
F_j. By F2 the <= 7 distinct edges G_j have no transversal of size <= 2, contradicting (7,2). []

**Lemma A_E.** For every edge E, every R subset V \ E and every m >= 0,

    tau(H^(m)_{E cup R}) <= 2ceil(|E|/4) + ceil(|R|/3) + floor(5m/2).

*Proof.* Put G_{l1} := E, label E on the four points off l1 (quarters), R on the three
points of l1 (thirds). Every line l != l1 meets l1 in one point and has two points off it, so
|L_l cap U| <= 2ceil(|E|/4) + ceil(|R|/3); E is disjoint from L_{l1} cap U = R and has no
outside points. Choose the other six edges lazily as in Lemma A; at the last step at most five
protruding edges precede, so |F_j| <= 5m/2. []

### 2.3 Pencil host bounds (Lemma C, Lemma D, Lemma D')   [FULL PROOF; checks [C] below]

The new point is to give **every vertex outside the chosen region the label p0**. By F3 the
four m-lines miss p0, so their edges may be *arbitrary* edges of H: only the region's vertices
labelled on the line must be avoided, and an edge avoiding any set of size <= t-1 exists.
Only the three pencil lines need edges avoiding the p0-class; these come from the host.

**Lemma C (no anchor).** For every U subset V with |U| >= 6 floor((t-1)/3),

    tau(H[U]) <= |U| - 4 floor((t-1)/3);

and if 3 ceil(|U|/6) <= t-1 then tau(H[U]) <= 2 ceil(|U|/6).

*Proof.* Let u = floor((t-1)/3), put u vertices of U at each of the six points other than
p0 and the remaining w = |U| - 6u vertices of U at p0; every vertex outside U gets p0. Each
m-line carries 3u <= t-1 labelled vertices, none outside U, so some edge of H avoids them.
Each pencil line carries w + 2u vertices of U plus all outside vertices; an edge of H[U]
avoiding those w + 2u = |U| - 4u vertices exists if tau(H[U]) > |U| - 4u. Then every vertex
lies only in edges of lines missing its label, and F2 contradicts (7,2). For the second
statement use w = 0 and near-equal classes of size ceil(|U|/6). []

**Lemma D (one anchor).** Let E in H, e = |E|, 2ceil(e/4) <= t-1, R subset V \ E. Then

    tau(H[E cup R]) <= max( 2ceil(e/4),  |R| + 6ceil(e/4) - 2t + 2 ).          (D)

*Proof.* Let s = ceil(e/4) and rho = t-1-2s >= 0. Split E into four classes of sizes floor(e/4)
or ceil(e/4) placed at b,b',c,c'. If |R| <= 2rho put ceil(|R|/2) vertices of R at a and the rest
at a' (w = 0); otherwise put rho at each of a,a' and w = |R| - 2rho at p0. All outside vertices get
p0. Edges: G_{l1} := E (its labels avoid l1). Each m-line carries at most rho + 2s = t-1 labelled
vertices: take any edge of H avoiding them. Each of l2, l3 carries the w vertices at p0, two
quarters of E (at most 2s vertices) and the outside vertices: take an edge of H[E cup R] avoiding
the at most w + 2s vertices of E cup R on it, which exists if tau(H[E cup R]) > w + 2s. By F2
these seven edges are not 2-pierceable. Hence tau(H[E cup R]) <= w + 2s, which is (D). []

Equivalently, (E, G_{l2}, G_{l3}) is a good triple whose union lies in E cup R_a cup R_a',
a set of size at most 2(t-1), and the four m-line edges are the classical static requests; the
host oracle is what supplies the two further triple edges.

**Corollary D1 (critical hosts).** If E is an edge and B is any (t-1)-set disjoint from E
(for instance a critical cover), then with d = t - tau(H[E cup B]),

    t <= 3|E|/4 + d/2 + 11/4        whenever the second term in (D) is the maximum;

in general d >= min( t - 2ceil(e/4), 2t - 6ceil(e/4) - 1 ).

Compare note 7.124 (7): t <= 3e/4 + (3/2)d + 3/2. A hypothetical counterexample with
t >= (3/4+eps)k must therefore have d >= 2eps k - O(1) at EVERY critical host (previously
(2/3)eps k). Note that Lemma D does not use criticality of B at all.

**Lemma D' (protruding host edges).** With E, e, s as above, m >= 0 and 2s + m <= t-1,

    tau(H^(m)_{E cup R}) <= max( 2s, |R| + 6s + 2m - 2t + 2 ).

*Proof.* As for (D) with rho = t-1-2s-m, host edges G_{l2}, G_{l3} taken from H^(m)_{E cup R}.
Write O2, O3 for their outside parts. The m-edges through a, namely (a,b,c) and (a,b',c'),
also avoid O2; the m-edges through a', namely (a',b',c) and (a',b,c'), also avoid O3. Each
m-request has size at most rho + 2s + m = t-1. An outside vertex in O2 \ O3 lies at most in
l2, (a',b',c), (a',b,c'): these three lines miss a, so the set is safe. Symmetrically O3 \ O2
lies at most in l3 and the two m-lines through a, which miss a'. A vertex of O2 cap O3 lies
only in l2, l3 (safe). Outside vertices in no host edge lie only on m-lines, which miss p0.
F2 finishes. []

At a critical host this gives t <= 3e/4 + d_m/2 + m + O(1), d_m = t - tau(H^(m)_{E cup B}).

### 2.4 Two further pencil consequences   [FULL PROOF]

**Disjoint pairs.** If F, G in H are disjoint then the seven-line pencil labelling with
F at b,b',c,c' (quarters), G at a,a' (halves), everything else at p0, and G_{l1} = F,
G_{l2} = G_{l3} = G, shows that H is not (7,2) as soon as ceil(|G|/2) + 2ceil(|F|/4) <= t-1.
Hence |F| + |G| >= 2t - O(1) for every disjoint pair.

**Anchor with protrusion (upper trace bound).** For any edge F and any host U with
f = |F cap U|, g = |F \ U|, placing F entirely at b,b',c,c', U \ F at p0, a, a', other vertices
at p0, gives

    tau(H[U]) <= max( 2ceil(f/4)..., |U| - 2t + g + ceil(f/2) ) + O(1)

(the host edges avoid F's outside part automatically). In particular an edge with a large
trace on a high-transversal host must protrude a lot.

### 2.5 Computer checks of the pencil construction   [C, randomized + exact thresholds]

* `pencil_check.py` — builds the Fano/pencil seven-tuple on random families and random
  hosts/labelings; whenever all seven edges exist, verifies exhaustively that no <= 2-point
  transversal exists (15 084 completed constructions, 0 failures).
* `pencil_exact.py` — computes the exact integer optimum h_D(e,|R|,t) of the Lemma D labelling
  LP and h_C(N,t); on the whole grid t <= 25 the excess over the leading terms
  max(ceil(e/2), |R|+3e/2-2t) is at most 3.5 (resp. 8/3 for Lemma C).
* `pencil_endtoend.py` — random families (no (7,2) assumed): in all 886 cases where
  tau(H[E cup R]) exceeded the bound (D), the explicit seven edges were built and shown bad.
* `pencil_protrusion_check.py` — same for Lemma D' with m in {0,1,2}: 3202 cases, 0 failures.

These are checks of the combinatorics, not substitutes for the hand proofs above.
