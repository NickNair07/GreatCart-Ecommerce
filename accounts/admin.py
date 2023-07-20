from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'username')  # to make the username also clickable
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)    # (,) is provided because to make it a tuple

    # required because using custom user model
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)