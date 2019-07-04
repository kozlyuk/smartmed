from django.contrib import admin
from purchases.models import Company, Deal, Purchase, InvoiceLine


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'chief', 'phone']
    fieldsets = [
        (None, {'fields': [('name', 'fullname'),
                           'address',
                           'requisites',
                           'bank_requisites',
                           ('chief', 'phone'),
                           'tax_system'
                           ]})
        ]


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['number', 'type', 'partner', 'company', 'expire_date', 'created_by']
    fieldsets = [
        (None, {'fields': ['type',
                           ('number', 'date'),
                           ('partner', 'company'),
                           'expire_date',
                           'upload',
                           'comment',
                           ]})
        ]


@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'product', 'unit_price', 'quantity', 'units']
    fieldsets = [
        (None, {'fields': ['product',
                           'purchase',
                           'unit_price',
                           'quantity',
                           'units',
                           ]})
        ]


class InvoiceLineInline(admin.TabularInline):

    model = InvoiceLine
    fields = ['product', 'unit_price', 'quantity', 'units']
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):

    list_display = ['deal', 'invoice_number', 'value',
                    'in_stock', 'created_by']
    list_per_page = 50
    fieldsets = [
        (None, {'fields': ['deal',
                           ('invoice_number', 'invoice_date'),
                           'value',
                           'in_stock',
                           'upload'
                           ]}),
        ]
    inlines = [InvoiceLineInline]


admin.AdminSite.site_header = 'Smartmed ERP'
admin.AdminSite.site_title = 'Smartmed ERP'
admin.site.disable_action('delete_selected')
