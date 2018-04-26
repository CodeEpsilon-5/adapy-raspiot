import importlib
from typing import Any
from . import config


def echo(*args: Any) -> Any:
    print('echo')
    print('args: ')
    for arg in args:
        print(arg)


def addmod(mod: str):
    importlib.invalidate_caches()
    impmod = importlib.import_module(f'mods.{mod}')
    config.loaded_mods[mod] = {}
    funcs = list(filter(lambda x: not x.startswith('__'), dir(impmod)))
    for func in funcs:
        config.loaded_mods[mod][func] = getattr(impmod, func)


def reloadallmods(*args: Any):
    for mod in list(config.loaded_mods.keys()):
        importlib.reload(mod)
    importlib.reload(config)


def delmod(mod: str):
    if mod != 'essentials':
        del config.loaded_mods[mod]
