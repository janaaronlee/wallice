import json
import os

from chalice import Chalice
from chalice.app import LambdaFunction

from wallice.api.routes import Router
from wallice.utils.introspector import walk


__version__ = '0.2.0'


class Wallice(Chalice):

    lib_dir = 'chalicelib'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('debug', bool(os.environ.get('debug', True)))
        super().__init__(*args, **kwargs)
        self.add_lambdas(self.lambdas)
        Router(self)

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
