# Final check of the post-referee fixes (six_sevenths_v3)

Scope: only the changes in `supporting/diff_after_referees.diff`. I confirmed that this file
is exactly `diff supporting/six_sevenths_v3_before_referee_fixes.tex manuscript/six_sevenths_v3.tex`,
with 36 hunks. Line numbers refer to the current `manuscript/six_sevenths_v3.tex`. No file
other than this report was modified.

**Verdict: the fixes are sound. There is no FATAL or SERIOUS finding. Four MINOR wording
problems and a few TYPOs remain, and the M-1 placeholder must be filled before the paper
goes out.**

---

## Findings

| # | Severity | Location | Finding | Fix |
|---|---|---|---|---|
| 1 | MINOR | Sec. 6, l. 829-830 (new, for L61-1) | "...and only then is $\lambda\ge0$" is **false**. In the early branch $\beta\ge\lfloor k/2\rfloor$ (35 ranks: 7-13, 15-21, 23-27, 29, 31-34, 37, 39-41, 45, 47, 48, 53, 55, 61, 69), $\lambda\ge0$ holds for 33 of them. It fails only at $k=11,13$ ($\lambda=-1$). Example: $k=7$ gives $h=1$, $s=0$, $r=0$, $\delta=2$, $\lambda=1$, and $\beta=3=\lfloor7/2\rfloor$. The late branch always has $\lambda\ge0$ (checked for $k<10^5$). No proof uses the remark. | "...only then are $\delta$ and $\lambda$ used, and only then do we need $\lambda\ge0$ (guaranteed by Lemma 6.1; outside (6.3) $\lambda$ can be $-1$, e.g. $k=11,13$)." |
| 2 | MINOR | Intro, l. 128-131 (for S8-5) | "The two static allocations do not close the triples with two medium cells, nor the triples containing a cell in $(T/2,k/2]$" is still false if read per triple. At $k=14$, $T=12$ ($\gamma=5$, $T/2=6$), Lemma 3.4 closes the two-medium triple $(6,6,5)$ with $(a_1,a_2,a_3)=(3,4,5)$ and request sizes 12, 11, 12, 12. It also closes $(7,5,5)$, whose cell 7 lies in $(6,7]$, with $(2,5,5)$. Both closures were verified by brute force on explicit sets. Lemma 3.1 fails for both in every orientation. The paper itself closes triples with a cell in $(T/2,k/2]$ by Lemma 3.4, in Prop. 6.2 Case 3 ($x=q>\alpha$). The class-level reading is correct. The referee's own suggested wording has the same ambiguity. | "The two static allocations do not close **all** triples with two medium cells, nor **all** triples containing a cell in $(T/2,k/2]$; we treat these with adaptive requests..." |
| 3 | MINOR | Sec. 8, l. 1040 (new) | "a pair attaining the largest small intersection $M$" misuses a defined term. *Small* means size $\le\gamma$ (Sec. 5, l. 594-596), but here $M>4t-3>t-\tfrac12$, so $M$ is medium. Line 114 avoids the clash by writing "small" in quotes. | "a pair attaining the largest pair intersection of size at most $k/2$ (the $M$ of Theorem 5.2)". |
| 4 | MINOR | Intro, l. 91-94 (for S1-2) | The convention sentence gives its reason for the wrong claim. "Property (7,2) implies property (6,2), and this holds in either convention, since a family with at most six edges has a transversal of at most $2\le k$ points..." Our at-most-(7,2) hypothesis gives (6,2) in both senses trivially, so the "since" clause is not needed for that. Read with both properties in the exactly-$p$ sense, the implication even fails for 6-edge families. The clause is really needed elsewhere: if EFKT's bound is stated in the exactly-six sense, which excludes or mishandles families with fewer than six edges, the small families must be covered separately. All the needed facts are present; only the logic is garbled. | "Property $(7,2)$ in our sense implies property $(6,2)$ in either convention. If $f(k,6)\le k$ is read in the exactly-six-edges convention, families with at most six edges are covered directly: they have a transversal of at most $2\le k$ points by property $(7,2)$ itself." |
| 5 | TYPO | Prop. 6.2, l. 890 (for P6-1) | "$x\ge h$ (for $k-d-x\le k-x$)" attaches the reason to the wrong inequality. The step $k-d-x\le k-x$ uses $d\ge0$, and $x\ge h$ is what gives $k-x\le T$. Also, $x\ge h$ already follows from $x\ge3h$ in the same list. | "$d\ge0$ and $x\ge h$ (for $k-d-x\le k-x\le T$)". |
| 6 | TYPO | Prop. 5.1 Case 3, l. 630 (for P51-1) | "as $z\le\gamma<\lceil k/2\rceil$": the strict inequality holds in Case 3, since $\gamma<y\le T/2\le k/2$. It does not hold for every $T$ allowed by the proposition: at $T=k$ with $k$ even, $\gamma=\lceil k/2\rceil$. Only $z\le\lceil k/2\rceil$ is needed. Optionally, l. 633 "$z+2g=\max\{z,\dots\}$" can now be written simply as $k+\epsilon-z$. | "as $z\le\gamma\le\lfloor k/2\rfloor$". |
| 7 | TYPO | l. 814 vs l. 992, 1000 (for S1-1) | Sec. 6 still says "For the rest of the paper fix $k\ge7$". Sec. 7 now treats $2\le k\le6$ and ends with "Finally, let $k\ge2$". Also, the "remark after Theorem 1.1" is an unnumbered paragraph, not a Remark. | Say "In Sections 6-7 (up to the padding step) fix $k\ge7$", and write "the paragraph after Theorem 1.1". |
| 8 | TYPO | Abstract, l. 42-43 | "medium size" is not defined in the abstract. This was already so before, but the sentence was rewritten. | Optional: add "(between $T-\lceil k/2\rceil$ and $T/2$)". |
| 9 | MINOR (editorial, blocking) | l. 1324-1325 (referee M-1, not addressed) | The placeholder "[The human authors must describe here the independent verification they performed.]" is still in the text. | The human authors must write this paragraph before anything is circulated. |

