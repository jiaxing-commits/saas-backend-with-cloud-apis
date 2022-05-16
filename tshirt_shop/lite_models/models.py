from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator, RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

only_numbers = RegexValidator(
            regex='^[0-9]*$',
            message='Must be numeric',
            code='invalid_input'
        )

# Create your models here.
class Tshirt(models.Model):
    tshirt_id = models.AutoField(primary_key=True)
    tshirt_name = models.CharField(max_length=30, unique=True)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    inventory = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'Item Id: {self.tshirt_id}, Item: {self.tshirt_name}, Price: {self.price}, Inventory: {self.inventory}'

class Customer(models.Model):
    # Customer info
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=26)
    last_name = models.CharField(max_length=26)
    street = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    postal_code = models.CharField(validators=[MinLengthValidator(5), only_numbers] ,max_length=5)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=320, unique=True)
    order_list = models.CharField(max_length=1000) # str list with comma delimiter Ex: "item_id1 quanitity1, item_id2 quanitity2, ..."
    order_total = models.FloatField(validators=[MinValueValidator(0.0)])

    #Card Information
    name_on_card = models.CharField(max_length=30)
    credit_card_number = models.CharField(validators=[MinLengthValidator(16), only_numbers] , max_length=16)
    cvv_number = models.CharField(validators=[MinLengthValidator(3), only_numbers] ,max_length=3) 
    billing_street = models.CharField(max_length=35)
    billing_city = models.CharField(max_length=35)
    billing_state = models.CharField(max_length=35)
    billing_postal_code = models.CharField(validators=[MinLengthValidator(5), only_numbers], max_length=5)

    # success access to stripe
    charge_success = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Name: {self.first_name} {self.last_name}, Customer Id: {str(self.customer_id)}, Order: {self.order_list}'