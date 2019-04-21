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
    list_display = ['type', 'number', 'company', 'expire_date']
    fieldsets = [
        (None, {'fields': [('number', 'date'),
                           ('partner', 'company'),
                           'expire_date',
                           'upload',
                           'comment',
                           ]})
        ]


class InvoiceLineInline(admin.TabularInline):

    model = InvoiceLine
    fields = ['product', 'unit_price', 'quantity', 'units']
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):

    list_display = ['deal', 'invoice_number', 'value_wc',
                    'in_stock', 'creator']
    list_per_page = 50
    fieldsets = [
        (None, {'fields': ['deal',
                           ('invoice_number', 'invoice_date'),
                           ('value', 'currency'),
                           ('warehouse', 'in_stock'),
                           'upload'
                           ]}),
        ]
    inlines = [InvoiceLineInline]


admin.AdminSite.site_header = 'Smartmed ERP'
admin.AdminSite.site_title = 'Smartmed ERP'
admin.site.disable_action('delete_selected')
