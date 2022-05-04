from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import FrpUserCreationForm, FrpUserChangeForm
from .models import FrpUser

# Register your models here.


class FrpUserAdmin(UserAdmin):
    add_form = FrpUserCreationForm
    form = FrpUserChangeForm
    model = FrpUser
    list_display = ['username', 'email', 'gold_coin', 'silver_coin']


admin.site.register(FrpUser, FrpUserAdmin)
