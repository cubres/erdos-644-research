# New capacity-domain theorem from Claude's balanced-three-part pipeline

26 September 2026. Status: **exact computer-assisted theorem**, subject only to the already proved type-model reductions listed below. This strengthens the covered structured domain; it does not improve the general 6/7 coefficient or prove Erdős 644.

## Result already certified

Let C be a closed set of unit types over three parts of positive capacities x0 <= x1 <= x2. If x1 >= 7/6 and tau*(C) > 3/4, then C has a bad seven-tuple. Thus the sharp 3/4 continuous theorem holds throughout the domain with at least two part capacities at least 7/6, irrespective of the smallest capacity and without a balance hypothesis.

This is new domain coverage relative to the inspected Claude files. Claude had 18 certified quarter boxes, one certified tiny box near (0.16,1.19,1.21), and a newly closed but not certified quarter box [0,1/4] x [5/4,3/2]^2. The present result covers the whole smallest-coordinate interval, lowers the two-large-parts cutoff below 5/4, and includes all unbalanced cases.

## Exact proof and its semantic premises

Use Claude's Theorem L+ if at most two parts carry super-heavy types (a type is super-heavy at i if ci > 2xi/3). Otherwise every part has such types and hence xi < 3/2: a unit type cannot have ci > 1. Assume for contradiction C has no bad tuple. The pencil lemma then implies that every type is super-heavy somewhere.

For each i let gi be the infimum of ci over types super-heavy at i, and ei=xi-gi. Choose tau with 3/4 < tau < tau*(C). The proved gap and excess reductions give:

- 2xi/3 <= gi <= min(xi,1);
- tau <= e0+e1+e2;
- tau <= 3/4+ei for each i;
- every revealed type is light (ci <= 2xi/3) or has ci >= gi at each part, and has a heavy class somewhere.

The four regions used are (B) all pair sums ei+ej <= 3/4, and (Uij) ei+ej >= 3/4 for ij=01,02,12. Their union covers every parameter point. On B, the balanced pair-map lemma also supplies the restricted minimisers at thresholds hij = inf{ci : c heavy at i, light at j}. The checker refuses restricted-minimiser nodes in any Uij region. Outside the balanced regime, an empty restricted class is assigned hij=gi; the ordinary type inequalities are then vacuous for that class. For nonempty restricted classes hij is their infimum. MIN and RMIN limits are taken along a subsequence with a fixed heavy/light pattern; all displayed inequalities survive the limit, and closedness keeps the limiting type in C. This justifies boundary equality at 2xi/3 without assuming the open heavy classes themselves are closed.

In each region an exact rational proof tree covers x0 in [0,3/2] and x1,x2 in [7/6,3/2], with sorted capacities. A MIN/RMIN node reveals an actual limiting type (closedness). A REQ node requests an actual type below x-w, after proving 0<=w<=x and sum w<=tau<tau*(C). All seven possible nonempty heavy patterns are explored. A SPLIT covers both closed halfspaces. A FACET node either proves a support-capacity inequality or explores its opposite halfspace. Terminal templates are genuine bad supports: no two cells cover the seven rows. Feasibility is certified from all exact vertices of their capacity-dual polytopes. EMPTY leaves are rational Farkas certificates or prove tau<=3/4. Strict inequality leaves prove that a violating support inequality cannot coexist with tau>3/4.

The decisive new request is already in Claude's search6 engine: avoid the whole smallest part, with the remaining cost shared between the two other parts,

    w = (x0, (tau-x0)/2, (tau-x0)/2).

Validity is proved per region, with exact halfspace branching if needed. It forces a zero-smallest-trace type, which breaks the previous tiny-part obstruction where every revealed trace hovered near 2x0/3. The new work is a whole-domain search, followed by exact certification of its coverage.

## Certificates, reproducing the exact check

New artifacts are under:

`/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/claude_followup/balanced3/`

The certificate files and observed standard-library checker outputs are:

