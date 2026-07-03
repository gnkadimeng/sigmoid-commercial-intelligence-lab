"""Root conftest — ensures the project root is importable as ``src`` during tests.

Placing this at the repository root makes pytest add the root to sys.path (prepend import mode), so
tests can ``import src...`` regardless of the working directory they are invoked from.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
