import importlib
from typing import Any
import config


def echo(*args: Any) -> Any:
    print('echo')
    print('args: ')
    for arg in args:
        print(arg)


def addmod(mod: str):
    importlib.invalidate_caches()
    impmod = importlib.import_module(mod, 'mods')
    config.loaded_mods[mod] = {}
    funcs = list(filter(lambda x: not x.startswith('__'), dir(impmod)))
    for func in funcs:
        config.loaded_mods['essentials'][func] = getattr(essentials, func)


def reloadallmods(*args: Any):
    for mod in list(config.loaded_mods.keys()):
        importlib.reload(mod)


def delmod(mod: str):
    if mod != 'essentials':
        del config.loaded_mods[mod]
