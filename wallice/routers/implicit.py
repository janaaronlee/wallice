import os

from wallice.routers.base import BaseRouter
from wallice.utils.introspector import walk


class ImplicitRouter(BaseRouter):

    excludes = ('__pycache__',)
    methods = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')

    @property
    def routes_dir(self):
        return os.path.join(self.app.lib_dir, 'routes')

    def generate_route_name(self, module_name):
        module_name = module_name.replace('.', '/')
        if module_name.endswith('index'):
            module_name = module_name[:-len('index')]

        if len(module_name) > 1 and module_name.endswith('/'):
            module_name = module_name[:-1]

        if not module_name.startswith('/'):
            module_name = '/{}'.format(module_name)

        return module_name

    def extract_methods(self, functions):
        for name, function in functions:
            name = name.upper()
            if name in self.methods:
                yield name, function

    @property
    def routes(self):
        routes = {}

        for module_name, functions in walk(self.routes_dir):
            route_name = self.generate_route_name(module_name)
            if route_name in routes:
                msg = 'Route {} is already set! Overriding!'
                print(msg.format(route_name))

            routes[route_name] = dict(self.extract_methods(functions))

        return routes

    def wrap(self, function):

        def wrapped(*args, **kwargs):
            return function(self.app.current_request)

        return wrapped
