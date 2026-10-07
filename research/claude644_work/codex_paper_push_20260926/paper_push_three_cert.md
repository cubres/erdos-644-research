# Three-part completion campaign, 26 September 2026

Current status: **the complete unbalanced three-part case is hand-proved by the independent theory agent and checked by root. The balanced case is proved whenever the smallest capacity is at least 6/7 (hand proof) or the median capacity is at least 9/8 (exact certificate). Full Th(3) is still open.** No unrestricted Erdős 644 upper-bound improvement is claimed here.

Latest advance: **a new exactly certified fourteen-form support closes an entire near-critical fan-in parameter cone**, with tau*<=3/4−g+j<=3/4−t/3 for0<=t<=1/50, g>=2t/3, h,j>=0, g+h+j<=t, and the anchors stated in `outputs/paper_push_new223.md`. A narrower one-parameter interval has the sharper bound tau*<=3/4−1.047t. The support formula passed an independent enumeration of all77,520bases; the interval passed24primal endpoint certificates; the cone passed600affine capacity checks at its five vertices. These results close an exact obstruction to the earlier restricted support menu. They add structural subcases inside the remaining balanced domain, without proving that whole domain.

The new balanced slab certificate `slab_9d8_fastcert.json` passed the unchanged checker: 1,854 leaves and 57,474 inequality certificates. Support-coverage checking also passed; SHA256 `1f86b1fb111a749bc3c33c6ba33acb2b54a143e6da6832b5dd77e3c23d1c112e`. Root independently replayed it. The strictness/witnessed-RMIN pipeline also passed an exact checker on the formerly difficult U12 neighborhood: `u12_hard_v4_cert.json`, 3,020 leaves and 18,015 inequalities, SHA256 `96c1e8311e6ece928102215182c8fcc7aa202aee53bb5ef265cec85aac4f622d`. That neighborhood is now subsumed by the full hand unbalanced theorem.

The remaining target is exclusively the balanced domain with x0<6/7 and x1<9/8. A focused depth-20 optimal-free-box probe at x=(3/4,3/4,4/5) exhausted its 240 CPU-second budget without a FAIL leaf. It checkpointed 1,113 completed subtrees; the saved terminal branch is exactly Farkas-empty. Its feasible immediate relaxation already fits V4. A subsequent300-second attempt with terminal anchor requests saved1,316 further subtrees and stopped without a FAIL leaf; its exact remaining region is preserved, but no exhaustive capacity-point certificate resulted. Historical milestones below retain their chronology and are superseded by this status paragraph where indicated.

## Historical first milestone: two unbalanced domain certificates

Retain the setup and semantic reductions of `agent_claude_balanced3_advance.md`: closed unit type family C on three sorted capacities x0 <= x1 <= x2, tau*(C)>3/4, all three super-heavy classes nonempty, thresholds gi and excesses ei=xi-gi. The present certificates cover the entire missing region x1<=7/6 in each of:

* U01: e0+e1>=3/4;
* U02: e0+e2>=3/4.

Their capacity box is [0,7/6] x [0,7/6] x [0,3/2], with sorted capacities enforced. Thus, combined with the existing theorem for median capacity at least 7/6, **both U01 and U02 are now closed for all capacities**. No restricted minimisers are used outside the balanced regime.

Artifacts in `work/paper_push/three_cert/`:

| Exact certificate | Checker result | Leaves | Inequality certificates |
|---|---:|---:|---:|
| missing_unb01_cert.json | PASS | 10 | 27 |
| missing_unb02_cert.json | PASS | 22 | 87 |

The unchanged original `capture/b3c/certify5.py` produced both certificates, and the unchanged standard-library `check5.py` checked them. The supplementary `check_support_coverage.py` also passed for both, including support union 127, pairwise noncovering, seven row assignments, and SHA256 digests; see `support_coverage.log`.

The exact certificates prove whole polyhedral domains, not sampled points or finite grids.

## Current domain map

Closed by the current hand proof: every unbalanced regime U01,U02,U12.

