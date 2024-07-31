from django.db import models
from costumerapp.models import Costumer
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=125)
    descriptions = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    qty = models.IntegerField(default=0)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Категория',
    )
    rating = models.IntegerField(default=0)
    guarantee = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.ManyToManyField(
        to=Costumer,
        blank=True
    )
    views_qty = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Profile(models.Model):
    bio = models.TextField(null=True, blank=True)
    social_link = models.CharField(max_length=125)
    phone_number = models.CharField(max_length=125)
    user = models.OneToOneField(
        to=User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
