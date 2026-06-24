from marshmallow import Schema, fields, validate, ValidationError

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    user_id = fields.Int(required=True)