Closed in the balanced regime: min xi>=6/7 by the new hand proof; median capacity>=9/8 by the newly checked slab combined with the earlier >=7/6 certificate. Claude's 18 certified quarter boxes supply additional coverage inside the remaining broad envelope.

Still open: balanced points with x0<6/7 and x1<9/8 outside those inherited boxes. Necessary conditions include total capacity>9/4, gi>=2xi/3, tau>3/4, tau<=sum ei, and every pair ei+ej<=3/4.

## Pipeline changes

`resume_search.py` uses the original exact region builders and original tree format. Every completed search subtree is saved to a task-local SQLite database. The random seed at each state is a deterministic hash of that state's exact inequalities, equalities, revealed-type information, and search parameters. A CPU timeout therefore preserves completed siblings and can resume the unfinished traversal. The deepest outstanding polyhedron is separately written as a `.frontier.json` and `.frontier.pkl` at a normal budget timeout. Search success still requires an exact certificate and checker PASS.

`fast_reps.py` generates Fano row-to-type assignment orbits by first enumerating set partitions of the seven rows up to Fano symmetry, then injective colorings of partition blocks modulo their stabilizer. This avoids the previous m^7 temporary storage when a search reaches 10 or more revealed types. The generated orbit sets agree exactly with the original orbit sets through six types; all counts through nine match the original files and Burnside's formula. Ten, eleven, and twelve types give 72,610, 136,906, and 245,400 representatives, generated in about 0.14, 0.29, and 0.52 seconds in the recorded test. The generator changes discovery only, never the checked proof semantics.

## Strictness refinement, subsequently checked

The pencil lemma says every actual type t in a hypothetical counterexample is strictly super-heavy somewhere. In a fixed weak pattern P, all coordinates outside P satisfy ti<=2xi/3, and those in P satisfy ti>=gi>=2xi/3. Consequently

    sum_{i in P} (ti-2xi/3) > 0.

This holds for ordinary requested types and for MIN/RMIN limits: those limits lie in closed C, so an everywhere-light limiting type would itself contradict the pencil lemma. The old checker only used the strict hypothesis tau>3/4. `strict_types.py` additionally bounds the auxiliary strictness variable by each displayed positive form. Exact max-min certificates then discharge implications on this smaller, semantically justified open region. Request validity remains a plain non-strict implication on the entire parent region.

`strict_certify.py` and `strict_check.py` run the original certificate and checking code with only that documented strict-system extension. The extension was independently reviewed by root and its completed U12 neighborhood certificate passed the extended exact checker. Unfinished experimental trees carry no theorem claim.

## Historical search difficulties, not impossibility claims

The original pair/Fano-only search encountered unresolved nodes in U12 around x=(0.27,1.05,1.22). Its available revealed types may have all-support MILP optima above 1 in a bounded discovery run; this is not an infeasibility certificate. Forcing two directional zero-smallest-part requests improved some branches but did not then close the domain; the later full hand proof now does.

The balanced box [3/4,1]^3 encounters unresolved nodes near total capacity 9/4. In three representative nodes, all-support discovery found bad tuples with capacity scales about .9781, .9593, and .9575, despite the pair/Fano menu failing. Thus those particular nodes are a template-menu deficiency, not a candidate counterexample. The explicit points, row assignments, and maximal supports are recorded in `support_diagnostics.json`. Corner computation was suspended when root reported the stronger prospective hand theorem for min xi>=6/7, to concentrate effort on small parts.

At an early checkpoint the balanced slab x1 in [9/8,7/6], x0 in [0,7/6], x2 in [9/8,3/2] had passed more than 1,000 template leaves. It subsequently closed and passed the unchanged exact checker, as stated above.

Historical targeted runs covered small-part U12 with two directional zero requests, per-type strictness, and general bad support templates. They were bounded and checkpointed; all U12 discovery has now stopped because the hand theorem covers it.

## Historical discovery stage: genuine blockers and a closed slab

The balanced median-capacity slab 9/8 <= x1 <= 7/6 closed in discovery with no FAIL leaf. The first traversal saved 2,082 completed subtrees before its 480 CPU-second cap. The resumed traversal recovered large completed siblings and finished after another 137.53 CPU seconds. Exact certification and independent checking subsequently passed, as recorded in the current status above.

