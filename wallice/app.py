from chalice import Chalice

from wallice.routers import ImplicitRouter


__version__ = '0.1.0'


class Wallice(Chalice):

    def __init__(self, router=ImplicitRouter, *args, **kwargs):

        super().__init__(*args, **kwargs)
        router(self)
