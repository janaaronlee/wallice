import json

from abc import ABC, abstractproperty, abstractmethod


class BaseRouter(ABC):

    def __init__(self, app):
        self.app = app
        self.add_routes()

    @abstractproperty
    def routes(self):
        raise NotImplementedError

    @abstractmethod
    def wrap(self, function):
        raise NotImplementedError

    def add_routes(self):
        registered_routes = {}
        for path, methods in self.routes.items():
            for method, function in methods.items():
                name = '{}_{}'.format(path.replace('/', '_'), method[:-1])
                self.app._add_route(
                    path, function,
                    methods=[method], name=name
                )
                registered_routes.setdefault(path, [])
                registered_routes[path].append(method)

        print('Regsistered routes:')
        print(json.dumps(registered_routes, indent=2))
