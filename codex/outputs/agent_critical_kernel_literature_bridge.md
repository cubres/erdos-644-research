# Critical-kernel literature bridge: exact scope and two elementary obstructions

Date: 2026-09-23. Internal draft. No publication or external communication.
Authoritative comparison: research `note_644.md`, Sections 7.87–7.90,
7.178–7.186. No existing certificate was replayed.

**Outcome.** No primary-source theorem found in this bounded search proves
the missing near-linear kernel or the general three-quarter bound. The
most directly applicable critical-order theorem is far too large at
growing rank. More usefully, the classical Hall-neighborhood route and
the minimum-cover blocker route have precise rank obstructions stated
below. A separate numerical calculation quantifies the loss in the
Bucić–Korándi–Sudakov covering-clutter route: even removing its logarithmic
rounding loss leaves a factor about 24.213 where width seven is required.
These are limitations of specified applications, not impossibility
results for all kernel or dual methods.

## 1. What the primary critical-order theorem actually supplies

Gyárfás–Lehel–Tuza, *Upper Bound on the Order of tau-Critical Hypergraphs*,
JCTB 33 (1982), 161–165, Theorems 1 and 2 and Remark 2:

https://users.renyi.hu/~gyarfas/Cikkek/15_GyarfasLehelTuza_UpperBoundOnTheOrderofTauCriticalHypergraphs.pdf

For an r-uniform edge-tau-critical hypergraph of transversal number t,
the paper proves

    |V| <= t binom(t+r-2,r-2) + t^(r-1).

Its neighborhood lemma assumes a **strongly stable** set S: every edge
meets S in at most one point. With Gamma(S) the family of deleted-point
edge neighborhoods, it proves

    d(x) <= |Gamma(S)| - |S| + 1    for x in S.

Here Gamma consists of sets, not neighboring vertices. Thus even the
corollary |S| <= |Gamma(S)| does not bound S by a small vertex set.
Remark 2 treats the requirement that every prescribed q-set extend to a
t-element transversal as an additional arrow-property parameter; it does
not give the desired estimate n <= r+t+o(r) for q=2 and growing r.

The normal form is rank bounded, not necessarily uniform. Private padding
allows the uniform theorem to be applied, but the padded family has at
least as many vertices as the original one. Even the resulting upper
bound is enormous when r=k and t is proportional to k. Private padding
is a mathematical comparison here, not a claim that the padded object
still has the original minimum-vertex normal form.

## 2. An exact obstruction to applying the strong-stability lemma to alpha

The following is an elementary consequence of actual edge criticality.
It does not require saturation, pair extension, or a fabricated edge.

**Lemma.** Let H be edge-tau-critical, tau(H)=t, and E an actual edge.
Choose a (t-1)-cover B_E of H minus E, disjoint from E. For every x in E,

    I_x = V(H) minus (B_E union {x})

is a maximum independent set and contains E minus {x}. Consequently any
partition of I_x into strongly stable sets uses at least |E|-1 parts.

**Proof.** B_E union {x} meets every edge of H and has t points, so its
complement is independent of size |V|-t=alpha(H). Its intersection with
E is exactly E minus {x}. A strongly stable set contains at most one
point of E. Covering those |E|-1 points by a partition into such sets
therefore requires at least |E|-1 parts. This proves all claims.

In the normal form, every actual edge has size at least

    e >= t - floor((k+4)/5),

and in an intersecting family e>=t. Thus the displayed obstruction costs
Omega(k) parts in the putative t>3k/4 regime. One cannot silently use the
strong-stability neighborhood theorem on a maximum independent set, or
partition it into O(1) admissible sets. The lemma does not exclude a
special maximum independent set with additional useful structure; it
identifies why the automatically supplied critical maximum independent
sets do not have that structure.

## 3. The minimum-cover blocker retains the original large edges

Let T be the hypergraph of all minimum transversals of H, and b(T) its
blocker, namely the inclusion-minimal sets meeting every member of T.

**Lemma.** Every actual edge E of an edge-tau-critical H is a member of
b(T).

**Proof.** Every minimum transversal meets E, so E meets every edge of T.
For any x in E, the minimum transversal B_E union {x} meets E only at x.
Hence E minus {x} fails to meet that member of T. Every proper subset of
E is contained in some E minus {x}, and is not a transversal of T.
Therefore E is inclusion-minimal as asserted.

In particular,

    rank(b(T)) >= rank(H),

not just the minimum-edge lower bound. T itself has rank t. Neither
operation produces a bounded-rank auxiliary clutter in the intended
asymptotic regime. The pair-extension property only says that the
2-shadow of T is complete. Replacing T by this shadow loses all its
higher-order information: the shadow is the same complete graph for
every family satisfying pair extension, regardless of t and k.

