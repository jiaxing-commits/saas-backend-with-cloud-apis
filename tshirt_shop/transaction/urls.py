from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('fillout/', views.fillout, name='fillout'),
    path('restock/', views.restock, name='restock'),
    path('stock/', views.stock, name='stock'),
    path('reset/', views.reset, name='reset'),
    path('config/', views.stripe_config, name='config'),
    path('stripe_session/', views.stripe_session, name='stripe_session'),
    path('success_fulfill/', views.success_fulfill, name='success_fulfill'),
    path('unsuccess_fulfill/', views.unsuccess_fulfill, name='unsuccess_fulfill'),
    url(r'^quantity_change/$', views.quantity_change, name='quantity_change'),
    url(r'^remove_item/$', views.remove_item, name='remove_item'),
]