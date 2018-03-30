from marshmallow import Schema, fields


class ContactSchema(Schema):

    name = fields.String()
    url = fields.Url()
    email = fields.Email()


class LicenseSchema(Schema):

    name = fields.String(required=True)
    url = fields.Url()


class InfoSchema(Schema):

    title = fields.String(required=True)
    description = fields.String()  # TODO: validate CommonMark
    termsOfService = fields.Url()
    contact = fields.Nested(ContactSchema)
    license = fields.Nested(LicenseSchema)
    version = fields.String(required=True)