The repeated zero-trace answers were traced to a concrete discovery defect. The old `blocker_request` counted ti>=0 at a zero retained capacity as blocking a known type even when ti=0. Such a type is not blocked. The independent `strong_blocker.py` tests every known type against the actual retained vector AFTER slack allocation and requires a strictly positive exclusion margin. It also ranks later request candidates by this margin, instead of putting three potentially repeated zero requests first. This changes search heuristics only; all requests still require ordinary exact legality certificates.

At the recorded hard point x=(.14047619,.95512943,1.29998168), tau=.75459341, the old heuristic retained approximately (0,.64807082,.99292308); three known types had exclusion margin exactly zero. The corrected request retains (.00997477,.85974705,.77127208) at the same cost, and every known type has exclusion margin at least .09538237. It forces a middle-class type with genuinely small first trace. The full tiny-part U12 run then passed hundreds of template closures without FAIL, although its covering tree is not finished.

Root independently approved the strictness semantics: the finite list of positive per-type forms and tau-3/4 has a positive minimum, so the augmented max-min implication is legitimate. Exact output checking remains necessary.

## Historical hand reduction preceding the complete unbalanced proof

Claude's Lemma U closes a pair of class minimisers a,b whenever e_i+e_j>=3/4 and their trace sum at the remaining part l is at most xl (choose the orientation with smaller l-trace; that trace is then <=xl/2, so the second V inequality follows).

Since ei<=xi/3, the unbalanced condition gives xi+xj>=9/4 and hence gi+gj>=3/2. Thus

    a_l+b_l <= 2-gi-gj <= 2-(2/3)(xi+xj) <= 1/2.

Consequently the unbalanced domain is already settled whenever xl>=1/2, and more precisely whenever 3xl+2xi+2xj>=6. This applies automatically to U01 and U02 for sorted capacities. For this preliminary reduction alone, the remaining piece was U12 with x0<1/2 and 3x0+2x1+2x2<6; the later restricted-minimum V4 argument closes that piece too. The exact certificates above are consistent with, and can be replaced in an exposition by, this short corollary of Lemma U.

### Full hand proof, including the equality boundary

Assume all three strict super-heavy classes are nonempty, and put gi=inf{ci:ci>2xi/3}, ei=xi-gi. Nonemptiness and unit row size give xi<3/2, while 2xi/3<=gi<=1 and ei<=xi/3. Suppose ej+ek>=3/4. Then xj+xk>=9/4, so both xj and xk exceed3/4 (the other is strictly below3/2), and gj,gk>1/2.

By compactness of closed C, choose actual limiting minimisers a,b in C with ak=gk and bj=gj. A limiting minimiser need not remain strictly super-heavy at its minimizing coordinate; the inequalities below use only its equality to g and membership in C.

First aj<=1-gk<=ej. Indeed,

    ej-(1-gk) = (ej+ek)-1+(2gk-xk)
               >= -1/4+xk/3 > 0.

Symmetrically bk<=ek. Consider the two-type V support, whose required per-part inequalities for an oriented pair (s,t) are s+t<=x and 5s/4+t/2<=x. For orientation (a,b), at part j we have aj+bj<=ej+gj=xj. Also aj<=1-gk<1/2<2xj/3, hence

    5aj/4+bj/2 <= xj/2+3aj/4 <= xj.

At part k, ak+bk<=gk+ek=xk, and

    xk-5gk/4-(1-gj)/2
      = (ej+ek-3/4)+(1-gk)/4+(3/2)(gj-2xj/3) >= 0.

Thus 5ak/4+bk/2<=xk. The same calculations with j,k interchanged prove the needed inequalities at these two parts for the opposite orientation (b,a) too.

At the remaining part i, choose s to have the smaller i-coordinate, so si<=ti. If ai+bi<=xi, then

    5si/4+ti/2 <= si+ti <= xi,

because si/4<=ti/2. All V inequalities hold in every part, giving a bad seven-tuple of actual types.

