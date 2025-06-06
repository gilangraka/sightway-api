from tortoise import fields, models

class Blindstick(models.Model):
    id = fields.IntField(pk=True)
    mac_address = fields.CharField(max_length=255)
    is_used = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)