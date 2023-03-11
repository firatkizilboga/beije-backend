from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Order(models.Model):
    pass

class Address(models.Model):
    pass

class Subscription(models.Model):
    pass