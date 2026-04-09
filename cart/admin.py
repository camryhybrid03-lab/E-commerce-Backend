from django.contrib import admin

from cart.models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "updated_at")
    search_fields = ("user__username", "user__email")
    ordering = ("-id",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "updated_at")
    list_select_related = ("cart", "product")
    ordering = ("-id",)
