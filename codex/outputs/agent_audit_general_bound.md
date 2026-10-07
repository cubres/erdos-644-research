# Independent audit of the general 6/7 bound

Audit date: 2026-09-21. The general 3/4 conjecture remains open.

## Conclusion

I found no mathematical gap in the checked proof of

\[
f(k,7)\le \lceil6k/7\rceil+10\qquad(k\ge1000).
\]

The exact replay passed all 256 chronological steps, including 215 steps using earlier gaps, and all 18,270 cover nodes. This audit also examined the hand reductions, the local allocation proofs, and the uniform integer allowance; it was not limited to accepting the replay's output. This is an independent agent audit, not external review or a formal proof-assistant verification, and makes no priority claim.

Command rerun successfully in `/Users/cubres/Documents/Clauding/erdos-hunt`:

```text
python3 -S p644_astra_six_sevenths_check.py
```

The input was `logs/astra_interval_finished_6_7.json`. Its final excluded interval is `[143/1000,1/2]`.

## Mathematical scope and dependency checks

1. **Avoidance is justified by the global transversal assumption.** If `tau>K`, every set of at most K points is avoided by a family edge. Every local construction uses this same assumption. No intersecting-family assumption is needed.

2. **Initial caps produce a genuine good triple.** For an initial intersection of size qr, take two subsets of the original edges, each containing their intersection, leaving caps `floor(ur)` and `floor(vr)`. Their union has size
   `2r-qr-floor(ur)-floor(vr) < beta*r+2` because `u+v=2-beta-q`. The checker verifies nonnegative caps and that they fit their hosts. Avoiding the union empties the common intersection. Repeated response edges do not invalidate the argument: a bad indexed tuple yields a bad subfamily of at most seven distinct edges.

3. **Chronology is genuinely one-way.** Each step's `prior_gaps` equals the interval union already proved. Maximum-small parameters are recovered from an already excluded interval ending at 1/2. The trace-dichotomy parameters refer to previously excluded intervals. No new exclusion is used in its own proof.

4. **Closed boxes safely enlarge the domain.** Retaining already forbidden endpoints cannot omit a possible triple. The six coordinate-order tetrahedra cover each box; replacing one edge by an interior rational division produces two tetrahedra with the same union. Every leaf checks every affine bound at all four vertices. Physically unrealizable triples sometimes also belong to a box; covering them does not weaken the proof for realizable triples.

5. **Static-template duality gives an upper bound for a reason.** The full equal-label-price hyperplane arrangement is enumerated on the four-price simplex. A piecewise-linear objective attains its maximum at an arrangement vertex. Complete enumeration, together with LP duality, establishes that an allocation exists; checking a collection of feasible dual points alone would not have sufficed. I checked the implementation's coordinate planes, label-price planes, Gaussian solve, nonnegative-price restriction, affine substitution, and adjacency/blocker conditions.

6. **Static integer rounding is uniform.** A part with a allowed labels loses an integer remainder of at most a-1 when its allocated masses are rounded down. Restoring the six part totals increases any request by at most `sum(a-1)<=15-6=9`. It preserves every permitted label and therefore every covered pair product. This is valid for every integer rank; no divisibility assumption is hidden here.

7. **The imported hand regions match their stated inequalities.** I read Lemmas 7.18, 7.20, 7.23, 7.25, 7.26, 7.29–7.33, 7.35, 7.37, 7.41, 7.43, 7.46 and 7.47, and checked their allocation/host arguments and the affine forms imported by the replay. In particular, the domain `S>=beta*r` in Lemma 7.37 and the separate trace-forcing domain inequalities in Lemmas 7.43 and 7.46 are actually enforced by the checker.

8. **The two new lemmas withstand the delicate integer checks.** In Lemma 7.46, `x+y>=r-hr` implies `x+y>=r-floor(hr)` because x+y is integral; thus the cut size `g=(r-y-floor(hr))_+` fits X and Z. Its two floor errors cost less than two. All three final bases contain both surviving triple cells, and their union becomes E union G after distributing the two private sets. In Lemma 7.47, the large E-trace makes the disjoint G-trace smaller than r/2, which is what licenses the global dichotomy. Its final partitions have integer capacities and integer demand.

9. **The final conditional theorem applies to all families.** The excluded interval `[.143r,.5r]` implies every pair intersection is at most r/4 or greater than r/2. Under an assumed large transversal number, a small pair exists by avoiding a large subset of one edge; a largest small intersection then exists because intersection sizes are integers in a finite range. Theorem 7.42 handles its two branches. The small branch invokes Lemma 7.18; the large branch either returns another small good triple or uses Lemma 7.41. Its additive four is strictly below the final additive ten.

10. **All budgets fit the stated rank range.** Local budgets are at most `ceil(6r/7)+9` or `ceil(6r/7)+4`, and the initial cap request costs less than `6r/7+2`. For r>=1000 these are at most r where that host condition is needed, and strictly below `K=ceil(6r/7)+10`.

