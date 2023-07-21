from __future__ import annotations

import pytask_vscode


def test_import():
    assert hasattr(pytask_vscode, "__version__")
