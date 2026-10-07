# New research results for Erdős 644 — 26 September 2026

The general three-quarter upper bound remains open. This session produces
a hand proof of the general six-sevenths bound with a better additive
constant, sharp three-quarter theorems for broad structured classes, and
new ways to force a contradiction in the remaining three-part case.
The main note contains the proofs, not only the statements below.

## Main new theorems

1. **The general bound now has a hand proof.** For every integer k>=7,

       f(k,7)<=ceil(6k/7)+1.

   Three rational pair-intersection exclusions and a hand finishing lemma
   replace the previous 256-stage / 18,270-node proof. The intermediate
   three-stage / 718-node certificate was independently replayed, but
   the final proof does not depend on it. All new scalar cases, the
   integer Hall allocation, and rounding were checked independently.
   A new integral triangle-allocation lemma then removes the rounding
   loss in S1a; sharper integer estimates in the remaining lemmas give
   the stated +1 constant and k>=7 range. The general-bound agent
   independently checked this strengthening. The leading coefficient
   remains 6/7.

2. **Arbitrary profiles, arbitrarily many large parts.** In the continuous
   model, let every vertex part have capacity at least 6/7 of the edge rank.
   Any closed admissible set of profiles whose type-closed family has (7,2)
   satisfies tau*<=3/4 of the rank. There is no convexity assumption and
   no bound on the number of parts or profiles. The coefficient is sharp.

3. **Uniform finite version.** Let H be k-uniform and invariant under all
   permutations within the parts of a vertex partition. If every part
   has at least 6k/7+6 vertices and H has (7,2), then

       tau(H)<=floor(3(k-1)/4)+84.

   If every part has at least k+6 vertices, the constant improves to 30.
   Both constants are independent of the number of parts.

4. **All partition-threshold families.** Let H consist of all k-subsets
   that meet at least one partition part in at least its assigned threshold.
   If H has (7,2), then

       tau(H)<=floor(3(k-1)/4)+36,

   without restrictions on part sizes, thresholds, or the number of parts.
   If there are at least six effective threshold parts, the stronger
   bound tau(H)<=7ceil(k/4)-k holds.

These results have full hand proofs and an independent proof check.
An exact-rational randomized construction check additionally exercises
the large-part constructions; it is a diagnostic, not their proof.

## Proof files and dependencies

- `paper_push_integer_sharpening.md`: the current general bound, the
  integral triangle-allocation lemma, and every changed integer estimate.
- `paper_push_six_sevenths_hand_proof.md`: the general proof, three rational
  interval exclusions, and exact integer bookkeeping.
- `paper_push_six_sevenths_hand_dependencies.md`: complete earlier hand
  lemmas used by that proof, extracted without the search chronology.
- `paper_push_three_theory.md`: the three-class selection argument and
  its extension to all numbers of super-heavy classes; contains every
  Fano coloring and capacity inequality.
- `paper_push_large_parts.md`: the four-class obstruction when part
  capacities are at least the rank, sparse finite rounding, and the two
  uniform finite bounds.
- `paper_push_uniform_threshold.md`: the three noncollinear Fano-point
  placement and the count that removes dependence on the number of
  threshold parts.

These are integrated into `note_644.md`, Sections 7.202 onward. Stable copies
are preserved for Claude in `claude644_work/codex_paper_push_20260926/`.

The shared earlier hand ingredients are the Fano capacity lemma (Section
7.65), the pencil construction and two-super-heavy-coordinate theorem L+,
Claude's explicit non-Fano V support, and the sparse seven-cell rounding
and two-part transfer (Section 7.199). Their use is stated inside the proofs.

## What this adds to a paper

The general six-sevenths result can now be presented as an ordinary
mathematical proof. A second substantive advance is a dimension-free class of arbitrary nonconvex
profile sets for which the exact conjectured leading coefficient is proved.
The finite transfer also has an error independent of the number of parts,
so the result applies when the partition itself grows with k. The threshold
theorem covers arbitrarily small parts by a different argument.

These results do not imply that an arbitrary hypergraph can be replaced
by a type-closed one while preserving both its transversal number and
(7,2). Such a reduction remains unproved. The other unresolved structured
case is arbitrary profiles with small parts.

## Further completed results and the remaining difficulty

The V4 support gives a full hand proof of the unbalanced three-part case,
including its equality boundary. In the balanced case, the new exact
median-capacity threshold is 9/8, down from 7/6: the original independent
checker passed 1,854 leaves and 57,474 rational inequality certificates.

