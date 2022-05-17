# saas-backend-with-cloud-apis

1.```pip3 install -r requirements.txt```
2.```cd tshirt_shop/```
3.```python3 manage.py runserver```
4.Go to http://127.0.0.1:8000/ on a web browser.
5.Go to http://127.0.0.1:8000/checkout to buy things.

Other Utility Urls
1. http://127.0.0.1:8000/stock : shows inventory of the shop
2. http://127.0.0.1:8000/restock : restock inventory of the shop
3. http://127.0.0.1:8000/customers : shows customers (also show if their payment was successful or not via Charge_success boolean)
