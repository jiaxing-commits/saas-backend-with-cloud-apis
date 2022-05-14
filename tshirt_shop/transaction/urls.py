from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    url(r'^quantity_change/$', views.quantity_change, name='quantity_change'),
    url(r'^remove_item/$', views.remove_item, name='remove_item'),
]