# Three-part two-box certificate for Erdős 644

This proves a structured theorem, not the full Erdős problem: an intersecting continuous type-closed family, whose types are a union of two boxes sliced by the rank-one plane over three parts, has a bad seven-tuple whenever its transversal coefficient exceeds 3/4.

Run from this directory:

    python3 -S p644_box_certificate_check.py

The checker reconstructs every mathematical assumption independently, checks all 64 support patterns in 13 symmetry orbits, verifies hashes, rejects untrusted proof rules, and invokes Ethos on each complete proof ending in false. It also checks the new integral rank-100 Fano witness. No SMT solver is required. The included Ethos executable is for macOS arm64; on another platform pass --ethos /path/to/ethos using Ethos 0.2.4. The verifier rewrites only the two signature include locations in temporary files.

The proof-producing discovery used Z3 5.1.0.0 and independent cvc5 1.4.0. Solver scripts retain their original discovery paths for provenance; these are not dependencies of replay. Twelve cases need only the older M1 and M5 templates; case 013_line also uses the new three-versus-four Fano construction. Four runs used smaller proof cores, and every retained assumption is matched against the complete independently reconstructed system.

Proof checker provenance:

- Ethos 0.2.4: https://github.com/cvc5/ethos/releases/tag/ethos-0.2.4
- Official macOS arm64 archive SHA256: 18717d16c7f33cafba0b82abb3c7ea6575da4a43873a2bb64ed94c979cea4021
- CPC signatures from cvc5 1.4.0: https://github.com/cvc5/cvc5/tree/cvc5-1.4.0/proofs/eo
- Official cvc5 source archive SHA256: 06c65b30693d1abf7c1393b497c799950de2833457920b9433da8e418bce9113
- Licenses are retained beside the checker and signatures.

The mathematical reduction and full hand lemmas are in Sections 7.58–7.62 of the adjacent research note. Rational witnesses scale to suitable multiples only. External mathematical review remains outstanding; nothing has been published.
