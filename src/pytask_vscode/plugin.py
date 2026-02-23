from __future__ import annotations

import pytask
from pluggy import PluginManager
from pytask_vscode import execution


@pytask.hookimpl
def pytask_add_hooks(pm: PluginManager) -> None:
    pm.register(execution)
