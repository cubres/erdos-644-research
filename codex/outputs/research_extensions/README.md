# Additional Erdős 644 certificates and discovery tools

The general bound remains 6/7. Sections 7.63–7.70 of the adjacent note distinguish hand proofs, checked finite claims and unfinished searches.

## Standard-library replays

Run from this directory:

```sh
python3 -B -S p644_fano_capacity_check.py
python3 -B -S p644_minimum_response_obstruction_check.py --gaps
python3 -B -S p644_pair_cover_check.py
python3 -B -S p644_support_lp_check.py logs/astra_support_exact_pocket.json
python3 -B -S p644_support_lp_check.py logs/astra_support_exact_pure.json
python3 -B -S p644_support_lp_check.py logs/astra_support_exact_line.json
python3 -B -S p644_support_lp_check.py logs/astra_support_exact_quarter.json
python3 -B -S p644_adaptive_response_check.py logs/astra_two_finish_adaptive_0_gaps_v2/summary.json
python3 -B -S p644_adaptive_response_check.py logs/astra_two_finish_adaptive_1_gaps_v2/summary.json
python3 -B -S p644_adaptive_response_check.py logs/astra_two_finish_adaptive_2_gaps_v2/summary.json
```

The complete-support certificate uses all 715 nonprojection classes and 54,214 component assignments. The pocket case has exact Farkas certificates for all of them. Positive cases contain explicitly trimmed Venn cells. To independently reconstruct the support catalogue, run `p644_support_catalog_check.py external_716_registry.json --output /path/to/a/new/report.json`; compare all report fields except elapsed time with `logs/astra_full_support_catalog.json`.

## Primary catalogue provenance

Testa, Haaswijk, Soeken and De Micheli, *The Complexity of Self-Dual Monotone 7-Input Functions*, IWLS 2019:
https://si2.epfl.ch/demichel/publications/archive/2019/IWLS_ET.pdf
Authors' repository: https://github.com/eletesta/7input_classification
Immutable tree: f8df07f4f30d8f9b61eb7befe4d4585b18fb7b75.
Only truth-table names are used; the checker independently establishes their validity and exhaustive orbit coverage.

## Discovery programs

The box-dimension, support-LP and adaptive-synthesis programs may require NumPy, SciPy, SymPy or Z3. Some discovery scripts use this machine's dependency path. They are supplied for continued research, not as portable theorem verifiers. Four-part timeouts and incomplete request searches prove no universal theorem. The original adaptive version's zero-neighbor boundary error is corrected in the supplied code; only the v2 response data listed above are certified. The affine-region learner is ongoing discovery work.
