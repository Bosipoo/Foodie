"""foodie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from ordering import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('add-cart/', views.add_to_cart, name="add to cart"),
                  path('register/', views.signup, name="register"),
                  path('', include('django.contrib.auth.urls')),
                  url(r'^payment/', views.payment, name="payment"),
                  path('', include('ordering.urls')),
                  url(r'^paypal/', include('paypal.standard.pdt.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
