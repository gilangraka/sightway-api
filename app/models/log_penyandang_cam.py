from tortoise import fields, models
from enum import Enum

class StatusEnum(str, Enum):
    NORMAL = "normal",
    DANGER = "danger",
    
class LogPenyandangCam(models.Model):
    id = fields.IntField(pk=True)
    
    penyandang = fields.ForeignKeyField("models.Penyandang", related_name="log_penyandang_cam")
    folder_name = fields.CharField(max_length=255)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "log_penyandang_cam"