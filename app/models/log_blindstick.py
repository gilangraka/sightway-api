from tortoise import fields, models
from enum import Enum

class StatusEnum(str, Enum):
    NORMAL = "normal",
    DANGER = "danger",

class LogBlindstick(models.Model):
    id = fields.IntField(pk=True)
    
    blindstick = fields.ForeignKeyField("models.Blindstick", related_name="log_blindstick")
    status = fields.CharEnumField(StatusEnum, default=StatusEnum.NORMAL)
    description = fields.TextField()    

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "log_blindstick"