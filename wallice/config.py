import yaml


class Config(dict):

    def __init__(self, config_file='config.yml'):

        with open(config_file, 'r') as f:
            yaml_data = f.read()

        super().__init__(**yaml.load(yaml_data))
