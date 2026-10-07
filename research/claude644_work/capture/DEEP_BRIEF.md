# Deep-attack brief: Erdős Problem 644 (full three-quarter bound)

Read this file AND the shared context file CONTEXT.md in the same directory
(/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/).
Authoritative research note (read-only, 21938 lines; grep/sed specific sections only):
/Users/cubres/Documents/Clauding/erdos-hunt/note_644.md . FKW paper text: erdos-hunt/fkw1999.txt .

## Problem and status
f(k,7): max tau of a k-uniform (equivalently rank<=k) family in which every <=7 edges have a
transversal of size <=2. Erdős asked whether f(k,7) = (3/4+o(1))k. Status: OPEN (erdosproblems.com/644).
Known: EFKT 1992: f(k,3)=2k, f(k,4)=floor(3k/2), f(k,5)=floor(5k/4), f(k,6)=k (extremal = complete
families). FKW 1999: 3k/4 <= f(k,7) <= ceil(7k/8); parity family (4k-sets of a (7k+1)-set with odd
intersection with a fixed 4k-set) has tau = 3k+1 = (3/4)(4k)+1, so complete families are not exactly
extremal. Internal (unreviewed, computer-assisted) upper bound: 6k/7 + O(1). Lower bound 3k/4 from the
complete k-uniform family on 7k/4 - 1 points.

## Reformulations
* Venn: seven sets are not 2-pierceable iff for all points x,y some set misses both; iff the point
  "types" sigma(x) = {i : x in G_i} have pairwise unions != [7]; iff the complements of types form an
  intersecting family on [7]. Bad seven-tuples correspond to maximal intersecting families M on [7]
  (types must avoid M): Fano (types inside a line complement; the complete-family extremizer),
  "size <= 3 types" (no point in 4 of the 7 edges), "three pairwise disjoint edges" (nu >= 3), and many
  mixed ones (note 7.67 has a catalogue of bad supports).
* Blocks: C = {V \ G : G in H}. tau(H) >= t iff every (t-1)-set lies inside a block; (7,2) iff no seven
  blocks cover all pairs and points of V. Fano pair-covers need a block of size >= 3|V|/7.
* Coloring: a Fano-type bad tuple exists iff V can be 7-coloured (Fano points) so that for every line l
  the union of the four colour classes OFF l contains an edge.

## Tools proved in this investigation (see CONTEXT.md; all refereed)
* GT: three edges with empty common intersection span >= 2t-3 vertices.
* Theorem G: every set of <= 2t-4 vertices induces a 3-wise intersecting family; hence induced tau is
  <= |W|/3 and <= |E|/2 for any edge E inside W; tau(H[U]) <= ceil(|E|/2) + max(0,|U|-2t+4).
* Lazy protrusion Fano bound: tau(H^(m)_U) <= |U| - 4floor(|U|/7) + 3m.
* Disjoint edges F,G satisfy |F|+|G| >= 2t-3. Every edge E has a partner F with |E cap F| <= |E|-t+1.
  Triangle lemma (note 7.105): three edges pairwise meeting in <= k/4 force tau <= 3ceil(k/4).
* Normal form (note 7.87): minimal counterexample is edge-critical, every vertex pair lies in a
  minimum transversal, every incidence has a <=6-edge certificate whose 2-cover endpoint set P is a
  global transversal with P cap E = {x}; edges have size >= t - floor((k+4)/5) (>= t if intersecting).

## Known obstructions to methods (do not repeat)
* Finite (bounded-size) adaptive scripts: the project could not beat 6/7 that way; the problem is
  equivalent to an UNBOUNDED adaptive query game, so a proof must use unboundedly many edges/global
  structure.
* Vertex-set capture / Fano on an induced host is exactly as strong as finding a good triple of union
  < 2t (Theorem G), and local sparsity at scale 2t is compatible with tau = k in non-(7,2) families
  (projective planes). So any proof must also use non-pencil bad tuples (e.g. types of size <= 3).
* Atomic obstructions (note 7.126): private padding vertices; trace families that are not (7,2);
  type-closure increases tau but can destroy (7,2); merging preserves (7,2) but lowers tau.
* Continuous type-closed models: 3/4 proved for convex type sets and all closed two-part type sets
  (note 7.75-7.77, Theorem P); open for general type sets over many parts.
* Probabilistic union bounds over pairs/minimal transversals lose too much (complete family has
  tau_f = 7/4).

## Standards
FULL_PROOF only for complete rigorous arguments checked line by line. Exact certificates must be
exact-arithmetic scripts saved in the workspace directory above (claude644_work/capture). Numerical evidence, conjectures and
failed approaches must be labelled as such. Local relaxations are not actual families. Do not claim
the theorem from an outline. Do not write into the note or the Codex directory; scripts only in the
workspace (claude644_work/capture). Nothing is to be published.

## NEW TOOLS salvaged from the first attack (exactly checked; referee pending)
* GT* (sharp): three edges with no common point span >= 2t-2 vertices (union <= 2t-3 closes via the
  pencil with the parity placement of the odd halves). Tight: K_9^(5) (t=5, min good-triple union 8)
  and all (4m+1)-subsets of a (7m+2)-set. Scripts: twohost_logic_check.py, twohost_endtoend.py,
  twohost_pg_and_tight.py.
* TWO-COLOUR LEMMA (TC). Fano points p0,p1,q,r1,r2,r3,r4; lines L={p0,p1,q}, B1={p0,r1,r2},
  B2={p0,r3,r4}, C1={p1,r1,r3}, C2={p1,r2,r4}, g1={q,r1,r4}, g2={q,r2,r3}. Let E be an edge
  quartered E=E1uE2uE3uE4 (labels r_i). Let B1,B2,C1,C2 be ANY edges with
      B1 cap E in E3uE4,  B2 cap E in E1uE2,  C1 cap E in E2uE4,  C2 cap E in E1uE3,
  and X = ((B1 u B2) cap (C1 u C2)) \ E. If |X| + max(|E1|+|E4|, |E2|+|E3|) <= t-1, then H is
  not (7,2): label Q=X by q, O1=(B1uB2)\(E u X) by p1, everything else outside E by p0; the two
  global edges g1, g2 avoid Q u E1 u E4 and Q u E2 u E3. No host is needed; B,C may protrude
  arbitrarily. It detects projective planes (four lines through a point off E give X = {P}), so it
  escapes the PG(2,q) limit of Theorem G. Tight at K_9^(5). (446k random end-to-end checks.)
  Consequence in a counterexample: for every edge E, balanced quartering and admissible
  B1,B2,C1,C2:  |((B1 u B2) cap (C1 u C2)) \ E| >= t - ceil(e/2).
* THREE-OUTSIDE-CLASS LEMMA. For an edge E quartered as above, pairings pi_x={E1uE2,E3uE4},
  pi_y={E1uE3,E2uE4}, pi_z={E1uE4,E2uE3}: for EVERY partition V\E = Vx u Vy u Vz there are w and
  S in pi_w such that every edge disjoint from V_w meets S. (No tau hypothesis.) threehost_check.py.
* Anchored split lemma: for E0 = P u Q, edges avoiding P or edges avoiding Q are 3-wise intersecting.
* Mixed-Fano placement criterion and GF(2)/Bose-Burton density law (see RESEARCH_LOG.md).

## CHECKPOINTING RULE (mandatory)
Sessions can be cut off. Every 15-20 minutes of work, and after every significant finding,
append your current results (statements, proofs so far, what failed) to your own notes file
/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/notes_<yourkey>.md so that nothing is lost if you are interrupted.
