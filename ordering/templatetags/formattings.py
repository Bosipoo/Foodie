from django import template
from ordering.models import Product

register = template.Library()


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter
def getproductattribute(value, arg):
    product = Product.objects.get(id = value)
    return product.__getattribute__(arg)

@register.filter
def getimageurl(value):
    product = Product.objects.get(id = value)
    return product.image.url
