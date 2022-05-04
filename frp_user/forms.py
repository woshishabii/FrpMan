from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import FrpUser


class FrpUserCreationForm(UserCreationForm):
    class Meta:
        model = FrpUser
        fields = ('username', 'email', 'password')


class FrpUserChangeForm(UserChangeForm):
    class Meta:
        model = FrpUser
        fields = ('username', 'email', 'password', 'gold_coin', 'silver_coin')
