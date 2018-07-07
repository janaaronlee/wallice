from os import environ as OS_ENVIRONMENT_VARIABLES

from marshmallow import Schema, fields, post_load, ValidationError


class ConfigSchema(Schema):

    debug = fields.Boolean(missing=False)
    cors = fields.Boolean(missing=False)
    cors_origin = fields.String(missing='*')
    cors_headers = fields.String(
        missing='Authorization,Content-Type,'
                'X-Amz-Date,X-Amz-Security-Token,X-Api-Key'
    )

    @post_load
    def listify_cors_headers(self, data):
        data['cors_headers'] = data['cors_headers'].split(',')
        return data


def Config():
    config = ConfigSchema().load(OS_ENVIRONMENT_VARIABLES)
    if config.errors:
        raise ValidationError(config.errors)
    return config.data
