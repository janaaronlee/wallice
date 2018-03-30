from marshmallow import Schema, fields

from wallice.api.spec.schemas.info import InfoSchema
from wallice.api.spec.schemas.common import DictField
from wallice.api.spec.schemas.paths import PathItemSchema
from wallice.api.spec.schemas.servers import ServerSchema


SUPPORTED_VERSIONS = ('3.0.0',)


class OpenApiSchema(Schema):

    openapi = fields.String(
        required=True,
        validate=lambda v: v in SUPPORTED_VERSIONS
    )
    info = fields.Nested(InfoSchema, required=True)
    servers = fields.Nested(ServerSchema, many=True)
    paths = DictField(
        fields.Str(),  # TODO: validate=validate.Regexp(r'')
        fields.Nested(PathItemSchema()),
        required=True
    )
    # components = fields.Nested(ComponentsSchema)
    # security = fields.Nested(SecurityRequirementSchema, many=True)
    # tags = fields.Nested(TagSchema, many=True)
    # externalDocs = fields.Nested(ExternalDocumentationSchema)
