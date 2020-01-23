from django.urls import path

from ordering import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('menu/', views.menu, name='menu'),
    path('user/', views.user, name='user'),
    path('cart/', views.cart, name='cart'),
    path('specials/', views.specials, name='specials'),
    path('edit/', views.edit_user, name='edit'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove/<int:pk>', views.delete_cart_item, name='delete_cart_item'),
]