| File | Region | Leaves | Inequality certificates |
|---|---|---:|---:|
| full_7d6_balanced_cert.json | B | 403 | 10256 |
| full_7d6_unb12_cert.json | U12 | 150 | 2541 |
| full_7d6_unb01_cert.json | U01 | 10 | 21 |
| full_7d6_unb02_cert.json | U02 | 10 | 21 |

All four printed **PASS**. Additionally, `check_support_coverage.py` independently checks that the union of every used support is exactly 127, so every row occurs and the dual capacity polytope is bounded; it also checks pairwise noncovering, seven assignments, and records SHA256 digests. All four certificates printed SUPPORT_COVERAGE_PASS. Results are in `support_coverage_7d6.log`. The maximum number of parent cells in a row window among these certificates is 10. Check with:

```sh
python3 /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c/check5.py /Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/claude_followup/balanced3/full_7d6_balanced_cert.json /Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/claude_followup/balanced3/full_7d6_unb12_cert.json /Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/claude_followup/balanced3/full_7d6_unb01_cert.json /Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/claude_followup/balanced3/full_7d6_unb02_cert.json
```

The discovery runner `run.py` imports Claude's original search6 library and cache read-only. It never persists its cache or edits the Claude originals. Its arguments are low-box, high-box, regime, output path, CPU-second budget. Example:

```sh
python3 work/claude_followup/balanced3/run.py 0,7/6,7/6 3/2,3/2,3/2 balanced work/claude_followup/balanced3/reproduce_7d6_balanced.json 120
```

Exact certification uses the unchanged original `b3c/certify5.py`; standard-library checking uses the unchanged original `b3c/check5.py`, which reconstitutes all regions, exact support vertices, all node coverage, and every inequality certificate. Numerical search success alone is not a proof.

Also completed the pending inherited certificate for [0,1/4] x [5/4,3/2]^2: `r7_0_5d4_5d4_cert.json`, PASS with 181 leaves and 836 inequality certificates. Fresh broader 5/4 certificates are retained for provenance; the 7/6 result subsumes them.

## What remains open, precisely

The present theorem leaves the three-super-heavy regime with median capacity x1<7/6. In its balanced part, the current necessary conditions are xi<3/2, N>9/4, tau-3/4<=min ei, and all ei+ej<=3/4. The unbalanced remnants with x1<7/6 also remain. These are parameter-domain restrictions, not claimed counterexamples.

Claude's 3T theorem for one rigid representative per class cannot solve the remaining general case without an additional selection theorem: the concrete nine-type family of note 7.79 has all nine types essential and every triple has tau* below 3/4 (best triple about .641). Thus a minimiser triple does not inherit the covering hypothesis required by 3T. The classwise directional constraints control different types; forcing all desired directional coordinates onto one type costs more than the permitted tau request budget. These are the specific current selection obstructions, not evidence the desired theorem is false.

The global problem has additional gaps even after full Th(3): higher-dimensional type sets, the transfer/tameness gap (Claude's architecture notes identify tameness in that form as equivalent to the dense original problem), and no known reduction of the sparse ground-set range. No global 3/4 claim follows from this computation.

## Completed stronger cutoff and bounded failure to extend farther

The theorem above uses the strongest cutoff certified in this task: **7/6**, not merely the intermediate 6/5 result. All four 7/6 certificate files have now printed PASS. Balanced certification took 204.6 seconds and used 403 terminal leaves / 10256 inequality certificates; the exact checker then completed successfully. The U12 certificate has 150 leaves / 2541 inequalities. U01 and U02 each have 10 leaves / 21 inequalities. All support-coverage assertions passed separately. The intermediate 6/5 and 5/4 files are preserved as provenance.

The bounded 9/8 probe reached its 180 CPU-second cap (182 wall seconds), with 530 closed template leaves, 230 facet nodes, and no FAIL leaf encountered before timeout. It did not finish the covering tree. This is a branch-growth limit for this fixed search (facet depth 5, at most two further requests, no all-support MILP), not a mathematical obstruction or counterexample. The exact remaining log is `full_9d8_balanced.log`. No further cutoffs were launched, and no 9/8 theorem is claimed.