Finally ai+bi<=2-gj-gk<=2-(2/3)(xj+xk). Therefore 3xi+2xj+2xk>=6 suffices. Since xj+xk>=9/4, xi>=1/2 is a simpler sufficient condition. Every displayed inequality allows ej+ek=3/4; only xj,xk>3/4 was needed for a strict comparison, and that follows from nonempty heavy classes even at equality. No perturbation of the capacity vector or unproved attainment in an open class is needed.

For sorted capacities x0<=x1<=x2, U01 implies x0+x1>=9/4 and hence x2>3/4. U02 implies x0+x2>=9/4 and hence x0>3/4, so x1>3/4. Their remaining capacities consequently exceed1/2. Only U12 can survive this lemma.

## Further pipeline advances and a formerly blocked neighborhood

`search_disjoint.py` replaces the overlapping FACET failure branches by an ordered chain of ordinary SPLIT nodes. Earlier template inequalities hold, the first failing inequality invokes the next strategy, and the all-pass branch ends in TMPL. Every template inequality is homogeneous, so this uses the original checker format verbatim. It avoids repeatedly proving the same region where several template inequalities fail at once.

The independent theory agent supplied the four-type V support on rows b,c,d,d,d,d,a. Its maximal cells, in that row order, are

    [3,60,77,86,92,106,108,113,116,120].

Its per-part cost is max(a,b,c,(a+b+c)/2,d+(b+c)/2,d+(a+b+c)/4). `v4_templates.py` scores all assignments of the four roles to available types. Every chosen assignment is serialized as an ordinary S template; the exact support-vertex checker proves its true capacity inequalities independently of the discovery scoring formula.

The witnessed-RMIN extension permits a restricted minimiser outside the balanced regime only after an earlier type-pattern label witnesses the restricted class. Its semantic invariant is precise: a REQ pattern is the genuine strict-heavy pattern of an actual chosen type; a MIN/RMIN pattern is the constant genuine pattern of the actual prelimit subsequence. Therefore a stored pattern with i heavy and j light proves the relevant class is nonempty, even if a limiting type reaches equality at its i-th heavy threshold. The checker maintains a separate stack of those ORIGINAL tree-edge pattern labels, so unrelated later facet inequalities cannot fabricate a witness. It does not infer nonemptiness from weak inequalities alone or from the summed strict form. Root reviewed this invariant.

With V4, disjoint splitting, witnessed RMIN, and genuine blockers, the whole U12 neighborhood

    [.13,.15] x [.95,.96] x [1.29,1.31]

closed in discovery in 136.97 CPU seconds. Earlier versions stalled there. Exact certification and the independent extended checker subsequently passed, as recorded above. The result is now subsumed by the complete hand unbalanced theorem.

At that historical point the larger U12 search still had unresolved branches. The zero-small-part minimum condition supplied the missing global information: if z1,z2 are minima within the two classes with c0=0, then tau*(C)<=x0+x1+x2-z1-z2. These z_i must not be replaced by the existing h_i0 thresholds. Root and the theory agent subsequently generalized this to restricted small-trace minima and completed the whole unbalanced case by hand. Generic U12 discovery has been stopped and its checkpoints preserved.

Bounded 300 CPU-second probes of the remaining balanced box x0<=6/7, x1<=9/8, x2<=3/2 encountered unresolved discovery leaves and timed out. No full Th(3) claim follows.

## Faster certificate production, same proof obligations

`fast_duals.py` first checks direct one-row certificates, then rationalizes numerical dual multipliers and verifies their coefficient identity and objective inequality using exact Fraction arithmetic. Any unsuccessful rationalization falls back to the original rational simplex. Numerical outputs are never accepted as certificates. `progress_certify.py` uses this producer and checkpoints only completed subtrees; the independent checker still verifies the complete final proof object. This avoids repeatedly running an exact simplex for elementary or already rational duals and makes long certification jobs resumable.


## Focused balanced depth probe: exact diagnostic

