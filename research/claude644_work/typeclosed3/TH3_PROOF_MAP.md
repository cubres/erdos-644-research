# Th(3) proof map (main session, 1 Oct 2026) — the complete logical chain and the status of every link

THEOREM Th(3).  Let x in R^3_{>0} and K a closed set of unit types (0 <= c <= x, |c| = 1) with tau*(K) > 3/4.
Then K contains a bad 7-tuple.  (= Erdős 644 for 3-part type-closed families; PROOF_ARCHITECTURE.md N2.0.)

Notation: S_i = {c in K : c_i > 2x_i/3}, sigma_i = inf_{S_i} c_i, e_i = x_i - sigma_i, tau = tau*(K), eta = tau - 3/4 > 0.
Templates: Fano (Lemma 7.63: rows <= x, line sums <= 2x, total <= 4x per part), V(a,b), the 42 two-type functions W,
T3 = L5, R = one-request Fano.  Every template below yields a bad 7-tuple when its rows are types of K.

Status legend: [HAND] hand proof checked line by line by the main session; [CERT] exact certificate with an
independent checker, checker source audited and re-run by the main session; [PENDING] not yet available.

## Chain (suppose K is a counterexample: closed, tau > 3/4, no bad 7-tuple)

1. Covering fact R0 [HAND, notes_structure R0].  A box u with cost(u) <= tau contains a type of K (the free boxes form
   a relatively open set, so a free box of cost exactly tau could be enlarged).  All "requests" rest on this.
2. Pencil [HAND, checked 1 Oct].  Every type is super-heavy somewhere.  If g <= 2x/3, the box x - 3g/4 has cost
   3|g|/4 = 3/4 < tau, so it holds a type f.  Then g on a line and f on the quadrangle satisfy Lemma 7.63:
   3g <= 2x, g + 2f <= 2x - g/2, 3g + 4f <= 4x.  Hence K = S_0 u S_1 u S_2.
3. Class box [HAND].  [0, sigma) is free, so E := sum e_i >= tau > 3/4.  Also sigma_i <= 1 gives x_i < 3/2, and
   e_i < x_i/3 gives N > 3E > 9/4.  (So the clique regime N ~ 7/4, which has no slack, never occurs.)
4. Two covering classes are impossible [HAND: Theorem B, notes_structure].  With L3 [HAND] this gives case (A): a
   maximal free threshold box t >= sigma with three finite facets, pure facet blockers b^i (b^i_i = t_i, b^i_j < t_j),
   every type has c_i >= t_i for some i, and cost(t) >= tau.  All three classes are nonempty.
5. Corollary C [HAND, audit-corrected]: e'_i := x_i - t_i >= eta (NON-strict; the certificates were re-validated
   with the non-strict row, see 9).
6. Tiny part [HAND + CERT: L4, Theorem TP, 64 Farkas certificates re-verified].  If some x_i <= 2 eta, then there is
   a two-type tuple.  Hence all x_i > 2 eta.
7. Regime split (WLOG x_0 <= x_1 <= x_2: the hypotheses are permutation invariant; strategies need not be).
   Min pair sum = x_0 + x_1.
   (S) SEPARATED: x_0 + x_1 >= 3/2.  Lemma SEP [HAND] gives:
       - the classes are disjoint;
       - sigma_i > 2x_i/3 is attained by minimisers m^i;
       - t = sigma, the blockers are the minimisers, E >= tau.
       (S1) x_0 + x_1 >= 8/5: THEOREM SEP(1/10) [CERT: certs/gcert5_test_m10.jsonl.gz, the three minimisers only,
            menu F,R,V,W; check_gen_cert3_ns.py ERRORS 0; mutation tests rejected; main-session audit 1 Oct].
       (S2) 3/2 <= x_0 + x_1 < 8/5: [PENDING] incremental CEGAR runs (cegar5):
            mM_3_40 (pi0 = 3/40), mM_1_20 (pi0 = 1/20), mM_0 / mGM_0 (pi0 = 0).  A certificate at pi0 = 0 covers all of (S).
   (A) SMALL PAIR: x_0 + x_1 < 3/2.  Case-(A) facts from 4-6.  After L1 [HAND] K may be taken finite, so the
       minimisers are attained and sigma_i > 2x_i/3.  [PENDING] Certificates per band of x_0:
       - LWA0: x_0 in [0,1/5];
       - LWA1: x_0 in [1/5,2/5];
       - LWA2: x_0 in [2/5,3/5];
       - MWA3: x_0 >= 3/5 (automatically x_0 < 3/4).
8. Coverage: (S1) u (S2) u (A) = all ordered x.  The checker prints each certificate's REGION line; the union must
   be checked when the band certificates exist (check_cover.py is not yet audited).

## Facts the certificate checkers assume (BASE rows) and their sources
| row | source | status |
| pair sums >= 3/2 + pi0 (sep) / band rows (caseA) | region hypothesis | — |
| sigma_i > 2x_i/3 (strict), sigma_i <= x_i | Lemma SEP (ii) / finite K via L1 | HAND |
| x_i - sigma_i >= tau - 3/4 (sep), x_i - t_i >= tau - 3/4 (caseA) | Corollary C | HAND; NON-strict (use check_gen_cert3_ns.py) |
| sum (x_i - sigma_i) >= tau (sep), sum (x_i - t_i) >= tau (caseA) | step 3 / L3 (ii) | HAND |
| x_i > 2 tau - 3/2, i.e. x_i > 2 eta (caseA) | Theorem TP | HAND+CERT |
| t_i >= sigma_i, t_i <= x_i, blockers b^i_i = t_i, b^i_j < t_j | L3 (i) | HAND |
| 'cls' every type in a class (sep); 'sh', 'gap', 'bk' (caseA) | pencil, def. of sigma, L3 | HAND |
| requests 'val'/'ans' (valid => answered), strict and lex variants | R0 + minimality (closed K) | HAND (audit 30 Sep) |
| templates F, V, T3 | Lemma 7.63, V, L5 | HAND (audit 30 Sep) |
| templates R, W | R0 + Lemma 7.63; W catalogue re-verified from LP certificates | HAND (audit 1 Oct) |

## What remains for Th(3)
(S2) and (A): the certificates are computational, and runs are in progress (boundary agent, notes_boundary.md).
When they finish:
- run check_gen_cert3_ns.py (non-strict e-rows) on each final certificate;
- verify coverage (audit check_cover.py or check the REGION lines by hand);
- audit any new role/request kinds used (margin escapes, lex roles, grid requests) against their statements, as was
  done for R and W.
Then Th(3) is a theorem: hand lemmas 1-7 plus finitely many exact certificates.
