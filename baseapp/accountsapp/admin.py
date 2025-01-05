from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'date_joined'
    )
    
admin.site.register(Account, AccountAdmin)
