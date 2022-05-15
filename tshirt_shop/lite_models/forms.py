from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'street', 'city', 'state', 'postal_code', 'phone', 'email', 'name_on_card', 'credit_card_number', 'cvv_number', 'billing_street', 'billing_city', 'billing_state','billing_postal_code']