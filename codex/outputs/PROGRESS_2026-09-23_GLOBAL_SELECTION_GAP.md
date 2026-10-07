# Progress and the remaining global selection gap

The full3/4 upper bound remains unproved. The general coefficient in the
working note remains6/7; the present continuation does not improve it.
The work makes the missing structural step more precise, but does not
support a completion percentage or a claim that a full proof is near.

## New hand results

Section7.174 resolves a specified subcase of the five-row shortening
defect. With anchor intersection size m, common five-row intersection
size c, total degree-four outside mass d, and no degree-three anchor
points, it proves

    tau <= m+(3k-c-2d)/2.

Thus c+2d>=3k/2 implies tau<=3k/4+m. The section also gives five
actual global covers before a response and ten afterward. The general
five-row defect is not closed. An explicit rank-bounded first-response
obstruction has tau exactly3, so it is not a high-transversal example.

Section7.175 gives exact endpoint formulas for all six actual row
replacements in the focused profile. Under global endpoint minimality,
if none of these replacements decreases Phi=3|union|-|endpoints|, every
response satisfies3o>=34b+min(s,b). This is stronger than the earlier
outside constraint and does not require uniform response ranks.
However, the stronger row3-through6 replacements leave the Fano
containing class. Their descent cannot be iterated using the previous
profile theorem. Straight induction on the outside projection has an
explicit rank mismatch, even if its local property were granted.

## A proposed shortcut is false

Section7.176 disproves a universal tau<=Phi/6+O(1) inequality by actual
complete uniform families. Counterexamples include a global Phi
minimizer, a minimum among degree-at-most-four tuples, and a tuple with
exact Fano support. A universal linear endpoint-gap correction within
Fano support requires coefficient at least1/3; this makes the large
endpoint-increasing pivots worsen that corrected expression.

This blocks the proposed scalar selection shortcut. It does not block
a theorem using actual endpoint minimality, criticality, or additional
structure. A valid link from the transformed witness to a small global
transversal remains necessary.

## Direct numerical probing and verification

Section7.177 records62 bounded arbitrary-code models: every empty-common
core containing G with one, two, or three further requests, at two
specified deficit vectors. No target-budget allocation was found.
All62 numerical solves completed, but no exact impossibility claim is
made. Existing outputs are cached; no old result was rerun merely to
check status.

The new exact support checker was inspected and run once. It passed
6,480 cases,38,880 pivots, and13,824 checks against Fano containing
models. All hand reports were read; the root corrected the distinction
between a common-point term and an outside-anchor term before integration.

Both copies of note_644.md agree through7.177, SHA256:

    0a9813eb5eb19fd8315a886590f3170e20cf5c82d2832aa3839f0e3e5dcd2165

All bounded assignments and root-owned processes have completed. Nothing
was published. The research goal remains active. Next useful work must
exploit joint compatibility of the new actual global covers, response
ranks, or genuine critical-certificate selection; merely minimizing Phi
or enlarging the same fixed-budget search does not establish the theorem.