The final focused run used capacity x=(3/4,3/4,4/5), a maximum of 20 requests and 24 revealed types, disjoint failure branches, the full V4 four-role menu, the learned nine-cell four-role support, and an optimal finite-family free-box oracle. It stopped at its 240.88 CPU-second cap with no FAIL leaf: 171 template closures, 150 template chains, 92 request nodes, 98 optimal-free-box selections, and 1,113 completed subtrees saved in `balanced_point_optimal20.sqlite`. The maximal observed path had six successive requests after three class minima; the traversal did not reach the configured depth20.

The raw timeout frontier (`balanced_point_optimal20.frontier.json`) is itself infeasible. `frontier_diagnostic.py` found and exactly checked a rational Farkas certificate, stored in `balanced_point_optimal20.diagnostic.json`. Thus this frontier is not evidence of an obstruction: the budget expired before the routine processed an already-empty child.

Removing its final failed-facet constraint gives an exactly verified rational point of the parent region with tau=113/150 and minimum strictness margin1/300. Its nine revealed rows are approximately

    (.50666667, .49333333, 0)
    (.49666667, .50333333, 0)
    (.04737068, .41596265, .53666667)
    (.45929599, 0, .54070401)
    (.43037722, .56962278, 0)
    (.56295611, .42921339, .00783050)
    (.38760535, .57745328, .03494137)
    (.33777778, 0, .66222222)
    (.50666667, .14222222, .35111111).

The diagnostic file stores every coordinate as an exact rational and verifies every retained region constraint by Fraction arithmetic. The request path is `mmmfssfrffrsfssfrfsssfrssffrsssffrsf`, with the last constraint removed only for this parent-region diagnostic. This records a logically possible finite revealed configuration, not a hypothetical full-family counterexample.

Exact finite-corner enumeration gives revealed-family tau*=530319962632667237/847524768019723800, approximately .6257279818. Its maximizing free-box supremum is (type6-coordinate0,3/4,type2-coordinate2). Spending the remaining assumed global budget proportionally yields retained capacities approximately (.3580638454,.6928384321,.4957643892), with exact deletion cost113/150; all nine rows are excluded by a positive margin of at least .0295415062. Consequently the whole-family assumption still forces a genuinely new type. More strongly, root subsequently found an existing bad V4 tuple at this sampled point, as detailed next. The point was a witness for an unfinished region, not a survivor of every template. The concrete current barrier is covering-tree branching, not exhaustion of global-budget information and not a finite counterexample.

The oracle enumerates all corners given by capacity boundaries and positive revealed coordinates, respecting strict exclusion at positive thresholds and never treating zero as excluding zero. It then constructs an affine request with exact rational coefficients. Each completed proof must still pass the ordinary exact request-legality conditions throughout its entire parent region. When configured above11 types, this diagnostic run restricts its Fano menu to assignments using at most three distinct types to avoid exponential m^7 arrays; V4 and the mixed support retain all four-role assignments. This is an explicit discovery limitation, not an assumption in any checked certificate.


## Terminal anchor requests and the sampled point's existing tuple

Root found that the exact parent-region sample already fits V4 with row assignment [7,2,1,1,1,1,0]. `frontier_template_check.py` verified all support inequalities exactly, with minimum margin5828761589002837/301342139740346240>0. The tuple does not uniformly close the entire parent polyhedron: four of its 42 inequalities remain unproved there. The sample must therefore never be described as surviving the template menu.

Independently, the new hand two-anchor exchange lemma also closes that point using anchors0 and3 in one request. The least cost produced by the exact two-anchor oracle is279731885288840711/376677674675432800≈.7426293197<3/4. Retain u=(2776370717733889/376677674675432800,3/4,4/5). The two V4 downboxes have capacities approximately R=(.0073706803,.5133333333,.8) and S=(.0747413606,.75,.4964799318); R1+S2>1. Every unit response fits one orientation. The theory agent independently obtained the same rational request.

`anchor_pair_request.py` enumerates all27 capacity/threshold corner choices for each anchor pair. The discovery wrapper accepts `--anchor-pair`, prepends the least-cost exchange request to the request menu, and retains all original exact legality and final support checks. This heuristic needs no checker extension. The separate rigorous exchange lemma and exact oracle are in `outputs/paper_push_three_theory.md` and `outputs/paper_push_anchor_exchange.py`.

