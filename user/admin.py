from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from user.forms import UserCreateForm
from user.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    form = UserChangeForm
    model = User
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Person', {'fields': ('image', 'first_name', 'last_name', 'phone', 'expiration',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
