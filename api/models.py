from django.db import models

class ReplacementPart(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField()

    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.name
