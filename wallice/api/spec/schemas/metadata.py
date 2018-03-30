from marshmallow import Schema, fields

from wallice.api.spec.schemas.common import DictField, OptionalReferenceSchema


class ExternalDocumentationSchema(Schema):

    description = fields.String()  # TODO: validate CommonMark
    url = fields.Url(required=True)


class TagSchema(Schema):

    name = fields.String(required=True)
    description = fields.String()
    externalDocs = fields.Nested(ExternalDocumentationSchema)


class HeaderSchema(OptionalReferenceSchema):

    pass


class EncodingSchema(Schema):

    contentType = fields.String()  # TODO: validate if valid content-type
    headers = DictField(
        fields.String(),
        fields.Nested(HeaderSchema())
    )  # TODO:
    """
    A map allowing additional information to be provided as headers, for
    example Content-Disposition. Content-Type is described separately and SHALL
    be ignored in this section. This property SHALL be ignored if the request
    body media type is not a multipart.
    """
    style = fields.String()  # TODO:
    """
    Describes how a specific property value will be serialized depending on its
    type. See Parameter Object for details on the style property. The behavior
    follows the same values as query parameters, including default values. This
    property SHALL be ignored if the request body media type is not
    application/x-www-form-urlencoded.
    """
    explode = fields.Boolean()  # TODO:
    """
    When this is true, property values of type array or object generate
    separate parameters for each value of the array, or key-value-pair of the
    map. For other types of properties this property has no effect. When style
    is form, the default value is true. For all other styles, the default value
    is false. This property SHALL be ignored if the request body media type is
    not application/x-www-form-urlencoded.
    """
    # TODO: ignore if media-type not: application/x-www-form-urlencoded
    allowReserved = fields.Boolean(default=False)


# TODO
class SchemaSchema(OptionalReferenceSchema):

    pass


class ExampleSchema(OptionalReferenceSchema):

    summary = fields.String()
    description = fields.String()  # TODO: validate CommonMark
    value = fields.Field()  # TODO: mutually exclusive with externalValue
    externalValue = fields.Url()  # TODO: mutually exclusive with value


class MediaTypeSchema(OptionalReferenceSchema):

    schema = fields.Nested(SchemaSchema())
    example = fields.Field()  # TODO: mutually exclusive with examples
    examples = DictField(  # TODO: mutually exclusive with example
        fields.String(),
        fields.Nested(ExampleSchema())
    )
    encoding = DictField(  # TODO: only when media typs is `multipart`
        fields.String(),  # TODO: must exist in schema as a property
        fields.Nested(EncodingSchema())
    )