---

## Hunk-by-hunk check

Every inequality that a hunk introduces was re-derived by hand. The numerical claims were
also checked by script.

| Hunk (new lines) | Content | (a) correct | (b) refs/notation | (c) resolves |
|---|---|---|---|---|
| 36-37 | "improves the asymptotic coefficient 7/8 ... includes $k=7$" | Yes. FKW's bound is stated for $k\ge8$ (l. 68, and FKW Thm 2). | OK | S1-3 |
| 39-47 | New description of the static allocations | Yes. Prop. 5.1 Cases 1-2 use no dichotomy and close every triple with all cells $\le T/2$ except those with $y>\gamma\ge z$, which is exactly "two medium". | "medium" undefined in the abstract (#8) | S8-4 |
| 91-100 | $k\le6$ reduction, conventions, 21 values, $k=7$ | $\lceil6k/7\rceil=k$ for $k\le6$. The two bounds coincide for exactly 21 values of $k$ in 8..48: {8-13, 16-20, 24-27, 32-34, 40, 41, 48}. They are strict for the other 20 values, and strict for every $k\ge49$ (proof: for $k\ge56$, $k/56\ge1$; for $49\le k<56$, checked; script to $2\cdot10^5$). $f(7,7)\le f(7,6)=7$ is correct. `[FKW, Section 1]` was checked against `fkw1999.txt`: its Introduction states $f(r;6;2)=r$ from EFKT. | Wording of the convention sentence (#4) | S1-2 (partly, see below), S1-3 |
| 128-132 | "do not close ..." | Per triple: false (#2). Per class: true. | OK | S8-5 partly |
| 310-313 | Responses may repeat an edge | Correct. Lemma 2.1's proof discards repeats. Lemma 2.3 still holds for $K\in\{E,F,G\}$: e.g. for $K=E$ the list becomes $X\times G\cup Y\times F\cup Z\times P_E$, which is exactly (2.1). | OK | F1, F6 |
| 541-545, 977-985, 1200-1213 | $Q\to\Delta$ in Lemma 4.5 and Prop. 6.4 Case 3 | The rename is complete: no stray $Q$ remains in these places. $\Delta=(S-T)_+$ now means the same in Lemmas 4.5 and 4.7, Prop. 5.1 Case 4 and Prop. 6.4 Case 3. The remaining $Q$s (Lemma 4.1 cell $Z\cap K$; Prop. 5.3 Case 1) are local. I re-derived the Case 3 identities: $2x+2\Delta+k-y-z=4x+y+z+k-2T\le2T-3\epsilon$ and $2k+x-y+\lambda+\Delta\le3T-2\epsilon$. | OK | F2 |
| 629-632 | $0\le M\le\lfloor k/2\rfloor<k$; $g=\lceil k/2\rceil-z$ | Correct. $M\le T/2\le k/2$, and $z\le\gamma\le\lfloor k/2\rfloor$. | Justification wording (#6) | P51-1 |
| 678 | "For $k=7$ this is the case $M\in\{2,3\}$" | $h+1=2$ and $\lfloor T/2\rfloor=3$. | OK | T52-1 |
| 702-704 | Request size $x+\lvert Y\rvert+\lvert Z\rvert\le x+2M\le T$; enough points in $P_G$ | Correct. $T-x-\lvert Y\rvert-\lvert Z\rvert\le k-\lvert Y\rvert-\lvert Z\rvert$ because $T-x\le k$. | OK | T52-2 |
| 737-746 | Prop. 5.3 preliminaries; disjoint $E_1,E_2$ | Correct. Every later use has the response missing a point of the edge concerned: $G$ in Case 1 and Case 2, and $H$ with $x_1\in A\cap B$ and $c_1\in C$. The Case 1 argument is complete. | OK | P53-1, P53-2 |
| 826-830 | Stage ranges; $\delta,\lambda$ used only under (6.3) | Ranges correct. **"only then is $\lambda\ge0$" is false (#1).** | OK | L61-1 (with new error) |
| 890-891 | $x\ge h$ added | True but redundant, and the parenthetical is mislabelled (#5). | OK | P6-1 |
| 957 | "(as $y\ge z$) ... $\le4T-k\le3T$" | Correct: $2x+3z+y\le2S$ iff $z\le y$, and $4T-k\le3T$ iff $T\le k$. | OK | P6-2 |
| 992-993, 1000 | $k\le6$ pointer; padding for all $k\ge2$ | Correct. Padding uses Theorem 1.1 for $k$-uniform families of every rank $k\ge2$, and that case is now fully covered. | Conflicts with "rest of the paper fix $k\ge7$" (#7) | S1-1 |
| 1013-1014 | "do not appear to be relaxable" | Properly hedged | OK | S8-1 |
| 1021-1026 | Starting the first stage | $2-2q-(t-q)=2-t-q$; $2-t-q\le2t-1$ iff $q\ge3-3t$; $3-3t\le t/2$ iff $t\ge6/7$. | OK | (clarity) |
| 1030-1033 | "(in the alternative $S>T$ of Lemma 4.7)" | Correct. In the orientation $(M,z,y)$, $2k-z_L+\Delta\le2T$ becomes $2k+M+z\le3T$; at $M=t/2$, $z=1-t$ this needs $t\ge6/7$. | OK | S8-2 |
| 1036-1064 | Window, two kinds, experiments | See below. Correct, apart from terminology (#3). | OK | S8-2, S8-3 (partly) |
| 1112-1113, 1140-1141 | $\lvert C_2\rvert\le T-y-a-z$, $\lvert C_3\rvert\le T-z$; "$q+v=z$" | Correct. The second base has $q+y+a+u+v-\theta=y+a+z+u-\theta$ points, and $\le T$ is the lower bound on $\theta$. | OK | F3 |
| 1187 | "$T\le k$" | Correct: $T-S-p-t\le k-y-z$ iff $T\le k+x+p+t$. | OK | F4 |
| 1259-1260 | "$W$ may go to any request" | Correct. With $C\mapsto\{1,3\}$ and $W\mapsto\{1,2,3\}$, the Hall conditions are $\{C\}$ and $\{C,W\}$, and $\{W\}$ is implied. | OK | F5 |
| 1262-1264 | $K=E$ allowed; $K\ne G$; $c\le m$ | Correct | OK | F5 |
| 1287-1309 | $A,C\to Y',Z'$ in Lemma 4.8 | The rename is complete: no stray $A$ or $C$ remains. The products are $X\times B$, $Y\times Y'$ ($\{E,G\}\mid\{F,H\}$) and $Z\times Z'$ ($\{F,G\}\mid\{E,H\}$). The statement uses only $X,B$. | OK | F2 |

**Section 8 window claim, re-derived.** In normalized sizes, let $5/6<t<6/7$ and
$M\in(4t-3,t/2]$. This set is nonempty because $4t-3<t/2$ iff $t<6/7$.

- The $y$-interval $(t-\tfrac12,\min(M,1-\tfrac{t+M}2)]$ is nonempty:
  - $M>4t-3\ge t-\tfrac12$ iff $t\ge5/6$;
  - $t-\tfrac12<1-\tfrac{t+M}2$ iff $M<3-3t$.
- The $z$-interval $(3t-2-M,1-t)$ is nonempty iff $M>4t-3$.
- The constraint $z\le y$ can be met because $3t-2-M<t-\tfrac12$ (from $M>2t-\tfrac32$) and
  $1-t<t-\tfrac12$.
- So the conditions are compatible for every such $M$.
- The lower limit $5/6$ is needed. At $t=0.82$ and $M$ just above $4t-3$, the $y$-interval is
  empty.

For these triples the paper's lemmas fail in the orientations of Prop. 5.1:

- $S>M+(t-\tfrac12)+(3t-2-M)=4t-\tfrac52>t$ (using $t>5/6$), so the $S\le T$ alternative of
  Lemma 4.7 fails.
- The $S>T$ alternative fails because $2+M+z>3t$.
- Lemma 4.6 needs $z\ge1-t$, which fails.

A rational-grid check (about $1.6\times10^6$ samples) agrees. The second bullet is also correct:
$2-t-M>2t-1$ iff $M<3-3t$.

The experimental sentences agree with `FINDINGS.md` §6 and the logs in `strengthen/`:

- `probe_box_855.log`: the discard route closes the window-1 corners at $t=0.855$.
- `search1_corner.log` and `fable_probe_window2_855.log`: the window-2 points need more than
  0.855.

The logs cover 7 points and are continuous and certified.

---

## Referee findings not (fully) addressed

| Finding | Status | Acceptable? |
|---|---|---|
| M-1 (placeholder in Research assistance) | **Not addressed** (l. 1324-1325) | No. It must be filled by the human authors before circulation (#9). |
| S8-5 | Reworded, but the per-triple reading is still false (#2) | Needs the one-word fix "all". |
| L61-1 | Addressed, but introduced a false side remark (#1) | Needs a one-line fix. |
| S8-3 | Partly addressed. The method, budget ($t=0.855$) and outcome are now stated. There is no pointer to the code, which exists in `strengthen/` (`routes.py`, `search1.py`, `fable_probe_window2.py` and logs). | Acceptable, since no proof uses it. I recommend "code available from the authors" or a repository link. |
| S1-2 | The upper bound used and the convention remark are now stated, and the FKW §1 citation was verified. Whether EFKT itself was checked in the primary source cannot be seen from the text. | Acceptable if an author confirms the EFKT statement; fix the wording (#4). |
| F2 (third item: $R$ as a request name in Lemma 3.4 and as a core in Lemma 4.6) | Not changed | Yes. The referee listed it without requiring a change. |
| F7 | Not changed | Yes. The referee said no change is needed. |
| CC-1, CC-2 (check_cases.py) | Addressed outside the manuscript. `cor_hall` is asserted at the Cor. 3.2 call sites, and `T+B-k <= C-1` and `k-x+y <= T` are asserted. I re-ran it: ranks 7..120, 2,008,516 branch checks pass. | n/a |
| M-2 (CHANGE_REPORT.md stale) | Addressed: it now says $k\ge2$ and has no placeholders. Only the remark "Ranks 8..200" (l. 75) remains. | Yes |

All other findings (F1, F3-F6, S1-1, S1-3, P51-1, T52-1/2, P53-1/2, P6-1/2, S8-1, S8-2,
S8-4) are resolved by the diff.

---

## Compilation

I ran pdflatex twice on an identical copy of `manuscript/six_sevenths_v3.tex` in the scratchpad,
so that the build files in `manuscript/` were not touched. The output is the same PDF: 18 pages,
390,338 bytes.

- 0 overfull and 0 underfull boxes.
- 0 undefined references or citations.
- No "Rerun" or other LaTeX warnings.

The existing `manuscript/six_sevenths_v3.log` is clean as well.
