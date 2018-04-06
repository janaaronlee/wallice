import json
import os
import yaml


from wallice.api.spec.schemas import OpenApiSchema


class OpenApi(object):

    def __init__(self, yaml_path):

        if not os.path.exists(yaml_path):
            msg = 'OpenAPI spec file not found in: `{}`'
            raise FileNotFoundError(msg.format(yaml_path))

        with open(yaml_path) as f:
            yaml_str = f.read()

        self.api, errors = OpenApiSchema().load(yaml.load(yaml_str))

        for error in errors:
            raise Exception(
                'An error has occurred while validating the OpenAPI spec '
                'file in `{}`! Please check the `{}` field and resolve this '
                'error.'.format(yaml_path, error)
            )

    @property
    def info(self):
        return self.api['info']

    @property
    def servers(self):
        return self.api.get('servers', [])

    @property
    def paths(self):
        return self.api['paths']

    def __str__(self):
        return yaml.dump(self.api, default_flow_style=False)
