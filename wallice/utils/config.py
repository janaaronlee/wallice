import json
import os


class Config(dict):

    config_dir = '.chalice'
    config_file = 'config.json'

    def __init__(self):
        with open(os.path.join(self.config_dir, self.config_file)) as f:
            _config = json.loads(f.read())
            _config.pop('stages')
            super().__init__(**_config)

    @property
    def version(self):
        return self['version']

    @property
    def app_name(self):
        return self['app_name']

    @property
    def debug(self):
        return os.environ.get('debug', "false") == "true"


Config = Config()
