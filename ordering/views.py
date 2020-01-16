from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ordering.models import *


def menu(request):
    groups = ProductGroup.objects.all().order_by("name")
    context = {
        'groups': groups
    }
    return render(request, 'menu.html', context)


def user(request):
    return render(request, 'user.html')


@login_required
def cart(request):
    return render(request, 'cart.html')


def signup(request):
    if request.method == "GET":
        return render(request, 'registration/register.html')
    else:
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']

        user = User.objects.create_user(email, password, first_name=first_name, last_name=last_name)
        user.save()
        user.customer.address = address
        user.customer.phone = phone
        user.customer.save()
        return HttpResponse('Account has been created successfully.')


def edit_user(request):
    phone = request.POST['phone']
    address = request.POST['address']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    user = request.user

    user.customer.phone = phone
    user.customer.address = address
    user.customer.save()
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return redirect('user')


def add_to_cart(request):
    return None
