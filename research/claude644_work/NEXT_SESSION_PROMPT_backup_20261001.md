Continue my research on Erdős Problem 644 (f(k,7) = (3/4+o(1))k; property (7,2): every subfamily of
at most seven edges has a transversal of at most two points). Work autonomously; do not contact anyone,
submit, or publish. Keep all durable files under ~/Documents/Clauding/erdos-hunt/claude644_work/ (never /tmp).

START BY READING (in this order):
1. claude644_work/typeclosed3/STATUS.md — everything verified so far on Th(3) (3/4 for all 3-part
   type-closed families) and the exact open core.
2. claude644_work/typeclosed3/notes_caseA.md (latest case-A progress), notes_structure.md, notes_strategy.md.
3. claude644_work/tameness/notes_counting.md (route C: model-tameness, the missing counting lemma) and
   claude644_work/tameness/notes_tameness.md (routes A/B: (7,2)-preserving compression, saturation + twins).
4. claude644_work/capture/PROOF_ARCHITECTURE.md (the two-pillar reduction: 644 <= Th_Z(p) + tameness;
   tameness is EQUIVALENT to the dense conjecture).
Background already finished (do not redo): the six-sevenths paper v3 in
claude644_work/fable_publication_revision_20260926/ (f(k,7) <= ceil(6k/7) for all k >= 2, incl. new k = 7).

GOALS, in priority order:
A. Finish Th(3). Verified: Theorem B (two covering classes => V tuple), Theorem TP (a part with
   x_i <= 2*eta => two-type tuple; 64 exact certificates), L3-L5, Corollary C, Lemma SEP (separated regime
   x_i + x_j >= 3/2 is rigid: disjoint classes, blockers = class minimisers). Open: case (A) with all parts
   > 2*eta — the separated regime (try a hand proof or an exact, independently re-checkable certificate
   using templates Fano/Lemma 7.63, V, the 42 two-type functions, K4, MP and the L5 line-pencil), then the
   non-separated regime. UPDATE: Theorem SEP(7/40) is certified (all pair sums >= 67/40) and its checkers were audited
   (audit_sep_tameness.md: valid; fix e_i > eta to e_i >= eta, all leaves survive). Remaining: the boundary layer
   3/2 <= min pair sum < 67/40 (brute certification ~1e8 nodes: prefer a HAND argument at the pair boundary
   x_i + x_j = 3/2, where all surviving adversaries live) and the small-pair regime (see STATUS.md final
   report). Then think about Th(p) for p >= 4.
B. Tameness pillar. Route C's missing lemma: "(7,2) and tau >= (3/4+eps)k imply model-tame for some
   partition into o(k) parts" (an exponential-precision one-sided counting lemma, sharp at 3/4) plus a
   first-moment Th_fm(p). Energy/refinement arguments are provably dead. Foothold (audit-corrected):
   a counterexample is "Schur-free" (E1 Δ E2 not an edge when |E1 ∩ E2| = k/2) at EVERY N once
   tau >= 3k/4 + 2; what N < 2.355k adds is an exponential DENSITY DEFICIT — an attack there must use it. Routes A/B (notes_tameness.md [0]-[17]):
   Lemma SH (shifted (7,2) families have tau < 3k/4+5.5), Lemma BW (shifting-preorder width w gives
   tau <= 3k/4 + 2 sqrt(30Nw) + O(w) given Th_Z); symmetrizations/conditional shifts are dead. The
   sharpest target is WIDTH-CORE: a saturated (7,2) family with N <= Ck, tau >= (3/4+eps)k has a vertex
   set U keeping tau - eps k/2 with shifting-width <= delta k (a testable stability lemma; audit: needs
   2 sqrt(30 C delta) + 17 delta < eps/4). SH, BW and route C were audited (claude644_work/audit_sep_tameness.md):
   verified with minor fixes. Attack WIDTH-CORE.

STANDARDS: verify every claimed lemma line by line yourself before accepting it (earlier agents made
real errors that were caught this way); treat numerical adversaries at exactly the strictness tolerance
as suspect; exact certificates must be re-checked by an independent checker built from the statement.
Record verified results in STATUS.md (Th(3)) or the tameness notes, and update memory.

RESOURCE LESSONS: the Fable weekly quota was exhausted (resets 30 Sep) — use Opus agents until then;
the 5-hour session limit and network drops repeatedly killed agents, so every agent must append notes
incrementally and keep tool calls short (watchdog stalls after ~10 min without a tool call); resume
stopped agents with SendMessage rather than restarting them. Be honest about odds: Th(3) is plausibly
provable; a tameness proof would settle the dense Erdős conjecture and needs a genuinely new idea.
