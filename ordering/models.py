from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """This represents a User object within our system"""
    username = None
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()


class Admin(models.Model):
    """This represents an administrator in our application"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Customer(models.Model):
    """This represents a customer in our application"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(null=True, max_length=11)

    def __str__(self):
        return self.user.get_full_name()


class ProductGroup(models.Model):
    """This represents a product group in our application"""
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    """This represents a product in our application"""
    name = models.CharField(max_length=25)
    image = models.ImageField(default="image not found.jpg")
    price = models.FloatField()
    group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    is_special = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    """This represents a transaction in our application"""
    DELIVERY_STATUS = [('p', 'Pending'), ('c', 'Confirmed'), ('d', 'Delivered')]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.FloatField()
    order_no = models.CharField(max_length=10)
    delivery_status = models.CharField(choices=DELIVERY_STATUS, max_length=10, default='p')

    def __str__(self):
        return self.order_no, " - ", self.product, " - ", self.delivery_status
