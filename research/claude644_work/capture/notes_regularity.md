# notes_regularity.md  (agent key "regularity", wave 11, 24 Sep 2026)
Target: structure-vs-randomness decomposition for k-set families on N = O(k) points, strong enough for pillar (II).
Read: DEEP_BRIEF, CONTEXT, RESEARCH_LOG (all), handback s0, notes_randomside (c1-c11), notes_tameness (t0-t12),
notes_dense (ckpt 2,7,8), notes_tcglobal (K4/TC*), randomside2/cert_fano_staircase.py + fano_janson_sym.py.

## [r0] Orientation (what the existing results force on any regularity lemma)
* Theorem R (tameness [t4]) + Prop S [t1]: e^{-ck}-sparsification keeps (7,2) and tau up to O(ck), destroys robust
  profiles at rank <= (1+gamma)k for EVERY bounded partition.  Hence any lemma "RL_pi > eps k & Psi(H,pi) => bounded
  refinement raises a bounded energy by delta k" together with "not Psi => bad tuple" yields tameness (II) and so 644
  (dense range).  Conversely 644 makes both statements vacuous.  => the task's target pair of lemmas, with ANY
  compatibility notion Psi, is EQUIVALENT to 644 in the dense range; its whole content sits in "not Psi => bad
  tuple" applied to sparsified non-tame counterexamples, i.e. Psi must be a Janson-type (relative-random) notion and
  the bad tuple must come from an entropic continuous theorem (Th_ent) -- exactly the [t8] reformulation.
* [c4]: KL/entropy-increment energies cannot see ATYPICAL profiles (those where bad tuples live): emptiness there
  moves the energy by e^{-Omega(k)}.  So the "energy" half is only useful at BULK profiles; the pseudo-random half
  must be a counting statement at exponential precision.
PLAN: (1) formalise the KL energy D(pi) (monotone under refinement, bounded, increment lemma at bulk profiles,
terminal 'bulk-regular' statement) [FULL_PROOF]; (2) Obstruction: bulk regularity is blind at exponential scale
(explicit); (3) the density-function model M_pi = (pi, c_pi) and the FIRST-MOMENT TRANSFER tau(H) <= tau(M_pi)+o(k)
for every pi [FULL_PROOF]; (4) relative Typed Janson [FULL_PROOF]; Th_ent(p, c(.)) conjecture in static form and
the precise residual (II_ent) (count-regularity), sparsification-stable; (5) TESTS: complete, random (Thm 1*),
type-closed, PG(2,q), LINEAR CODES -- for codes a NEW theorem: FOURIER-JANSON lemma (second moment over a random
code; Janson's coordinate marginals J become ALL subspaces U <= F_2^7) + subspace-staircase certificate
=> random syndrome families are not (7,2) whp once tau > 3k/4 + O(log k)  (script regularity/code_fourier_cert.py).

## [r1] checkpoint 1 (start): writing the code certificate script first (it is the only computational item).

## [r2] checkpoint (resumed session, ~15:00): context re-read; note has NO regularity/energy-increment material (grep:
## only Lemma 7.5 l.283-295 and the 'regularity reduction' remark l.7348) -> novelty clear.  Referee w10 F4: Theorem R
## does NOT exclude regularity with tower-type p(eps) or partitions adapted to the family (R2(a) is for partitions fixed
## before sampling; R2(b) needs ln p < K_s c(eps)).  That loophole is exactly the room for this agent's lemma.
## The earlier session wrote regularity/code_fourier_cert.py (Fourier-Janson certificate) but the derivation ([r3]-[r5])
## was lost with the cut; reconstructing below.
