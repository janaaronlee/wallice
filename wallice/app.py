from chalice import Chalice

from wallice.config import Config
from wallice.routers import ImplicitRouter


__version__ = '0.1.0'


class Wallice(Chalice):

    def __init__(self, router=ImplicitRouter, *args, **kwargs):

        self.config.update(kwargs)
        super().__init__(*args, **self.config)
        router(self)

    @property
    def config(self):
        config = Config()
        return config['app']
