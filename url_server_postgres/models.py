from tortoise import models, fields

class URL(models.Model):
    id = fields.IntField(pk=True)
    original_url = fields.CharField(max_length=120)
    short_url = fields.CharField(unique=True, max_length=20)

    class Meta:
        table = "urls"