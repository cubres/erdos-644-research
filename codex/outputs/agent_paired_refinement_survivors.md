# Exact survivors of the low-c paired-refinement experiment

These are **method obstructions and discovery states, not counterexamples
to Erdős 644**. The ten- and twelve-row families below have transversal
number 2; the fourteen-row sample has transversal number 3. The purpose
is to determine which finite constraints a proposed proof still fails to
use. All point classes can be replaced by integer sets at a common scale.

The exact standard-library checker is
`work/p644_agent_global_interval_survivor.py`; its output is
`outputs/agent_global_interval_survivor.json`. Run it with Python 3.
It uses `fractions.Fraction`, not an optimization solver.

## 1. The five-pair construction on an interval

Normalize the rank to 1 and the ground-set size to 2. The old three
complementary pairs are coordinate cuts of the following six old cells:

| Old type | Size |
|---|---:|
| 000, 011 | 1/2 each |
| 100, 111 | c each |
| 101, 110 | 1/2-c each |

Take `1/8 <= c < 1/4`. Add complementary pairs `(G,H)` and `(J,K)`.
The following table gives their four subcell sizes within each old cell.
The columns mean membership in the two displayed edges; for example
`G,K` means in `G` and outside `J`.

| Old type | G,J | G,K | H,J | H,K |
|---|---:|---:|---:|---:|
| 000 | 1/8 | 1/8 | 1/8 | 1/8 |
| 011 | 1/8 | 1/8 | 1/8 | 1/8 |
| 100 | 0 | 0 | 1/8 | c-1/8 |
| 111 | 0 | 0 | 1/8 | c-1/8 |
| 101 | 0 | 1/4 | 0 | 1/4-c |
| 110 | 1/8+c/2 | 1/8-c/2 | 1/8-c/2 | 1/8-c/2 |

Every edge has size 1 and every designated pair is complementary in the
same ground set. A point in the `G,K` subcell of 011 and one in the `H,J`
subcell of 100 pierce **all ten rows**, so every seven-row condition holds.

The first response is legal: `G` avoids both small old cells, and its
traces on 000 and 011 are each `1/4 <= 1/8+c`. One can choose the initial
deleted subsets of size `3/8-c` in the `H` portions of these two cells;
together with the two small cells their total mass is exactly `3/4`.

The second response survives an avoidance stronger than the original
request. Delete all of 101 and subsets of 000 and 011 of size
`1/8+c/2` each, selected in their `K` portions. The total is

\[
 (\tfrac12-c)+2(\tfrac18+\tfrac c2)=\tfrac34.
\]

The `K` portions have size `1/4`, so these deletions fit throughout the
stated interval. They can include the two prescribed individual points.
There is no outside part of `G`, and `J` avoids all these deletions.

Number the old pairs 1,2,3, then `(G,H)` as 4 and `(J,K)` as 5. The ten
distinct triple counts are exactly:

| Triple of pairs | Q |
|---|---:|
| 123 | c |
| 124, 125, 134, 135, 145, 234 | 1/4 |
| 235 | 7/32+c/2 |
| 245, 345 | 9/32-c/8 |

These follow by multiplying the masses of opposite three-coordinate
cells. In particular every value is at least `c`. Repeated-pair triples
reduce to one or two complementary cuts and have `Q>=1/2`, or `Q=1`
for a single repeated pair. Thus the original triple really minimizes
`Q` over all triples of actual disjoint pairs in this finite family.
The only disjointness edges are the designated complementary pairs.

Its paired endpoint minimum is also the original `1+2c`. The full ten-row
pair graph, however, has only four components:

\[
 2K_{1/8,c-1/8}\;\sqcup\;2K_{1/8,1/8}.
\]

Consequently its full pair count is `c/4` and its full endpoint mass is
`1/2+2c`. These full-ten quantities are not automatically transversals of
an ambient family; the seven-row property gives that conclusion only for
endpoint sets of at most six selected rows.

## 2. A third full-budget request and a six-pair survivor

Delete the following entire old subcell unions:

\[
 D_A=(G\cap000)\cup100\cup111
       \cup\bigl(H\cap(101\cup110)\bigr).
\]

Its mass is

\[
 \tfrac14+2c+2(\tfrac14-c)=\tfrac34.
\]