The single additional focused run, `balanced_point_anchor12`, finished at its300.75 CPU-second cap with TIMEOUT and no FAIL leaf. It saved1,316 completed discovery subtrees, selected64 anchor-pair requests, and closed267 direct template leaves plus147 template chains. This does not certify the capacity point: an exhaustive covering tree remains unfinished. No further discovery job is running.

Its exact saved frontier has11 types after8 successive requests, with path `mmmfcnfCsfCrfrsfrsfrfrfrfrsssfcnsfrf`. Unlike the earlier raw frontier, this region is genuinely feasible: `frontier_diagnostic.py` verifies a rational point with tau=2953/3930 and strictness margin11/7860 against every stored constraint. The finite revealed-family tau* is approximately .6621643639; a legal next global-budget request retains approximately (.4136935132,.4048567930,.7300502027), excluding all11 known rows by margin at least .0233290944. Exact values are in `balanced_point_anchor12.diagnostic.json`.

Again, that particular sampled point is already disproved by a present V4 tuple: roles(a,b,c,d)=(6,0,5,8), rows[0,5,8,8,8,8,6], with exact positive capacity margin24134664276404955378986529785143/389442156546317103501629108387130. It also admits an anchor1/anchor9 request of cost5677/7860<3/4. The retained vector for that request is (3/4,109/3930,4/5); its two boxes have cross-threshold sum1007/1965+4099/7860>1. These pointwise closures do not close the whole parameter region, which is the precise outstanding computational work. The checkpoint is a reproducible remaining branch, not a candidate counterexample and not a theorem that the approach fails.


## Reproduction index

All paths below are relative to this Codex workspace. Discovery changes were isolated under `work/paper_push/three_cert/`; the Clauding originals remain unchanged.

* Original-checker slab: `slab_9d8_fastcert.json`, producer log `slab_9d8_fastcertify.log`, replay log `slab_9d8_fastcheck.log`.
* Extended-checker neighborhood: `u12_hard_v4_cert.json`, replay log `u12_hard_v4_check.log`. Its metadata lists `strict-types` and `conditional-rmin`; it must be checked with `conditional_check.py`, not misrepresented as passing the unchanged checker.
* Resumable general producer: `progress_certify.py TREE.json CERT.json`; ordinary certificates are independently replayed with Claude's unchanged `capture/b3c/check5.py`.
* Focused checkpoint diagnosis: `frontier_diagnostic.py PREFIX`; exact row data and the original frontier's Farkas certificate are emitted as `PREFIX.diagnostic.json`.
* Exact sampled-tuple and whole-region distinction: `frontier_template_check.py PREFIX`; output includes the exact positive point margins and any region inequalities still unproved.
* Exact two-anchor point oracle: `anchor_pair_request.py DIAGNOSTIC.json`; optional search flag `--anchor-pair` supplies the corresponding affine requests.

A TIMEOUT, sampled feasible polyhedron, unproved template inequality, or bounded MILP incumbent is never labeled a counterexample or an impossibility theorem here. The remaining rigorous barrier is the absence of a uniform argument covering all balanced type configurations in the stated residual domain.


## A genuine restricted-menu obstruction

The theory agent supplied capacities(755,780,750)/1000 and three own-class minima(512,0,488),(404,521,75),(499,0,501), divided by1000. Their own-class slacks sum to751/1000. `three_minimum_barrier_replay.py` independently checks, using exact arithmetic, that all3^7 Fano assignments, all3^4 V4 assignments, and all42 minimal two-type support functions fail on these three rows. The best two-anchor exchange costs, including the trivial total-capacity-minus-one limiting bound, are83/100,257/200,817/1000, all above3/4.

This refutes the proposed shortcut “three minima already admit Fano/V4/a pair template, or one pair has a terminal exchange request of cost at most3/4.” Additional whole-family requests or a stronger support/selection lemma are mathematically necessary for that restricted menu. It is not a counterexample to Th(3), because the three-row subfamily is not asserted to have transversal number above3/4. The replay and its JSON output are included in the resume manifest.


