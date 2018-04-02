from marshmallow import fields

from wallice.api.spec.schemas.common import DictField, OptionalReferenceSchema
from wallice.api.spec.schemas.metadata import (
    ExampleSchema, MediaTypeSchema, SchemaSchema
)


class ParameterSchema(OptionalReferenceSchema):

    class Meta:
        """
        If in is "path", the name field MUST correspond to the associated path
        segment from the path field in the Paths Object. See Path Templating
        for further information.
        If in is "header" and the name field is "Accept", "Content-Type" or
        "Authorization", the parameter definition SHALL be ignored.
        For all other cases, the name corresponds to the parameter name used by
        the in property.
        """
        include = {
            'in': fields.String(
                required=True,
                validate=lambda l: l in ('query', 'header', 'path', 'cookie')
            )
        }

    name = fields.String(required=True)  # TODO:
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
    style = fields.String()
    """
    Default values (based on value of in): for query - form; for path - simple;
    for header - simple; for cookie - form.
    """
    explode = fields.Boolean()
    """
    When style is form, the default value is true. For all other styles, the
    default value is false.
    """
    allowReserved = fields.Boolean()
    """This property only applies to parameters with an in value of query"""
    # TODO: mutually exclusive with content
    schema = fields.Nested(SchemaSchema)
    example = fields.Field()  # TODO: mutually exclusive with examples
    examples = DictField(  # TODO: mutually exclusive with example
        fields.String(),
        fields.Nested(ExampleSchema())
    )
    content = DictField(  # TODO: mutually exclusive with schema
        fields.String(),
        fields.Nested(MediaTypeSchema)
    )
