# Erdős 644: new results from Claude's September 25 work

26 September 2026. All work remains local. The unrestricted three-quarter
upper bound is still unproved. The project's previously verified general
computer-assisted coefficient 6/7 is unchanged.

## Located Claude's actual latest progress

The substantive new sources are in
`/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/`:

- `RESEARCH_LOG.md`: the research through September 25, including corrections
  and explicitly open branches.
- `paper_main.tex`, `sec_threshold.tex`: the 0.865 hand proof and the
  continuous threshold-family theorem.
- `templates_handproofs.md`: hand proofs replacing earlier two-part and
  two-threshold-box computer certificates.
- `notes_core.md`: the dual-pencil intersection inequality.
- `PROOF_ARCHITECTURE.md`: the precise transfer theorem and remaining gaps.
- `notes_balanced3cert.md`, `b3c/`: the unfinished three-part certificate
  programme, including its unbalanced remnants.

The new deductions below build on these sources rather than rerunning the
older research wholesale.

## Results proved in this continuation

### 1. Sharper hand proof of a general bound

For k>=1000,

    f(k,7) <= ceil(19k/22)+10.

This improves Claude's hand coefficient 173/200=0.865 to
19/22=0.863636..., but remains weaker than the existing computer-assisted
6/7. A new use of his S1 static template enlarges the local closing domain;
the final gap-extension proof then loses its difficult second branch.
An explicit one-parameter family of good-triple cell sizes shows why the
same six-lemma menu cannot go below 19/22 without an additional idea.

Full hand proof: `agent_claude_hand_sharpen.md`.
The authoring agent ran 726,516 exact arithmetic checks using
`work/check_claude_hand_param.py`; all passed. Root checked the new static
branch, finite gap argument, and obstruction algebra. These checks supplement
the hand proof, not replace it.

### 2. Stronger finite three-quarter theorems

For any k-uniform (7,2) family invariant under permutations within two parts,

    tau <= floor(3(k-1)/4)+12.

This sharpens the earlier additive constant 28 and now has a hand proof,
using Claude's newly located continuous two-part proof.

For threshold unions (an edge qualifies by reaching a prescribed threshold
in at least one part),

    tau <= floor(3(k-1)/4)+6s,

where s counts the effective threshold parts plus at most one part formed by
combining all nonthreshold parts. This removes Claude's padding assumption
and restriction to at least three boxes, and improves his additive 8p.
In particular it gives the coefficient 3/4 uniformly when s=o(k).

The new general mechanism has two steps: every continuous bad seven-tuple
can be represented with at most seven positive cells per part; perturb each
integer profile a to max(0,a-1+epsilon), then recover the exact original
profile by integer rounding. Conditional on the continuous theorem Th(p),
the same finite bound floor(3(k-1)/4)+6p follows for arbitrary p-part families.
Th(p) itself remains open in general.

Full hand proofs: `agent_claude_threshold_sharpen.md`, especially Section 7.
Root and the threshold agent independently checked the lattice perturbation
and its inverse rounding, including zero coordinates and clipped capacities.

### 3. Improved general transfer theorem

The same sparse-cell argument lowers Claude's universal profile shift from
14 to 6. Thus the transfer error becomes 7p instead of 15p, entirely by hand:

    tau(H) <= 3k/4 + EL + 7p,

conditional on the continuous type theorem. EL must be defined for the new
shift-six profile family; it is not the previous shift-fourteen EL. The
unproved assertion EL=o(k) remains a substantive gap.

Full hand proof: Section 6 of `agent_claude_threshold_sharpen.md`.

### 4. New exact three-part region

For a closed family of unit types on three parts, if at least two capacities
are at least 7/6, then a continuous transversal coefficient greater than
3/4 forces a bad seven-tuple. The smallest capacity is unrestricted and no
balance hypothesis is needed.

Four rational certificate trees cover the balanced region and all three
unbalanced regions. Root independently replayed all four with Claude's
standard-library `b3c/check5.py`: PASS, 573 terminal leaves and 12,839
inequality certificates in total. A separate support check confirms that
every used support covers all seven rows and has no covering pair.

Report: `agent_claude_balanced3_advance.md`.
Certificates: `work/claude_followup/balanced3/full_7d6_*_cert.json`.
The bounded 9/8 extension timed out with an incomplete tree; it is not a
theorem or a counterexample. All computation launched here has finished.

### 5. Stronger pruning and a fractional improvement

Retaining union sizes in Claude's dual-pencil inequality gives, when
4t>=3k+2 and t=tau(H),

    tau_f(H) <= 6k/t - t/(12k) <= 127/16.

The sharper implicit constant solves 6/w-3/w^3=t/k; its limiting value at
t/k=3/4 is approximately 7.93650, compared with Claude's 8.

More consequentially, the ambient constant fractional cover strengthens
the earlier private-row pruning theorem: arbitrary overlapping private
families with exp(o(k)) rows can now be eliminated for o(k) transversal
loss. The earlier condition was exp(o(k^(2/3))). The same argument prunes
o(k) low-trace layers simultaneously when their total row count is
subexponential. Any high-transversal family in this regime must have
at least (127/111)^(t-1) actual edges.

Full hand proofs: `root_claude_fractional_strengthening.md`.
The threshold agent independently checked all steps; the zero-row case was
made explicit before integration.

## Remaining gaps

The three-part region with median capacity below 7/6 still has unresolved
cases, and higher-dimensional continuous type sets remain open. Even a full
continuous type theorem would not establish the necessary structural
transfer to arbitrary families: Claude's architecture identifies the
tameness condition in its current form as equivalent to the dense original
problem. No general reduction of sparse ground sets to size O(k) has been
proved. The new pruning retains actual edges and linear excess, but does
not force rank reduction or restore a critical cover.

These are partial theorems with complete stated scopes. None is presented
as a proof of the unrestricted three-quarter bound.
