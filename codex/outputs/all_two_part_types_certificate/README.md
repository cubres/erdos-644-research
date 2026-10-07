# Every closed two-part type set: the 3/4 threshold

Theorem 7.75 and Corollary 7.76 in the research note prove the continuous 3/4 threshold for any closed admissible type set over two parts, without convexity or intersectingness. Every finite k-uniform (7,2)-family invariant under permutations within two parts satisfies tau <= floor(3k/4)+28. The unrestricted Erdos problem remains unresolved.

Replay from this directory:

```sh
python3 -B -S p644_two_part_gap_check.py
```

The standard-library checker reconstructs all allowed mathematical assumptions, checks the explicit capacity constructions and their maximum of fourteen parent cells, and verifies 640 rational duals covering every linear case. No numerical solver, SMT solver or external proof checker is needed. The hand gap lemma and rounding proof in sections 7.76-7.77 of the note are essential parts of the argument.

Discovery scripts are included separately. The complete 715-support catalogue is not needed: positive witnesses for the 42 constructions used by this proof are included. No public posting has been made; external mathematical review and priority checks remain outstanding.