A two-anchor exchange lemma eliminates an open neighborhood of an exact
three-minimum obstruction. At x=(106,106,112)/140 with anchors
(71,69,0)/140 and (65,0,75)/140, it proves tau*<=51/70<3/4. Coordinate
perturbations of size epsilon<=1/500 retain the bound 51/70+9epsilon<3/4.
An exact oracle finds the best one-request two-orientation argument among
at most 3^p residual boxes; the three-part instance needs at most 27.

A second exact state shows that this pair-only mechanism is insufficient.
For capacities (755,780,750)/1000 and three specified class minima, every
optimized anchor-pair request costs more than 3/4. A single Fano response
construction nevertheless proves the much stronger bound tau*<=457/1000
for every (7,2) superfamily containing those anchors. This gives a concrete
reason to combine response boxes from different constructions. The hand
proof and exact finite-menu replay are in `paper_push_three_theory.md` and
`paper_push_mixed_exchange_check.py`.

The remaining broad three-part envelope, after sorting, is

    0<x0<6/7, x0<=x1<9/8, x1<=x2<3/2,
    sum ei>3/4, and every pair ei+ej<3/4.

There are also solved subregions inside this envelope. A bounded search at
x=(3/4,3/4,4/5) saved 1,316 completed subtrees before its 300-second CPU
limit. It did not produce a complete point theorem or a counterexample.
Its sample frontier point already admits a V4 contradiction; completing
the entire remaining region is the outstanding task.

`paper_push_general.md` records new hand near-core allocation lemmas that
use the complete globally largest-small-intersection gap. They close the
old exact 0.856 menu hole and enable the new hand finisher. A separate
exact obstruction shows why one padded four-edge response cannot always
be completed by three simultaneous requests at 0.856. It does not exclude
other requests or later adaptivity. No general coefficient below 6/7 is
claimed here.

`paper_push_six_sevenths_barrier.md` explains why merely retuning the new
three-gap proof while preserving its cap and finishing requirements forces
beta>=6/7. It explicitly identifies which requirements a further
improvement must change; it is not an impossibility claim about all
avoidance arguments.

`paper_push_three_cert.md` records new exact domains, remaining domains,
and the resumable search. Completed domains are distinguished from active
searches. No finite grid or unfinished traversal is counted as a theorem.

The new hand graph reduction applies to three class minima at capacities
at least 3/4. Their slack-arrow graph has outdegree at most one. Empty
graphs, a single arrow, a directed path, and a directed three-cycle all
close. A converging fork also closes whenever both target pencil
inequalities fit, in particular whenever its target slack is at least
1/4. The remaining graphs are two-cycles, two-cycles with a feeder, and
forks with a small target slack and a failed pencil inequality. Full proof:
`paper_push_three_cycle_one_response.md`.

An explicit one-parameter family arbitrarily close to capacities
(3/4,3/4,3/4) defeats every Fano/V4 template using one occurrence of the
requested type. A short hand proof bounds all such requests away from
3/4. At a rational instance, even arbitrary repetition of the new type
does not repair the Fano/V4 menu: an independent standard-library checker
and a five-case hand bound prove every terminal request costs at least
0.756. These are precise template obstructions, not hypergraph
counterexamples. The new 2,2,3 support discovered from this obstruction
now repairs a whole parameter cone. At capacities
(3/4+t,3/4,3/4), for the displayed fan-in profiles with excesses
g>=2t/3, h,j>=0, g+h+j<=t and 0<=t<=1/50, it proves

    tau*<=3/4-g+j<=3/4-t/3.

Along the original thin family the stronger bound is 3/4-1.047t.
Explicit perturbations of every capacity and anchor coordinate by at
most epsilon<=t/100 retain the upper bound 3/4-1.047t+39epsilon<3/4.
The four-box argument is proved in full. Its new support formula has an
independent exact check of all 77,520 bases; separate replays passed 24
rational primal endpoint allocations and 600 inequalities at the five
vertices of the full parameter cone. Root read and replayed each new
checker and checked the outer hand argument. See `paper_push_new223.md`
and `paper_push_endpoint_repair.md`, integrated into Sections 7.217–7.218.

The near-critical capacity cube is still unproved. Its saved search ended
with 49 failed leaves; those leaves are not counterexamples. The new
support repairs the known thin obstruction, and can now be added to the
quantified search without relying on numerical infeasibility.

Section 7.219 adds a further hand V5 exchange for the remaining fork.
Two failed target pencils are impossible; exactly one can fail. An exact
eight-branch probe rules out one proposed simplified case split, while
the actual V5 boxes repair its witness at cost 19/72. This distinguishes
an inadequate sufficient criterion from an obstruction to the full
method. The rational replay passed independently. A complete fork theorem
is still missing.

No material has been posted or sent to anyone.