I did not independently formalize the entire proof in a proof assistant, audit Python's implementation, or carry out a comprehensive literature-priority search. These are limits of this audit, rather than detected mathematical gaps.

## A reusable strengthening: force only one trace small

The strongest mechanism in the proof is the fifth-edge response in Lemma 7.41. It obtains new information before choosing the final two requests and therefore escapes the earlier simultaneous-allocation obstruction. The following hand-proved variant makes its local hypotheses less restrictive.

**Generalized one-trace matching lemma.** Let E,F,G,H be r-edges with all triple intersections empty. Write

\[
X=E\cap F,\quad B=G\cap H,\quad Y=E\cap G,\quad Z=F\cap G,
\quad A=F\cap H,\quad C=E\cap H.
\]

Let their sizes be x,b,y,z,a,c; put `s=y+z`, `t=a+c`, and `u=s+t`. Suppose an integer h0 and a nonnegative real delta have the following global trace implication: every family edge I with `|G intersect I|<=h0` has `|G intersect I|<=delta`. This implication follows, for example, from an already proved intersection gap. Set

\[
p=\max(0,r-h_0-s).
\]

If an integer budget T satisfies

\[
p\le b,\quad u+p\le T,\quad x+\delta\le T,\quad
x+b\le2T,\quad 2x+b+u+p\le3T,
\]

then three more avoiding responses produce a bad seven-tuple. The same conclusion holds using H in place of G, with `p=max(0,r-h0-t)`. With a common gap one may therefore use `p=max(0,r-h0-max(s,t))`.

**Proof.** Put `q=min(x,T-u-p)`. Choose p points from B and q points from X, and request I avoiding these points and all of `Y union Z union A union C`. This costs `u+p+q<=T`. It avoids s+p points of G, so `|G intersect I|<=h0`. Consequently

\[
d:=|B\cap I|\le\delta,\qquad x_I:=|X\cap I|\le x-q.
\]

Choose `B1 subset B` containing `B intersect I`, of size `min(b,T-x)`. This is possible because `T-x>=delta>=d`. Use the two final requests

\[
D_1=X\cup B_1,\qquad D_2=(X\cap I)\cup(B\setminus B_1).
\]

The first costs at most T. The last two displayed hypotheses imply `2x+b-q<=2T`: if q=x this is `x+b<=2T`; otherwise it is `2x+b+u+p<=3T`. If b<=T-x then `|D2|=x_I<=x<=T`; otherwise

\[
|D_2|\le x-q+b-T+x\le T.
\]

The candidate pairs piercing E,F,G,H are precisely the three products `X times B`, `Y times A`, `Z times C`. I misses both points of every pair in the latter two. For a surviving pair in `X times B`, either its B-point is in B1, in which case D1 contains both, or its B-point is outside I, in which case its X-point must belong to I and D2 contains both. The final two avoiding responses eliminate these pairs. This proves the claim integrally. □

The original lemma forced **both** G- and H-traces small, but only one is needed to bound B intersect I. This observation gives a smaller first request when s and t are unequal. It supplies a new sufficient local region; it does not alone improve the general bound.

For a continuous normalized region use `p=max(0,1-h-s)` and delta=ell for an established gap `[ell,h]`. For a uniform integer realization, replace hr by its floor and use a budget increased by one: p increases by less than one, and each of the displayed budget inequalities remains satisfied. The host `p<=b` is also preserved when `1-h-s<=b`, since `r-s-b` is an integer.

The separately written script `p644_agent_audit_generalized_matching.py` checked 98,432 bounded integer allocation instances, including every permitted residual occupancy in each tested instance. These are regressions supporting the hand proof, not a replacement for it.

## Bounded test against the existing obstruction

At the requested point `(x,y,z)=(.4,.086,.372)r`, the initial whole-core request costs `.858r`, exceeding the target `.856r` by exactly r/500. Therefore this generalized matching lemma cannot be reached through that fourth request. A surviving triple cell must be handled, or the initial request geometry must change.

I also tested four adjacent slices with y=.084,.082,.080,.075 using an unpadded whole-core request and all 24 orientations of the four-edge configuration, together with each established gap and the maximum-small dichotomy. Each had an exactly verified rational response outside this lemma's sufficient regions. The resulting data are in `logs/astra_agent_audit_generalized_matching.json`. This only obstructs using this lemma by itself: the saved responses are in fact handled by existing simultaneous three-request templates with respective certified feasible budgets 569/800, 761/1000, 761/1000 and 1419/2000. They are not hard configurations for the full method.

The realistic next use is to add the one-trace variant to a mixed local menu, especially when another request already produces unequal small-pair sums. A direct attack on the .858 core still requires controlling its remaining triple-cell star. Repeating the existing whole-cell fifth-request search is not justified: the already recorded obstructions cover that experiment.
