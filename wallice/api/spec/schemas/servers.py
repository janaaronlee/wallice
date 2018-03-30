from marshmallow import Schema, fields

from wallice.api.spec.schemas.common import DictField


class ServerVariableSchema(Schema):

    enum = fields.List(fields.String())
    default = fields.String(required=True)
    description = fields.String()  # TODO: validate CommonMark


class ServerSchema(Schema):

    url = fields.Url(reqyured=True)
    description = fields.String()  # TODO: validate CommonMark
    variables = DictField(
        fields.String(),
        fields.Nested(ServerVariableSchema)
    )
