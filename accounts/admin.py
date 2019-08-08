from django.contrib import admin
from accounts.models import Employee, Partner


@admin.register(Employee)
class Employee(admin.ModelAdmin):
    list_display = ['name', 'position', 'phone']
    fieldsets = [
        (None, {'fields': [('user', 'name'),
                           ('position', 'phone'),
                           'avatar',
                           'birthday',
                           'theme',
                           ]})
        ]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'chief', 'phone']
    fieldsets = [
        (None, {'fields': [('user', 'name'),
                           'fullname',
                           'requisites',
                           'bank_requisites',
                           ('chief', 'phone'),
                           'tax_system',
                           'theme',
                           ]})
        ]
