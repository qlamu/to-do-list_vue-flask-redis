from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from marshmallow.decorators import validates_schema


class AuthSchema(Schema):
    username = fields.Str(required=True, error_messages={'required': 'username is required'})
    password = fields.Str(required=True, error_messages={'required': 'password is required'})


class ListSchema(Schema):
    title = fields.Str(required=True, error_messages={'required': 'title is required'})


class AddTodoSchema(Schema):
    description = fields.Str(required=True, error_messages={'required': 'description is required'})


class UpdateTodoSchema(Schema):
    description = fields.Str()
    is_done = fields.Int(strict=True, validate=OneOf([0, 1]))

    @validates_schema
    def validate(self, data, **kwargs):
        'description' in data or 'is_done' in data
