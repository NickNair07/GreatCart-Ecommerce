from django.contrib import admin
from .models import Cart, Cart_item

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')    

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart)
admin.site.register(Cart_item)