from wallice.routers.base import BaseRouter

from importlib import import_module
from inspect import getmembers, isfunction

import os


class ImplicitRouter(BaseRouter):

    root_dir = 'chalicelib/routes'
    excludes = ('__pycache__',)
    methods = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')

    def generate_route_name(self, root, file):
        root, file = root[len(self.root_dir):], file[:-3]

        if file.endswith('index'):
            file = file[len('index'):]

        route_name = os.path.join(root, file)

        if route_name.endswith('/'):
            route_name = route_name[:-1]

        return '/{}'.format(route_name)

    def get_methods(self, root, file):
        methods = {}

        path = os.path.join(root, file[:-3])
        module_name = path.replace('/', '.')
        module = import_module(module_name)

        for name, function in getmembers(module, isfunction):
            name = name.upper()
            if name not in self.methods:
                continue

            methods[name] = function

        return methods

    @property
    def routes(self):
        routes = {}

        for root, _, files in os.walk(self.root_dir):
            if root.endswith(self.excludes):
                continue

            for file in files:
                route_name = self.generate_route_name(root, file)
                methods = self.get_methods(root, file)

                if route_name in routes:
                    msg = 'Route {} is already set! Overriding!'
                    print(msg.format(route_name))

                routes[route_name] = methods

        return routes

    def wrap(self, function):

        def wrapped(*args, **kwargs):
            return function(self.app.current_request)

        return wrapped
