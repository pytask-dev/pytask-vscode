import pytask
from pytask_vscode import execution
from pluggy import PluginManager

@pytask.hookimpl
def pytask_add_hooks(pm : PluginManager) -> None:
    pm.register(execution)