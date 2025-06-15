from tortoise import fields, models

class Post(models.Model):
    id = fields.IntField(pk=True)

    category = fields.ForeignKeyField("models.MCategory", related_name="posts")
    
    title = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255)
    content = fields.TextField()
    thumbnail = fields.CharField(max_length=255)
    count_view = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    tags = fields.ManyToManyField("models.MTag", related_name="posts", through="post_tags")
