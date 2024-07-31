from django.db import models
from django.contrib.auth.models import User


class Costumer(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    user = models.OneToOneField(  # costumer_1 = Costumer() # costumer.user # user = User() # user.costumer
        to=User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return self.name