There may be extra edges in b(T). Adding them to H preserves its minimum
covers, but preservation of property (7,2) is an additional unproved
requirement. Edge criticality does not license that saturation step.
This report does not use it.

## 4. Quantified barrier in the published covering-clutter route

Bucić–Korándi–Sudakov, *Covering graphs by monochromatic trees and
Helly-type results for hypergraphs*, Combinatorica 41 (2021),
Theorem 5.3 and Appendix A (Proposition A.1, Theorem A.2):

https://arxiv.org/html/1902.05055v4

The relevant exact auxiliary construction puts the actual edges of H
on its vertex set. For every pair S of original points, make an auxiliary
edge consisting of the original edges disjoint from S. Call this C_2(H).
Its transversal number is the minimum size of a non-two-pierceable
actual subfamily. Also tau(H)>2s is equivalent to s-wise intersection
of C_2(H). Theorem A.2 says that an s-wise intersecting hypergraph with
M vertices and maximum degree D satisfies

    tau <= M^(1/s) (1+log D).

Consequently, Theorem 5.3, in our variable names, requires

    local_width >= binom(k+u,u)^(1/floor(u/2)) * 4k log(2k)

in order to conclude tau(H)<=u.

Here is the explicit asymptotic comparison, derived in this report.
If u/k -> beta>0, Stirling's formula gives

    log binom(k+u,u)
      = k[(1+beta) log(1+beta) - beta log beta] + o(k).

Hence

    binom(k+u,u)^(1/floor(u/2))
      -> exp((2/beta)[(1+beta) log(1+beta)-beta log beta]).

At beta=3/4 this limit is

    (7/4)^(14/3) * (4/3)^2 = 24.2133585873... > 7.

The exact expression, rather than its decimal, establishes the strict
inequality. For example (7/4)^(14/3)>(7/4)^4>9 and (4/3)^2>1, so it is
already greater than seven.

Thus even the hypothetical replacement of the logarithmic rounding
factor by one would not make this particular universal edge-count
substitution prove the width-seven theorem. It would need a genuinely
stronger estimate for the relevant covering clutter or a structurally
improved original-edge count.

The ordinary critical-edge count is exponentially tight even at the
known three-quarter boundary. Indeed all k-sets on n=k+t-1 vertices
form an edge-critical family of transversal number t, with
binom(k+t-1,k) edges. Taking k=4m, t=3m, n=7m-1 gives property (7,2)
by the existing complete-family/Fano partition argument. Its edge count
has exactly the exponential rate above. This does not rule out a
structural drop for hypothetical families with t>(3/4+epsilon)k; proving
such a drop would itself be new information, absent from the cited
bound. The report makes no general claim that all dual approaches lose
this constant.

## 5. Fresh literature status and the recent regularity near-candidate

The author-hosted 1999 Fon-Der-Flaass–Kostochka–Woodall PDF was accessible:

https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf

Its introduction states the published ceiling(7k/8) upper bound. The
2021 paper above still treats the general local-cover problem and cites
1999. A targeted search of the exact title, f(k,7), and Problem 644 did
not locate a later proof of the desired three-quarter statement.

The indexed page for https://www.erdosproblems.com/644 currently displays
OPEN and no claimed proof. Direct page and LaTeX/discussion fetches
failed (HTTP 403 or tool fetch errors), so this is **indexed status,
not a successful live-page confirmation**. An independently authored
recent computational working report surfaced a claim f(12,7)>=10,
already present in our note; its certificate was not replayed and is not
used here as new evidence. No claim of exhaustive bibliographic coverage
is made.

A genuinely newer primary source located in the citation trail is
Henning–Yeo, *Extensions and applications of the Tuza–Vestergaard
theorem*, European J. Combin. 130 (2025), 104201:

https://findresearcher.sdu.dk/ws/portalfiles/portal/292254822/1-s2.0-S0195669825000897-main.pdf

Its Theorem 2 bounds transversals of **6-uniform** hypergraphs with maximum
degree four, with explicit exceptional-component terms; Theorem 4 gives
tau<=2n/7 for 4-regular 6-uniform hypergraphs. The source's abstract and
main statements were checked. This does not mean six arbitrary actual
edges with point degree at most three meet its hypotheses. Such an
actual tuple has six edges of rank up to k; its incidence dual has six
vertices and edges of size at most three. Neither is the required
6-uniform object, and a transversal of that auxiliary tuple does not
cover the full original family. No application to the global endpoint
minimum is established.

## 6. Actionable conclusion

The critical-kernel route still needs a theorem using the simultaneous
(7,2) condition and critical incidence witnesses. Existing critical-order
bounds, pair extension alone, and passage to all minimum covers do not
supply it. The more specific live target remains a global constraint on
actual endpoint sets/response exchanges. The bounded literature search
provides no reason to replace that target with a generic kernel theorem.
