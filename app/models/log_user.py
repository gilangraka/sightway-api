from tortoise import fields, models

class LogUser(models.Model):
    id = fields.IntField(pk=True)
    
    user = fields.ForeignKeyField("models.User", related_name="log_user")
    description = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "log_user"