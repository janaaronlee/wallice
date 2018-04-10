import json
import os

from chalice import CORSConfig 

from wallice.api.spec import OpenApi
from wallice.utils.introspector import walk


class Router(object):

    _api_file = 'api.yml'
    _paths_dir = 'paths'

    def __init__(self, app, api_file=None):
        self.app = app

        if api_file is not None:
            self._api_file = api_file

        self.route_handlers = RouteHandlers(self.paths_dir)
        self.api = OpenApi(self.yaml_path)
        self.add_routes()

    @property
    def yaml_path(self):
        return os.path.join(self.app.lib_dir, self._api_file)

    @property
    def paths_dir(self):
        return os.path.join(self.app.lib_dir, self._paths_dir)

    def init_route(self, path, method, config):
        function = self.route_handlers[path][method]

        def wrapped(*args, **kwargs):
            return function(self.app.current_request)

        return wrapped

    @property
    def route_kwargs(self):
        if os.environ.get('cors', 'false').lower() != 'true':
            return {}

        return {
            'cors': CORSConfig(
                allow_origin=os.environ.get('cors_origin', '*'),
                allow_headers=os.environ.get(
                    'cors_headers',
                    'Authorization,Content-Type,'
                    'X-Amz-Date,X-Amz-Security-Token,X-Api-Key'
                ).split(',')
            )
        }

    def add_routes(self):
        registered_routes = {}
        for path, methods in self.api.paths.items():
            for method, config in methods.items():
                name = '{}:{}'.format(path.replace('/', '_'), method)
                method = method.upper()
                self.app._add_route(
                    path, self.init_route(path, method, config),
                    methods=[method], name=name, **self.route_kwargs
                )
                registered_routes.setdefault(path, [])
                registered_routes[path].append(method)

        print('Registered routes:')
        print(json.dumps(registered_routes, indent=2))


class RouteHandlers(dict):

    valid_http_methods = (
        'GET', 'POST', 'PUT', 'DELETE',
        'HEAD', 'OPTIONS', 'CONNECT'
    )

    def __init__(self, routes_dir):
        super().__init__(self.get_routes(routes_dir).items())

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
            if name in self.valid_http_methods:
                yield name, function

    def get_routes(self, routes_dir):
        routes = {}
        for module_name, functions in walk(routes_dir):
            route_name = self.generate_route_name(module_name)
            msg = 'Duplicate route for `{}` is not allowed!'
            assert route_name not in routes, msg.format(route_name)
            routes[route_name] = dict(self.extract_methods(functions))
        return routes
