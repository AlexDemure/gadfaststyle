import types


def define(module: types.ModuleType) -> str:
    return module.__name__
