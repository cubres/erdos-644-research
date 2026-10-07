# Erdős644: critical-witness progress, 22 September

The general3/4 upper bound remains unproved. This phase proves a new
conditional3/4 closing theorem and a stronger quantitative critical-witness
inequality. It does not improve the previously recorded general6/7 bound.
No public posting occurred.

## Positive proof progress

Section7.160 of `note_644.md` gives two explicit avoidance requests for an
entire two-parameter six-row profile. Its four noneligible Fano classes have
size a+3b; its three eligible classes have base size a and four single-
incidence-defect classes of size b each. The row size is k0=4a+12b.
If the global minimum endpoint count is at least3a+12b, then

    tau <= 3a+9b+1 = 3k0/4+1.

The requests cost3a+9b+e and leave at most3a+12b−2e possible endpoints;
e=1 gives the theorem. The argument permits arbitrary outside points and
does not require the secondary pair-count minimum. Full hand proof:
`outputs/agent_shared_witness_cover_addendum.md`.

Section7.161 permits arbitrary losses of incidences on the four noneligible
classes and arbitrary sizes for those classes. Keep the specified symmetric
eligible profile, let A be the noneligible host, and let
g=|P(F)|−p_min be the actual witness's endpoint gap. Then

    tau <= (3/4)max{k0,|A|}+g/2+1.

If these six ACTUAL rows certify an incidence x in E and k0<=k, put
z=|A\E|. The resulting global inequality is

    4tau−3k <= 3z+2g+4.

This needs no assumption that the other locally available clone edges are
actual. The rank-scale hypothesis k0<=k is substantive: deleting incidences
can leave all actual row sizes below k0. Full hand proof:
`outputs/agent_cleaning_descent.md`.

The unresolved bridge is existence of an actual certificate of this profile
with 3z+2g=o(k), or a valid decreasing exchange toward one. Incidence
minimality guarantees a witness, but does not prescribe its profile, endpoint
count, or external noneligible points. We have not proved that bridge.

Section7.162 adds a three-request triangle lemma for the symmetric profile
with arbitrary star mass c, cycle-base mass a, and path mass b:

    tau <= 2c+a+4b+1.

It reaches3k0/4+1 when c<=a+b, where k0=2c+2a+6b. The two-request theorem
handles c=a+3b, and the endpoint cover handles c>=a+5b. The intermediate
range, in particular c=a+4b, remains open for these methods. There is an
exact obstruction to the existing24-table orbit, but no exact infeasibility
certificate for all allocations or all strategies. Numerical searches
returning111b against a109.5b target are recorded only as discovery evidence.

## What the difficult-case probes established

* An entire8b reservoir of one-point repairs can coexist with the old nine
  rows. Requests excluding the previous singleton, a minimum cover, or the
  whole reservoir have explicit local responses. These finite families have
  transversal number three; they are not high-transversal counterexamples.
* In an incidence-minimal family containing an actual full clone block,
  every leaf shares one critical witness; a reservoir of at least six forces
  width six. Edge criticality charges the reservoir exactly against tau,
  but deletion leaves full-rank old rows and loses the desired excess.
* An exact815-row construction at b100 fits six such witness rows together
  with the old nine rows and all800 clones. All finite six-/seven-row tests
  pass. Its witness has precisely the profile closed by Section7.160, so it
  cannot extend to a high-transversal family retaining the global endpoint
  minimum. This distinguishes local compatibility from the global problem.
* Saturation gives an exact intersection formula for actual clones. A
  globally vertex-minimum saturated parity construction shows that many
  missing clones may each need a different witness excluding just one.
  Its excess over3k/4 is only1/4; it does not refute a statement using fixed
  positive proportional excess.
* Pair extension, even with minimum-cover basis exchange and a globally
  minimum six-row endpoint cardinality, does not imply that true minimum
  covers lie almost inside that endpoint set. The explicit obstruction is
  below3k/4 by an additive constant and fails exact global vertex minimality.

The common repair core has size144b−1, not143b. The removed point is an
exact singleton. This correction was applied before all new conclusions.

## New verification only

The root inspected and ran these new standard-library certificates:

    python3 -S work/p644_fourth_response_clone_reservoir_check.py
    python3 -S work/p644_fourth_response_mincover_check.py
    python3 -S work/p644_fourth_response_full_R_check.py
    python3 -S work/p644_shared_witness_transport_check.py
    python3 -S work/p644_shared_witness_cover_check.py
    python3 -S work/p644_shared_witness_two_request_check.py
    python3 -S work/p644_clean_profile_allocation_check.py

All passed. The reservoir check has382 six-row and466 seven-row symmetry
cases; each concrete fourth response has252 new six-row and210 new
seven-row cases. The815-row transport uses9949 six-row and16384 seven-row
symmetry cases. Its claims are finite b100 claims. The final closing theorem
uses exact(a,b,e) coefficient arithmetic and a full hand argument; it is
valid for all integers a>=0,b>=1. The109b+1 single-request lemma is superseded
on this profile by the new108b+1 two-request bound.

No old general-bound certificates or old fixed-five-row searches were
replayed. No numerical optimizer lower bound is being promoted to a theorem.

The additional new checker `python3 -S work/p644_heavier_clean_star_allocation_check.py` passed. It certifies a feasible111b request cost, not optimality or a target109.5b exclusion. All bounded assignments are complete; the goal remains active.
