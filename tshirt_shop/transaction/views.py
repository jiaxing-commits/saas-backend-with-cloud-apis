from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import json
        
class CartItem:
    def __init__(self, name: str, src: str, description: str, \
        price: float, quantity: int) -> None:
        self.name = name
        self.src = src
        self.description = description
        self.price = price
        self.quantity = quantity
        self.total = quantity * price
        
    def update_quantity(self, quantity: int) -> None:
        # must update total after updating quanity of any cart items
        if quantity < 0: return 
        self.quantity = quantity
        self.total = round(quantity * self.price,2)

class Cart:
    def __init__(self, tax_rate: float, shipping_rate: float, cart_items: dict[CartItem]) -> None:
        self.tax_rate = tax_rate
        self.tax_rate_display = tax_rate * 100
        self.shipping_rate = shipping_rate
        self.cart_items = cart_items
        self.sub_total = 0
        self.tax = 0
        self.grand_total = 0
        self.update_total()
    
    def update_total(self) -> None:
        # must update total after updating quanity of any cart items
        new_sub = 0
        
        for key in self.cart_items:
            new_sub += self.cart_items[key].total
        
        self.sub_total = round(new_sub, 2)
        if new_sub == 0:
            self.tax = 0
            self.grand_total = 0
        else:
            self.tax = round(new_sub * self.tax_rate, 2)
            self.grand_total = round(new_sub + self.tax + self.shipping_rate, 2)

cart_items = {
        "Dingo Dog Bones": CartItem("Dingo Dog Bones", "https://s.cdpn.io/3/dingo-dog-bones.jpg", \
            "dogg", 12.99, 1),
        "Nutro™ Adult Lamb and Rice Dog Food": CartItem("Nutro™ Adult Lamb and Rice Dog Food", \
            "https://s.cdpn.io/3/large-NutroNaturalChoiceAdultLambMealandRiceDryDogFood.png", \
                "weeeee", 45.99, 1)
                }

cart = Cart(0.05, 15, cart_items)

def checkout(request: HttpRequest) -> HttpResponse:
    context = {'cart': cart}
    return render(request, 'transaction/checkout.html', context)

def quantity_change(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
           item_name = request.GET['item_name']
           item_val = request.GET['item_val']

           cart.cart_items[item_name].update_quantity(int(item_val))
           cart.update_total()
           
           context = {
               'item_total': cart.cart_items[item_name].total,
               'sub_total': cart.sub_total,
               'tax': cart.tax,
               'shipping': 0 if cart.sub_total == 0 else cart.shipping_rate,
               'grand_total': cart.grand_total,
           }
           return HttpResponse(json.dumps(context))
    else:
           return HttpResponse("Request method is not a GET")

def remove_item(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
           item_name = request.GET['item_name']

           cart.cart_items[item_name].update_quantity(0)
           cart.update_total()
           
           context = {
               'sub_total': cart.sub_total,
               'tax': cart.tax,
               'shipping': 0 if cart.sub_total == 0 else cart.shipping_rate,
               'grand_total': cart.grand_total,
           }
           return HttpResponse(json.dumps(context))
    else:
           return HttpResponse("Request method is not a GET")