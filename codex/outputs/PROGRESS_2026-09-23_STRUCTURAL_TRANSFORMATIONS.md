# Erdős 644: actual transformations and global obstructions

The general three-quarter bound remains unproved. This continuation is
PROGRESS: it adds actual-row transformations and exact global constraints,
not a new general coefficient. Both note copies now contain7.170–7.173.

## Actual Fano transformation

For an empty-common-intersection six-tuple define Phi=3N-p, where N is its
active union size and p is its piercing-pair endpoint count. In the focused
clean profile, a response G avoiding P except in defect types123,124 gives

    Delta Phi = 3o-s

when G meets the two required A classes. Here s is its selected endpoint
trace and o is its mass outside the old union. The report also gives the
exact endpoint formula when one or both A traces vanish.

The entire new tuple stays inside a Fano containing structure. The selected
type123 and124 points are defects of the new cycles1235 and1246. There is
no exceptional support to delete. The eligible groups have masses
(c+x,c+y,c), with unequal bases and defect weights. The existing symmetric
eligible-profile theorem does not cover those new weights automatically.

For a=33b and the full two-defect set S, the first request has size109b.
If tau(H)>109.5b in a146b-uniform family, either this actual transformation
decreases Phi, or every response has s<=3o and the family of its outside
traces has transversal number>b/2. This uses the global high-transversal
assumption. The outside alternative has not been contradicted.

The root proved the full containing-type absorption and ran the new exact
checker once:

    python3 -S work/p644_actual_fano_pivot_check.py

It passed1296 support cases, including degenerate traces, and checks the
formula, class closure, new eligible masses and potential change. The
general statements have full hand proofs in agent_actual_fano_pivot.md.

## What the other two global routes establish

Section7.170 gives the exact condition for combining disjoint residual
cover exchanges: the combined replacement must meet every actual edge whose
critical-cover trace crosses both discarded parts. A growing example is
globally vertex-minimum and edge-critical, has two linearly rich covers
retaining the same prescribed pair, and fails that crossing condition.
It is not incidence-minimal and has only constant excess above3k/4, so it
does not obstruct a theorem using those remaining hypotheses.

Section7.171 proves that deleting a small anchor intersection costs at most
its size in tau, and either shortened anchor can be adjoined separately.
Simultaneous addition can fail. Every such failure has a common residual
intersection outside both anchors; with at most four residual rows, this
intersection must cover the whole residual family. A residual good triple
is available in the high-transversal regime. An explicit fixed-anchor
oracle still survives at ratio4/5 and minimum intersection1, so a proof
must use unanchored constraints as well. That oracle fails full(7,2) and
is not a counterexample to the desired theorem.

All three hand reports were read in full. No old certificates or solver
runs were repeated. A targeted primary-source literature check connected
pair extension with the classical arrow formulation in Remark2 of
[Gyárfás–Lehel–Tuza (1982)](https://users.renyi.hu/~gyarfas/Cikkek/15_GyarfasLehelTuza_UpperBoundOnTheOrderofTauCriticalHypergraphs.pdf).
Its fixed-rank maximum-order result does not supply the near-linear kernel
needed here; no new theorem from that search was used in the proofs.

## General host identity and exact menu outcome

The root extended the transformation identity to arbitrary positive star
weight c. Its new noneligible host has size k+2b+o-s. Thus an inside-union
response containing both whole selected defect classes would give a host
of size exactly k. Such a response is not guaranteed by the oracle, and
unequal eligible weights plus the endpoint gap still need control.

The bounded menu test for this inside-union, full-S branch is complete.
All35 integer deficit compositions fail the existing table at109.5b,
across360 ordered retained-four choices and both actual and containing-star
supports. Best containing-star residual is at least112.5b, above111b.
The root inspected and ran the new checker once; it uses exact fractions.
This rules out this menu at the tested points, not arbitrary allocations
or a broader strategy. No continuous simplex cover was attempted.

    python3 -S work/p644_pivot_fixed_menu_check.py

All bounded assignments and root commands have completed. No search
process remains running. The goal remains ACTIVE; nothing was published
and no notebook was modified.

Both main-note copies agree through7.173; SHA256 8c0f590debb6b7d4b98beb9194d5470387bda8f33cf801b0dfce62ab05f3ba37.
