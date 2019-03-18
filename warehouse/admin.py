from django.contrib import admin

from warehouse.models import Warehouse, Stock


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    fieldsets = [
        (None, {'fields': ['name',
                           'address'
                           ]})
        ]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity_in_hand']
    fieldsets = [
# test
        (None, {'fields': ['product',
                           'warehouse',
                           'quantity_in_hand'
                           ]})
        ]
