from tortoise import fields, models
import enum

class HubunganStatus(enum.Enum):
    KELUARGA = "keluarga"
    LAINNYA = "lainnya"

class PenyandangPemantau(models.Model):
    id = fields.IntField(pk=True)

    penyandang = fields.ForeignKeyField("models.Penyandang", related_name="penyandang_pemantau")
    pemantau = fields.ForeignKeyField("models.Pemantau", related_name="penyandang_pemantau")

    status = fields.CharEnumField(HubunganStatus, max_length=50)
    detail_status = fields.TextField(null=True)

    class Meta:
        table = "penyandang_pemantau"
        unique_together = (("penyandang", "pemantau"),)