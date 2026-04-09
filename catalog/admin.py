from django.contrib import admin

from catalog.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "price", "stock_qty", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("sku", "name")
    ordering = ("-id",)
