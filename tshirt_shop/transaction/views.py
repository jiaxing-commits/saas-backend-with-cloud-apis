from lite_models.models import Customer, Tshirt
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http.response import JsonResponse
from json import JSONEncoder
import json
import stripe
        
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
    if request.method == 'POST':
        request.session['cart_info'] = request.POST["cart_info"]
        return redirect('/../fillout')
    else:
        # initial cart for html template. The current cart information is stored in the cart_str attribute!
        cart_items = {
            "Red T-shirt": CartItem({"name": "Red T-shirt", "src": "https://s.cdpn.io/3/dingo-dog-bones.jpg", \
                "description": "It is red", "price": 12.99, "quantity": 1}),
            "Green T-shirt": CartItem({"name": "Green T-shirt", \
                "src": "https://s.cdpn.io/3/large-NutroNaturalChoiceAdultLambMealandRiceDryDogFood.png", \
                    "description": "It is green", "price": 45.99, "quantity": 1})
                    }

        cart = Cart({"tax_rate":0.05, "shipping_rate":15, "cart_items":cart_items})

        context = {'cart': cart, 'cart_str': json.dumps(cart, indent=4, cls=CartEncoder)}
        return render(request, 'transaction/checkout.html', context)

def quantity_change(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
           item_name = request.GET['item_name']
           item_val = request.GET['item_val']
           cart = cart_str_tojson(request.GET['cart'])
           
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
           cart = cart_str_tojson(request.GET['cart'])
        
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
    cart = cart_str_tojson(request.session['cart_info'])

    del_list = []
    for item in cart.cart_items:
        if cart.cart_items[item].quantity == 0: del_list.append(cart.cart_items[item].name)
    
    for delete_item in del_list:
        del cart.cart_items[delete_item]

    context = {'cart': cart, 'cart_str': json.dumps(cart, indent=4, cls=CartEncoder)}
    return render(request, 'transaction/card_fillout.html', context=context)

def reset(request: HttpRequest) -> HttpRequest:
    Tshirt.objects.all().delete()
    return render(request, 'transaction/reset.html')

def restock(request: HttpRequest) -> HttpRequest:
    items = {
        "Red T-shirt": {
            "price": 12.99,
            "inventory": 30,
        },
        "Green T-shirt": {
            "price": 45.99,
            "inventory": 10,
        }
    }
    
    for item_name in items:
        if Tshirt.objects.filter(tshirt_name=item_name).exists():
            item = Tshirt.objects.get(tshirt_name=item_name)
            item.inventory = items[item_name]["inventory"]
        else:
            item = Tshirt(tshirt_name=item_name, price=items[item_name]["price"], inventory=items[item_name]["inventory"])
        item.save()

    return render(request, 'transaction/restock.html')

def stock(request: HttpRequest) -> HttpRequest:

    context = {'inventory': list(Tshirt.objects.all())}
    return render(request, 'transaction/stock.html', context=context)

def cart_str_tojson(json_string: str) -> Cart:
    cart = json.loads(json_string)

    for item in cart["cart_items"]:
        cart["cart_items"][item] = CartItem(cart["cart_items"][item])
    cart = Cart(cart)
    return cart

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def stripe_session(request):
    if request.method == 'GET':
        form_data = request.GET
        cart = cart_str_tojson(form_data["cart_info"])
        
        if Customer.objects.filter(email=form_data["email"]).exists():
            new_customer = Customer.objects.get(email=form_data["email"])
        else:
            new_customer = Customer()
            new_customer.first_name = form_data["firstname"]
            new_customer.last_name = form_data["lastname"]
            new_customer.street = form_data["shipping_address"] 
            new_customer.city = form_data["shipping_city"]
            new_customer.state = form_data["shipping_state"]
            new_customer.postal_code = form_data["shipping_zip"]
            new_customer.phone = form_data["phone"]
            new_customer.email = form_data["email"]
            new_customer.order_list = ",".join(list(cart.cart_items))
            new_customer.order_total = cart.grand_total

        with transaction.atomic():
            order_availability = True
            for item_name in cart.cart_items:
                tshirt = Tshirt.objects.select_for_update().get(tshirt_name=item_name)
                if cart.cart_items[item_name].quantity > tshirt.inventory:
                    order_availability = False
            
            if order_availability:
                all_items = []
                new_customer.charge_success = True
                new_customer.save()

                for item_name in cart.cart_items:
                    item_json = {}
                    item_json["name"] = item_name
                    item_json["quantity"] = cart.cart_items[item_name].quantity
                    item_json["currency"] = "usd"
                    item_json["amount"] = str(cart.cart_items[item_name].total).replace('.','')
                    all_items.append(item_json)
                    tshirt = Tshirt.objects.select_for_update().get(tshirt_name=item_name)
                    tshirt.inventory -= cart.cart_items[item_name].quantity
                    tshirt.save()
                
                print(all_items)
                domain_url = 'http://localhost:8000/'
                stripe.api_key = settings.STRIPE_SECRET_KEY
                try:
                    checkout_session = stripe.checkout.Session.create(
                        success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                        cancel_url=domain_url + 'cancelled/',
                        payment_method_types=['card'],
                        mode='payment',
                        line_items=all_items
                    )
                    
                    return JsonResponse({'sessionId': checkout_session['id']})
                except Exception as e:
                    return JsonResponse({'error': str(e)})

        new_customer.charge_success = False
        new_customer.save()
        return JsonResponse({'error': 'not enough inventory'})