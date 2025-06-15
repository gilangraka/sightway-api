from tortoise import fields, models

class Penyandang(models.Model):
    id = fields.IntField(pk=True)
    
    user = fields.ForeignKeyField("models.User", related_name="penyandang")
    blindstick = fields.ForeignKeyField("models.Blindstick", related_name="penyandang_blindstick", null=True, on_delete=fields.SET_NULL)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    pemantau = fields.ManyToManyField("models.Pemantau", related_name="penyandang", through="penyandang_pemantau") 