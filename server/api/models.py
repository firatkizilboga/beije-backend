from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class AdminUser(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    address_line1 = models.CharField(max_length=255, blank=False, null=False)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

class Item(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

from datetime import timedelta
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullfillment_frequency = models.IntegerField(default=30)
    start_date = models.DateField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    last_fullfillment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=255, blank=False, null=False, default='Subscription')

    @property
    def items(self):
        return SubscriptionItem.objects.filter(subscription=self)
    
    @property
    def total(self):
        total = 0
        for item in self.items:
            total += item.item.price * item.quantity
        return total
    
    @property
    def next_fullfillment_date(self):
        return self.last_fullfillment_date + timedelta(days=self.fullfillment_frequency)
    

    #these functions are for the instance of the subscription
    def fullfill(self):
        self.last_fullfillment_date = self.next_fullfillment_date
        self.save()


    
    def cancel(self):
        self.is_active = False
        self.save()
    
    def reactivate(self):
        self.is_active = True
        self.save()
    
#create a Item Subscription relation
class SubscriptionItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    #make sure item and subscription are unique together
    class Meta:
        unique_together = ('item', 'subscription')

from datetime import datetime
class Order(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_paid_date = models.DateTimeField(blank=True, null=True)
    is_shipped = models.BooleanField(default=False)
    is_shipped_date = models.DateTimeField(blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    is_delivered_date = models.DateTimeField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)
    is_cancelled_date = models.DateTimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        if not self.total_price or self.total_price == 0:
            self.total_price = self.subscription.totalæ
        super(Order, self).save(*args, **kwargs)

    def cancel(self):
        self.is_cancelled = True
        self.is_cancelled_date = datetime.now()
        self.save()
    
    def pay(self):
        self.is_paid = True
        self.is_paid_date = datetime.now()
        self.save()
    
    def ship(self):
        self.is_shipped = True
        self.is_shipped_date = datetime.now()
        self.save()
    
    def deliver(self):
        self.is_delivered = True
        self.is_delivered_date = datetime.now()
        self.save()
    
