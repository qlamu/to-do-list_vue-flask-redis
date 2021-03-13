from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from marshmallow.decorators import validates_schema


class AuthSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "username is required"})
    password = fields.Str(required=True, error_messages={"required": "password is required"})


class ListSchema(Schema):
    title = fields.Str(required=True, error_messages={"required": "title is required"})


class AddTodoSchema(Schema):
    description = fields.Str(required=True, error_messages={"required": "description is required"})
    is_done = fields.Int(validate=OneOf([0, 1]))


class UpdateTodoSchema(Schema):
    description = fields.Str()
    is_done = fields.Int(validate=OneOf([0, 1]))

    @validates_schema
    def validate(self, data, **kwargs):
        "description" in data or "is_done" in data


class LogSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "username is required"})
    status = fields.Str(
        required=True,
        validate=OneOf(["FAIL", "WARNING", "SUCCESS"]),
        error_messages={"required": "status is required"},
    )
    message = fields.Str(required=True, error_messages={"required": "message is required"})
