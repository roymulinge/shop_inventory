from django.contrib import admin
from .models import Product, Sale
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'selling_price', 'buying_price', 'created_at')
    search_fields = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_sold', 'total_price', 'date')
    list_filter = ('date',)