## Exact six-anchor Fano plus V4 response oracle

The next bounded task supplied a substantially stronger terminal-query oracle. `fano_v4_partner_oracle.py` fixes the new response U at Fano row6 and enumerates all3^6 assignments of the other six rows to three known unit types. For each assignment it checks the four pencils that do not contain U. The remaining response caps are the minimum of x, the three vectors2x minus the two anchors on a response pencil, and4x minus the sum of the six anchors. Row transitivity makes fixing row6 exhaustive for this one-response Fano menu. Nonnegative boxes meeting the unit slice are combined with every three-anchor V4 partner box; dominated boxes are discarded.

The exact set-complement and free-box routines in root's `v4_escape_boxes.py` then calculate the union's escape orthants and the cheapest retained request box. Every generated cap, escape orthant, and accepted closed request is checked with rational arithmetic. Infimal requests that require an epsilon reduction are marked separately; an infimal cost at most3/4 is sufficient under the strict hypothesis tau>3/4. This is a reusable exact terminal-rule generator, not a proof that its rules cover all three-minimum configurations.

For the preceding restricted-menu obstruction, a single Fano partner box already improves the theory agent's mixed request: assignment[a,b,b,c,c,b,U] permits retained U=(298,780,750)/1000, for deletion cost457/1000. Its exact artifact is `three_minimum_barrier_replay.fano_v4_partner.json`. Thus the earlier obstruction applies specifically to the smaller menu and is overcome by a genuine extra request with this new Fano support.

The bounded rational probe separates configurations already contradicted by known-anchor tuples from those genuinely requiring a response. `known_anchor_bad.py` exhaustively checks Fano assignments, V4 role assignments, and all42 pair functions using exact integer arithmetic.

* Broad phase: the logged first1,200 states comprised939 already-bad configurations and261 genuine terminal-query cases. Every tested terminal cost was at most677/1000. The deterministic generator was replayed solely to classify these states, without rerunning the terminal search; its classification output is `classify_broad_partner_probe.json`.
* Focused phase:776 states had each capacity in[.7500,.7650], total own-class slack in[.7501,.7550], and off-diagonal traces zero or within.0050 of a simplex edge. Of these,211 already contained a bad known-anchor tuple; all565 remaining cases had an exact terminal request. The50 CPU-second phase's largest cost was3691/5000=.7382. Full rational inputs and receipts are in `fano_v4_partner_focused.json`.

The worst focused state is

    x=(7543,7504,7509)/10000,
    a=(5029,0,4971)/10000,
    b=(0,5006,4994)/10000,
    c=(0,4992,5008)/10000.

Its exact request retains(7543,7504,127)/10000, deleting3691/5000 from the third part. The complete partner union has four maximal boxes and five escape orthants, recorded with their support assignments in `fano_v4_partner_focused.worst.json`.

No counterstate survived this bounded probe. No universal claim follows from sampled inputs. The bounded probe suggested the following conjecture, **subsequently refuted by the exact thinner-band state below**: when three own-class minima satisfy x_i>=3/4 and the sum of own-class slacks exceeds3/4, either the known anchors already form a bad tuple, or their complete Fano/V4 one-response partner union admits a terminal request of infimal cost at most3/4. A proof of this conjecture, or an exact surviving configuration requiring further information, is the next mathematical target.


## Quantified cube attempt and a sharper exact obstruction

The attempted cube theorem used x_i in[3/4,153/200], sorted up to relabeling, and only the three class minima. `terminal_partner_search.py` selects one- or two-box partner recipes, splits every affine cap-validity, cost, and unit-slice covering precondition, and ends in ordinary REQ/SPLIT/TMPL nodes. It changes no checker rule. The complete discovery run `critical_cube_partners` finished after94.1 CPU seconds with49 FAIL leaves,233 constructed terminal recipes, and367 cached subtrees. It proves no cube theorem. Some failed discovery branches reflect the recipe search and boundary handling, so they are not all mathematical counterstates.

The independent theory agent then found an actual exact obstruction inside the cube, at

    x=(76000,75000,75000)/100000,
    A=(50849,0,49151)/100000,
    B=(0,50099,49901)/100000,
    C=(0,49951,50049)/100000.

