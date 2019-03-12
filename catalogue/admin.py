from django.contrib import admin
from catalogue.models import Category, Group, Brand, Product, Image, PriceRecord
from catalogue.models import AttributeType, Attribute, AttributeValue, ProductInstance
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.db import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    fieldsets = [
        (None, {'fields': ['name',
                           ]})
        ]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    fieldsets = [
        (None, {'fields': ['name',
                           ]})
        ]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    fieldsets = [
        (None, {'fields': ['name',
                           ]})
        ]


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150"  style="object-fit: cover;"/></a> %s ' % \
                (image_url, image_url, file_name, _('')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


class ImageInline(admin.TabularInline):
    model = Image
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    fields = ['image']
    extra = 0


class PriceRecordInline(admin.TabularInline):
    model = PriceRecord
    fields = ['price', 'from_date']
    extra = 0


class AttributeInline(admin.TabularInline):
    model = Attribute
    fields = ['type']
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'upc', 'category', 'group', 'brand', 'is_active']
    fieldsets = [
        (None, {'fields': [('title', 'upc'),
                           ('category', 'group', 'brand'),
                           ('pack_size', 'min_store_quantity', 'default_uom'),
                           ('warranty_terms', 'has_instances', 'has_attributes', 'is_discountable', 'is_active'),
                           'description',
                           ]})
        ]
    inlines = [PriceRecordInline, AttributeInline, ImageInline]


@admin.register(AttributeType)
class AttributeTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    fieldsets = [
        (None, {'fields': ['name',
                           ]})
        ]


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    fields = ['value']
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'type']
    fieldsets = [
        (None, {'fields': ['product',
                           'type'
                           ]})
        ]
    inlines = [AttributeValueInline]


@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ['product', 'instance_name', 'serial_number', 'attribute_value', 'stock']
    fieldsets = [
        (None, {'fields': [('product', 'instance_name'),
                           ('serial_number', 'warranty_end_date'),
                           ('attribute_value', 'stock'),
                           ]})
        ]
