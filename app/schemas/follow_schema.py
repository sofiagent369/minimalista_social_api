from marshmallow import Schema, fields, validate, ValidationError

class FollowSchema(Schema):
    id = fields.Int(dump_only=True)
    follower_id = fields.Int(required=True)
    followed_id = fields.Int(required=True)