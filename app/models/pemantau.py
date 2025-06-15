from tortoise import fields, models

class Pemantau(models.Model):
    id = fields.IntField(pk=True)
    
    user = fields.ForeignKeyField("models.User", related_name="pemantau")

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)