from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import *


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


def make_special(modeladmin, request, queryset):
    queryset.update(is_special=True)


make_special.short_description = "Mark selected Products as special"


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_special']
    ordering = ['name']
    actions = [make_special]


admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(ProductGroup)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
