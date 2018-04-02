from marshmallow import Schema, fields

from wallice.api.spec.schemas.common import (
    DictField, ReferenceSchema, OptionalReferenceSchema,
)
from wallice.api.spec.schemas.metadata import (
    ExternalDocumentationSchema, MediaTypeSchema
)
from wallice.api.spec.schemas.parameters import ParameterSchema
from wallice.api.spec.schemas.servers import ServerSchema


class RequestBodySchema(OptionalReferenceSchema):

    description = fields.String()  # TODO: validate CommonMark
    content = DictField(
        fields.String(),  # TODO: validate content types
        fields.Nested(MediaTypeSchema()),
        required=True
    )
    required = fields.Boolean(default=False)


class OperationSchema(Schema):

    tags = fields.List(fields.String())
    summary = fields.String()
    description = fields.String()  # TODO: validate CommonMark
    externalDocs = fields.Nested(ExternalDocumentationSchema)
    operationId = fields.String()  # TODO: validate unique all
    parameters = fields.Nested(ParameterSchema, many=True)  # no duplicates
    requestBody = fields.Nested(RequestBodySchema)
    # responses = fields.Nested(ResponsesSchema)
    # callbacks = DictField(
    #     fields.String(),
    #     fields.Nested(CallbackSchema)  # TODO: REF
    # )
    deprecated = fields.Boolean()
    # security = fields.Nested(SecurityRequirementSchema)
    servers = fields.Nested(ServerSchema, many=True)


class PathItemSchema(ReferenceSchema):

    summary = fields.String()
    description = fields.String()  # TODO: validate CommonMark
    get = fields.Nested(OperationSchema)
    put = fields.Nested(OperationSchema)
    post = fields.Nested(OperationSchema)
    delete = fields.Nested(OperationSchema)
    options = fields.Nested(OperationSchema)
    head = fields.Nested(OperationSchema)
    patch = fields.Nested(OperationSchema)
    trace = fields.Nested(OperationSchema)
    servers = fields.Nested(ServerSchema, many=True)
    parameters = fields.Nested(ParameterSchema, many=True)  # no duplicates
