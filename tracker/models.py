from django.db import models

# Create your models here.
class MilkEntry(models.Model):
    date = models.DateField()
    quantity = models.FloatField()
    price_per_litre = models.FloatField(default=60, editable=False)

    def total(self):
        return self.quantity * self.price_per_litre

    def __str__(self):
        return f"{self.date} - {self.quantity}L"