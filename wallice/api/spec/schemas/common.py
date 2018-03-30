from marshmallow import Schema, fields


class DictField(fields.Field):

    def __init__(self, key_field, value_field, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.key_field = key_field
        self.value_field = value_field

    def _deserialize(self, value, attr, data):
        key_fn = self.key_field.deserialize
        val_fn = self.value_field.deserialize

        return {key_fn(k): val_fn(v) for k, v in value.items()}

    def _serialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.key_field._serialize(key, attr, obj)
            v = self.nested_field.serialize(key, self.get_value(attr, obj))
            ret[k] = v
        return ret


class ReferenceSchema(Schema):

    _ref = fields.String(attribute='$ref')
    # TODO


class OptionalReferenceSchema(ReferenceSchema):

    pass
    # TODO
