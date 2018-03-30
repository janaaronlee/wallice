from marshmallow import Schema, fields

from wallice.api.spec.schemas.common import (
    DictField, ReferenceSchema, OptionalReferenceSchema,
)
from wallice.api.spec.schemas.metadata import (
    ExternalDocumentationSchema, MediaTypeSchema
)
from wallice.api.spec.schemas.servers import ServerSchema


class ParameterSchema(OptionalReferenceSchema):

    name = fields.String(required=True)  # TODO:
    """
    If in is "path", the name field MUST correspond to the associated path
    segment from the path field in the Paths Object. See Path Templating for
    further information.
    If in is "header" and the name field is "Accept", "Content-Type" or
    "Authorization", the parameter definition SHALL be ignored.
    For all other cases, the name corresponds to the parameter name used by
    the in property.
    """
    _in = fields.String(
        data_key='in',
        required=True,
        validate=lambda l: l in ('query', 'header', 'path', 'cookie')
    )
    description = fields.String()  # TODO: validate CommonMark
    required = fields.Boolean(default=False)  # TODO:
    """
    If the parameter location is "path", this property is REQUIRED and its
    value MUST be true. Otherwise, the property MAY be included and its default
    value is false.
    """
    deprecated = fields.Boolean()
    allowEmptyValue = fields.Boolean(default=False)  # TODO:
    """
    Sets the ability to pass empty-valued parameters. This is valid only for
    query parameters and allows sending a parameter with an empty value.
    """
    # TODO: the rest


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