The own-class slacks sum to.75003, below the focused probe's lower limit.7501. The three old types themselves have property(7,2): every third trace exceeds(4/7)x2, so the common-part covering lemma applies. The same fact rules out any already-bad tuple using only these old anchors, independent of the support menu.

A precise distinction matters. The initial partner oracle used the new response in exactly one row; its exact optimal terminal cost here is19771/20000=.98855. A single new TYPE may be repeated in the seven-tuple. `repeated_response_oracle.py` includes all204 four-color Fano orbits containing the response and all V4 role assignments containing it; the exact optimum decreases to501901/600000, still above3/4. Adding all42 two-type capacity functions and the previously learned mixed1321 support yields cost8321/10000=.8321, again above3/4.

`check_endpoint_menu_barrier.py` is a standalone exact replay. It reconstructs the22 maximal partner boxes and13 escape orthants, then independently enumerates864 corner-cut triples to verify the.8321 optimum. This is a rigorous obstruction to forcing the current template menu with one arbitrary budget request, even allowing the answer type to repeat. It does not exclude different supports, a second request, or a stronger extremal selection argument. It is not a counterexample to Th(3), since the old three-type subfamily has no asserted large transversal number.

## A new support bypasses a concrete escaped response

Root proposed the escaped response U*=(.498,.502,0). The bounded all-support MILP found a bad tuple in1.24 CPU seconds, and rational reconstruction independently verifies it. The row assignment is[A,A,B,B,U*,U*,U*]; C is unused. A raw-support primal/dual calculation gives exact required masses75749/100000,200699/300000,148953/200000, below the three capacities.

Thus this particular four-type family is **not** a counterexample: it exposes a missing three-role support. Its maximal parent cells are(11,19,46,54,60,78,86,92,101,102,106,114,120). `endpoint_u_all_support.json` records the discovered tuple; `endpoint_new_template.certificate.json` preserves exact primal and dual weights for an independent rational replay.

The reusable2,2,3 capacity formula is now complete: fourteen exact linear forms. `check_new223_facets.py`, independently of the original enumerator, checks all77,520 full bases by integer Bareiss elimination. It finds36vertices including the origin,24projected points including zero, and14coordinatewise maximal forms; runtime6.84CPU seconds. This proves the support formula for all nonnegative role loads by linear-programming duality.

The new support overcomes the previous exact menu obstruction. At the endpoint above, four partner boxes cover a retained request of cost73953/100000=.73953. More strongly, for the entire one-parameter family

    x=(3/4+t,3/4,3/4),
    A=(1/2+.849t,0,1/2−.849t),
    B=(0,1/2+.099t,1/2−.099t),
    C=(0,1/2−.049t,1/2+.049t),
    0<=t<=1/100,

every P7 continuous type family containing these anchors satisfies tau*<=3/4−1.047t. The complete short four-box covering proof is in `outputs/paper_push_new223.md`. `check_endpoint_interval.py` independently passed24rational primal endpoint allocations, which interpolate to prove capacity validity throughout the interval. This interval result does not rely on completeness of the fourteen-form enumeration.

The theory agent then generalized the same four support roles to the whole fan-in parameter cone: x=(3/4+t,3/4,3/4), A=(1/2+g,0,1/2−g), B=(0,1/2+h,1/2−h), C=(0,1/2−j,1/2+j), with0<=t<=1/50, g>=2t/3, h,j>=0, g+h+j<=t. The bound is tau*<=3/4−g+j<=3/4−t/3. `check_endpoint_cone.py` independently passes all600affine support-capacity inequalities at the five vertices of this parameter polytope and checks the covering inequalities. The separate new223 report states and proves the theorem, while `outputs/paper_push_endpoint_repair.md` contains the theory agent's derivation and robust extension.

These quantified positive theorems supersede the restricted-menu obstruction as a barrier for this family. They do not establish the full balanced three-part theorem or the unrestricted3/4upper bound. The near-critical cube remains open; its preserved failed discovery tree is not a counterexample. No further computation is running.
