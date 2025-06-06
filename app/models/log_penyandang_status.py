from tortoise import fields, models
from enum import Enum

class StatusEnum(str, Enum):
    NORMAL = "normal",
    DANGER = "danger",

class LogPenyandangStatus(models.Model):
    id = fields.IntField(pk=True)
    
    penyandang = fields.ForeignKeyField("models.Penyandang", related_name="log_penyandang_status")
    blindstick = fields.ForeignKeyField("models.Blindstick", related_name="penyandang", null=True, on_delete=fields.SET_NULL)
    status = fields.CharEnumField(StatusEnum, default=StatusEnum.NORMAL)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "log_penyandang_status"