import json
import os

from chalice import Chalice
from chalice.app import LambdaFunction

from wallice.routers import ImplicitRouter
from wallice.utils.config import Config
from wallice.utils.introspector import walk


__version__ = '0.1.3'


class Wallice(Chalice):

    lib_dir = 'chalicelib'

    def __init__(self, router=ImplicitRouter, *args, **kwargs):
        kwargs.setdefault('app_name', Config.app_name)
        kwargs.setdefault('debug', Config.debug)
        super().__init__(*args, **kwargs)
        self.add_lambdas(self.lambdas)
        router(self)

    @property
    def lambdas_dir(self):
        return os.path.join(self.lib_dir, 'lambdas')

    @property
    def lambdas(self):
        for handler_name, functions in walk(self.lambdas_dir):
            handler_name = handler_name.replace('.', '-')
            functions = dict(functions)

            if 'lambda_handler' in functions:
                yield handler_name, functions['lambda_handler']

    def add_lambdas(self, lambdas):
        registered_lambdas = []
        for handler_name, lambda_function in lambdas:
            wrapper = LambdaFunction(
                lambda_function, name=handler_name,
                handler_string='app.%s' % handler_name
            )
            registered_lambdas.append(handler_name)
            self.pure_lambda_functions.append(wrapper)

        print('Registered lambdas:')
        print(json.dumps(registered_lambdas, indent=2))
