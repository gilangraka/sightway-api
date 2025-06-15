from tortoise import fields, models

class LogPenyandangMap(models.Model):
    id = fields.IntField(pk=True)
    
    penyandang = fields.ForeignKeyField("models.Penyandang", related_name="log_penyandang_map")
    latitude = fields.CharField(max_length=255)
    longitude = fields.CharField(max_length=255)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "log_penyandang_map"