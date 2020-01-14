from django.urls import path
from ordering import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('user/', views.user, name='user'),
    path('cart/', views.cart, name='cart')
]