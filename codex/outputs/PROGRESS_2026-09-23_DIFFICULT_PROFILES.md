# Erdős 644: unequal witnesses and the remaining structural gap

The general three-quarter upper bound remains unproved. The current draft's
general coefficient remains 6/7. This continuation adds Sections7.163–7.169
to both copies of note_644.md. It does not establish that a full proof is
close, and no completion percentage or timetable is justified.

## Positive mathematical results

1. Section7.163 extends the clean-profile target bound to the whole interval
   a+2b<=c<a+3b. Two explicit requests give tau<=ceil(3k0/4). Together with
   previous results, the unresolved symmetric intervals for those arguments
   are a+b<c<a+2b and a+3b<c<a+5b. Arbitrary profiles remain open.
2. Sections7.165–7.166 prove separated critical-residual cover identities
   and a quotient cover-or-witness dichotomy. In an intersecting family a
   robust q-row witness obeys |type(x) union type(y)|<=q-2. Witnesses can
   change with y; a fixed-witness restriction cannot be imposed on the
   whole critical cover without another argument.
3. Section7.168 permits several shortenings simultaneously. For 7r<|E|-1,
   either an actual minimum cover retains the prescribed x,y and at least
   r+1 additional E-points, or at most six actual rows give a witness with
   1<=|P intersect E|<=7r+1. Rejection also supplies robust constraints or
   a witness row meeting E in at most 7r points. All proofs use actual rows.
4. Section7.169 proves tau<=109b for the concrete pure-cycle witness of
   Section7.157, assuming its endpoint count111b is the global minimum.
   The target at its ambient rank144b+1 is108b+1. The new bound narrows this
   conditional case but does not close it for b>=2.

## Precise limitations established

The focused clean profile c=a+4b has rank4a+14b and noneligible host size
4a+16b. For any actual edge E, writing ell=|P intersect E| and
z=|A minus E| gives the exact identity

    z-ell = |A|-|E|+|E minus (A union P)| >= 2b.

Thus changing the compared edge or minimum cover cannot remove the host
surplus. The entire Section7.161 host bound is weaker than the endpoint
cover bound on this profile, at every endpoint gap g>=0. A different
witness or a stronger inequality is required.

Sections7.164 and7.167 give scalable exact survivors for the fixed and
focused-adaptive requests at rank146b and target budget109.5b. They retain
the minimum six-row potential(111b,3669b^2). Their transversal numbers are
three and two, respectively. They disprove only the corresponding finite
request contradictions; neither is a high-transversal counterexample.

For the Section7.157 pure-cycle witness, the standard triangle table has
exact integer optimum109b over all four K4 triangles. The proof accounts
for singleton endpoints and first excludes empty light pieces. Rank
charging and redistribution within this table cannot reach108b+1 for b>=2.

## New verification performed

Run from the task directory:

    python3 -S work/p644_clean_profile_allocation_check.py
    python3 -S work/p644_heavier_clean_star_rank_survivor_check.py
    python3 -S work/p644_focused_response_adaptive_check.py
    python3 -S work/p644_pure_B_rank_escape_check.py

The root inspected each new or updated checker and ran it once; all passed.
They use exact integer or rational arithmetic. The first and fourth support
full hand proofs. The two finite-family certificates check all28 six-row
and eight seven-row subfamilies, ranks, budgets, and actual small covers.
No positive occupancy cutoff or numerical solver establishes these claims.
No old general-bound certificate was replayed. Preliminary agent claims
were not promoted when their singleton accounting was incomplete.

The main unresolved step is global: show that an arbitrary hypothetical
family above3/4 yields a witness amenable to the proved inequalities, or
derive a stronger inequality for the surviving profiles. Local finite
compatibility and numerical search failures do not supply that step.

The final bounded four-old-row search tested2356,2456,1235 with arbitrary
two-request cell splitting at b=1000. Completed outputs reported109.001b,
109.001b,109b against target108.00075b. These are numerical outcomes only,
not exact lower bounds, and do not exhaust retained-row choices. The root
inspected the model and outputs without replaying the solves. All bounded
assignments and root-owned commands have completed; no search is running.
The goal remains ACTIVE. No public posting or notebook mutation occurred.

Both main-note copies agree through7.169; SHA256 f6f682d7f186b6ca3645b8fd7329e5fdf580b586e5c1ed75f640caf124f7985e.
