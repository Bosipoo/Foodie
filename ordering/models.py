from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
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


class Admin(models.Model):
    """This represents an administrator in our application"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Customer(models.Model):
    """This represents a customer in our application"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.IntegerField()


class Payment(models.Model):
    """This represents a transaction in our application"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=20)
    card_no = models.IntegerField()


class Group(models.Model):
    """This represents a product group in our application"""
    name = models.CharField(max_length=20)


class SubGroup(models.Model):
    """This represents a product subgroup in our application"""
    name = models.CharField(max_length=20)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, related_name='subgroups')


class Product(models.Model):
    """This represents a product in our application"""
    name = models.CharField(max_length=25)
    subgroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE)
