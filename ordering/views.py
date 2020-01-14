from django.shortcuts import render, redirect


# Create your views here.
def menu(request):
    return render(request,'landingup.html')


def user(request):
    return render(request,'settings.html')


def cart(request):
    return render(request,'cart.html')