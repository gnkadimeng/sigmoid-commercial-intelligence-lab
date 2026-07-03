"""Sigmoid Commercial Intelligence Lab — computational core.

This package is the single source of computational truth for the lab. Dashboards, notebooks, and
tests import scoring/validation/evidence logic from here rather than re-implementing it (see the CIS
Computational Architecture section).

Modules
-------
- scoring     : transparent, weighted 0..100 scoring functions.
- validation  : structural data-integrity checks.
- evidence    : evidence weighting, strength classification, and aggregation.
- ontology    : lightweight object types mirroring the CIS ontology.
- utils       : shared helpers (paths, safe numerics, loading frameworks/data).
"""

__version__ = "0.1.0"
