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
        for name, path, function, method in self:
            self.app._add_route(path, function, methods=[method], name=name)

    def __iter__(self):
        for path, methods in self.routes.items():
            for method, function in methods.items():
                name = '{}_{}'.format(path.replace('/', '_'), method)
                yield name, path, self.wrap(function), method
