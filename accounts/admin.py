from django.contrib import admin
from .models import *


#@admin.register(Partner)
#class PartnerAdmin(admin.ModelAdmin):
#    list_display = ['name', 'chief', 'phone']
#    fieldsets = [
#        (None, {'fields': [('user', 'name'),
#                           'fullname',
#                           'address',
#                           'requisites',
#                           'bank_requisites',
#                           ('chief', 'phone'),
#                           'tax_system'
#                           ]})
#        ]
