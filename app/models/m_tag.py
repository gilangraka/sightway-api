from tortoise import fields, models

class MTag(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "m_tags"