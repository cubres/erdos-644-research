# Complete two-type capacity catalogue

The complete 715-support catalogue and its 54,214 binary row assignments give 11,865 different per-part capacity functions. Exact pointwise dominance leaves 42 functions. This is a classification for type-closed families with two fixed types, not a resolution for arbitrary set families.

The data archive contains only JSON mathematical certificates. The checker reads it directly. No solver is needed for replay:

```sh
python3 -B -S p644_support_capacity_check.py --archive capacity_data.zip --workers 6
python3 -B -S p644_capacity_dominance_check.py
```

The first command independently reconstructs all support-colour orbits and verifies 375,446 rational primal/dual certificates, every capacity polygon's facets, and the retained construction witnesses. The second uses angular breakpoints to check all 11,865 dominations and pairwise incomparability of the 42 retained functions. The `--workers` setting affects speed only. The primary support catalogue can separately be reconstructed using `p644_support_catalog_check.py external_716_registry.json --output /path/to/a/new/report.json`.

Primary Boolean-function catalogue: Testa et al., IWLS 2019, https://si2.epfl.ch/demichel/publications/archive/2019/IWLS_ET.pdf and https://github.com/eletesta/7input_classification, immutable tree f8df07f4f30d8f9b61eb7befe4d4585b18fb7b75. Only truth-table representatives are used; validity and completeness are independently verified. New capacity projections and reductions are supplied here as research results, with external mathematical review and priority checks outstanding.