This contains the two full 000--111 components, the 100 sides of the
remaining two components, and extra subcells that use the remaining budget.
It is not asserted to maximize the removed full-ten piercing-pair count.
It meets every one of the ten rows, so a response avoiding it is new.

Nevertheless it has the following exact response. Let `L` agree with
`G` outside 000 and with `H` inside 000; let `M` be its complement.
The two portions of 000 each have size `1/4`, so `L` has rank 1 and
avoids `D_A`.

For the new pair 6, the ten new distinct paired-triple counts are:

| Triple | Q |
|---|---:|
| 126, 136, 146, 156, 236, 246, 346 | 1/4 |
| 256, 356 | 9/32-c/8 |
| 456 | 5/16+(1/4-c)^2/2 |

Again all are at least `c`. The original paired endpoint minimum remains
`1+2c`; triples 146,246,346 have endpoint mass `3/2`, and the other new
ones have mass 2. A `G,K` point of 011 and an `H,J` point of 100 still
pierce all twelve rows. The full-twelve pair count is `c/8` and its full
endpoint mass is `1/4+c`.

These are explicit survivors of the displayed requests. They do **not**
establish survival against every legal whole-cell request, and no finite
closure assertion is being made.

## 3. A fourth request and a seven-pair sample at c=6/25 [C]

At `c=6/25`, make the symmetric full-budget request

\[
 D_B=(G\cap011)\cup100\cup111
       \cup\bigl(H\cap(101\cup110)\bigr).
\]

It also has mass `3/4`. Set

\[
 N=000\cup\bigl(G\cap(101\cup110)\bigr),\qquad O=U\setminus N.
\]

Both have rank 1, and `N` avoids `D_B`. This adds pair 7. The exact checker
verifies all 35 distinct paired-triple inequalities, all repeated-pair
versions, and all 3,432 seven-row subfamilies. The smallest paired `Q`
remains `6/25`. The original paired `P` is **no longer** minimal: triple
467 has `P=5/4`. All six-row endpoint masses, paired or unpaired, still
exceed `3/4`.

The fourteen rows no longer share a piercing pair. Their transversal
number is exactly 3, checked by finding a three-atom cover and verifying
that no pair of occupied atoms covers all rows. This is a finite sample
statement. An interval claim for the fourteen-row sample is not needed
and is not inferred from the five-/six-pair interval calculations.

## 4. The new global information: unpaired endpoint sets [C]

For the three exact samples at `c=6/25`, exhaustive standard-library
enumeration of **all** six-row subfamilies gives:

| Actual rows | Minimum six-row endpoint mass | One minimizing six-tuple |
|---:|---:|---|
| 10 | 37/25 = 1.48 | 1,2,3,4,5,6 |
| 12 | 31/25 = 1.24 | 1,3,4,5,7,11 |
| 14 | 99/100 = 0.99 | 1,3,5,7,11,14 |

Rows `2i-1,2i` are the two members of pair `i`. The checker retains the
exact occupied atom indices of every piercing pair for these minimizing
tuples.

For the fourteen-row minimum the pair graph is particularly simple:

\[
 \boxed{(G\cap011)\times(000\cup100),}
\]

with side masses `1/4` and `1/2+c=37/50`; their sum is `99/100`.
This graph uses the six actual rows `1,3,5,7,11,14`.

This is the next global quantity to use. In an ambient `(7,2)` family,
the endpoint set of **every** six-row subfamily is a transversal.
Therefore a continuation forcing such an endpoint mass to at most
`3/4` would finish this state. No assumption that the initial tuple
globally minimizes unpaired endpoint mass is needed for that conclusion.

The paired-Q inequalities alone do not capture the decreases
`1.48 -> 1.24 -> 0.99`. Conversely, these particular decreases are
features of the displayed responses, not yet bounds valid for every
possible adversarial response.

## 5. Verification boundary

The interval mass tables and the displayed five-/six-pair Q identities
are algebraic hand calculations. The checker reproduces them at exact
rational values. The exhaustive unpaired endpoint minima and the
fourteen-row sample's properties are marked `[C]` and produced by the
same standard-library script. The JSON records exact rational masses,
all paired profiles, minimizing unpaired tuples, and explicit covers.
No floating-point feasibility status is used for these statements.
