import os

from importlib import import_module
from inspect import getmembers, isfunction


def get_functions(module_name):
    return getmembers(import_module(module_name), isfunction)


def walk(root_dir, excludes=('__pycache__',)):
    if not os.path.exists(root_dir):
        return

    for root, _, files in os.walk(root_dir):
        if root.endswith(excludes):
            continue

        for file in files:
            module_name = os.path.join(root, file)[:-3].replace('/', '.')
            yield module_name[len(root_dir) + 1:], get_functions(module_name)
