from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.views.decorators.http import require_GET
from paypal.standard.pdt.views import process_pdt

from ordering.models import *


def menu(request):
    groups = ProductGroup.objects.all().order_by("name")
    context = {
        'groups': groups
    }
    return render(request, 'menu.html', context)


def user(request):
    return render(request, 'user.html')


def cart(request):
    price = 0
    for key, value in request.session.get('cart', dict()).items():
        product_price = Product.objects.get(id=value['product_id']).price
        price += int(value['quantity']) * product_price

    cart = request.session.get('cart', dict())
    return render(request, 'cart.html', {'cart': cart, 'total': price})


def signup(request):
    if request.method == "GET":
        return render(request, 'registration/register.html')
    else:
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        phone = request.POST['phone']

        user = User.objects.create_user(email, password, first_name=first_name, last_name=last_name)
        user.save()
        user.customer.phone = phone
        user.customer.save()
        login(request, user)
        return redirect('user')


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


from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm


@require_GET
def payment(request):
    pdt_obj, failed = process_pdt(request)
    context = {"failed": failed, "pdt_obj": pdt_obj}
    if not failed:

        # WARNING!
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)

        if pdt_obj.receiver_email == request.user.email:
            # ALSO: for the same reason, you need to check the amount
            # received etc. are all what you expect.

            # Do whatever action is needed, then:
            return render(request, 'valid_payment.html', context)
    return render(request, 'invalid_payment.html', context)


@login_required
def checkout(request):
    # What you want the button to do.
    paypal_dict = {
        "currency_code": "USD",
        "business": request.user.email,
        "amount": request.POST['total'],
        "item_name": 'Food from Foodie',
        "invoice": 10001,
        "notify_url": request.build_absolute_uri(reverse('paypal-pdt')),
        "return": request.build_absolute_uri(reverse('payment')),
        "cancel_return": request.build_absolute_uri(reverse('menu')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "checkout.html", context)


def add_to_cart(request):
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    quantity = int(request.GET['quantity'])
    cart = request.session.get('cart', dict())
    if product.name in cart:
        quantity += int(request.session['cart'][product.name]['quantity'])
    cart[product.name] = {'product_id': product_id, 'quantity': quantity}
    request.session['cart'] = cart

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def specials(request):
    specials = Product.objects.filter(is_special=True)
    return render(request, 'specials.html', {'specials': specials, 'quantity': 0})

#
# @login_required
# def checkout(request):
#     return render(request, 'checkout.html')
def delete_cart_item(request, pk):
    cart = request.session.get('cart', dict())
    product = Product.objects.get(id=pk)
    del cart[product.name]
    request.session['cart'] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))