from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Tshirt(models.Model):
    tshirt_id = models.AutoField(primary_key=True)
    tshirt_name = models.CharField(max_length=30)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    inventory = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Item Id: {self.tshirt_id}, Item: {self.tshirt_name}, Price: {self.price}, Inventory: {self.inventory}'