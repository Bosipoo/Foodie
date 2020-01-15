from django.urls import path

from ordering import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('menu/', views.menu, name='menu'),
    path('user/', views.user, name='user'),
    path('cart/', views.cart, name='cart'),
    path('edit/', views.edit_user, name='edit'),
]
