from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from json import JSONEncoder
import json
        
class CartItem:
    def __init__(self, json_dic) -> None:
        self.name = json_dic["name"]
        self.src = json_dic["src"]
        self.description = json_dic["description"]
        self.price = json_dic["price"]
        self.quantity = json_dic["quantity"]
        self.total = json_dic["quantity"] * json_dic["price"]
        
    def update_quantity(self, quantity: int) -> None:
        # must update total after updating quanity of any cart items
        if quantity < 0: return 
        self.quantity = quantity
        self.total = round(quantity * self.price,2)

class Cart:
    def __init__(self, json_dic) -> None:
        self.tax_rate = json_dic["tax_rate"]
        self.tax_rate_display = json_dic["tax_rate"] * 100
        self.shipping_rate = json_dic["shipping_rate"]
        self.cart_items = json_dic["cart_items"]
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

class CartEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def checkout(request: HttpRequest) -> HttpResponse:

    # initial cart for html template. The current cart information is stored in the cart_str attribute!
    cart_items = {
        "Dingo Dog Bones": CartItem({"name": "Dingo Dog Bones", "src": "https://s.cdpn.io/3/dingo-dog-bones.jpg", \
            "description": "dogg", "price": 12.99, "quantity": 1}),
        "Nutro™ Adult Lamb and Rice Dog Food": CartItem({"name": "Nutro™ Adult Lamb and Rice Dog Food", \
            "src": "https://s.cdpn.io/3/large-NutroNaturalChoiceAdultLambMealandRiceDryDogFood.png", \
                "description": "weeeee", "price": 45.99, "quantity": 1})
                }

    cart = Cart({"tax_rate":0.05, "shipping_rate":15, "cart_items":cart_items})

    context = {'cart': cart, 'cart_str': json.dumps(cart, indent=4, cls=CartEncoder)}
    return render(request, 'transaction/checkout.html', context)

def quantity_change(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
           item_name = request.GET['item_name']
           item_val = request.GET['item_val']
           cart = json.loads(request.GET['cart'])

           for item in cart["cart_items"]:
               cart["cart_items"][item] = CartItem(cart["cart_items"][item])
           cart = Cart(cart)
           
           cart.cart_items[item_name].update_quantity(int(item_val))
           cart.update_total()
           
           context = {
               'item_total': cart.cart_items[item_name].total,
               'sub_total': cart.sub_total,
               'tax': cart.tax,
               'shipping': 0 if cart.sub_total == 0 else cart.shipping_rate,
               'grand_total': cart.grand_total,
               'cart_str': json.dumps(cart, indent=4, cls=CartEncoder),
           }
           return HttpResponse(json.dumps(context))
    else:
           return HttpResponse("Request method is not a GET")

def remove_item(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
           item_name = request.GET['item_name']
           cart = json.loads(request.GET['cart'])

           for item in cart["cart_items"]:
               cart["cart_items"][item] = CartItem(cart["cart_items"][item])
           cart = Cart(cart)
        
           cart.cart_items[item_name].update_quantity(0)
           cart.update_total()
           
           context = {
               'sub_total': cart.sub_total,
               'tax': cart.tax,
               'shipping': 0 if cart.sub_total == 0 else cart.shipping_rate,
               'grand_total': cart.grand_total,
               'cart_str': json.dumps(cart, indent=4, cls=CartEncoder),
           }
           return HttpResponse(json.dumps(context))
    else:
           return HttpResponse("Request method is not a GET")

def fillout(request: HttpRequest) -> HttpResponse:
    return render(request, 'transaction/card_fillout.html')