from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class FrpUser(AbstractUser):
    gold_coin = models.IntegerField(default=0)
    silver_coin = models.IntegerField(default=0)
