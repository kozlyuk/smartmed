from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django_userforeignkey.models.fields import UserForeignKey
from warehouse.models import Stock
from stdimage.models import StdImageField



def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product/product_upc/<filename>
    return 'product/{0}/{1}'.format(instance.product.upc, filename)


class Category(models.Model):
    name = models.CharField(_('Category name'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(_('Group name'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(_('Brand name'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(_('Product title'), max_length=255)
    upc = models.CharField(_('Product UPC'), max_length=32, unique=True)
    category = models.ForeignKey(Category, verbose_name=_('Product Category'), on_delete=models.PROTECT)
    group = models.ForeignKey(Group, verbose_name=_('Product Group'), on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, verbose_name=_('Product Brand'), on_delete=models.PROTECT)
    description = models.TextField(_('Product description'), blank=True)
    warranty_terms = models.PositiveSmallIntegerField(_('Warranty terms, months'), blank=True, null=True)
    default_uom = models.CharField(_('Default units of measurement'), max_length=8, default=_('pcs.'))
    pack_size = models.PositiveSmallIntegerField(_('Pack size'), default=10)
    min_store_quantity = models.IntegerField(_('Minimal store quantity'), default=10)
    has_instances = models.BooleanField(_('Has instances'), default=True)
    has_attributes = models.BooleanField(_('Has attributes'), default=True)
    is_discountable = models.BooleanField(_('Discountable'), default=True)
    is_active = models.BooleanField(_('Active'), default=True)
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-date_created', 'title']

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = StdImageField(_('Product Image'), upload_to=image_directory_path,
                          variations={
                                   'large': (400, 400, True),
                                   'thumbnail': (100, 100, True),
                                })

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')

    def __str__(self):
        return self.image.url


class PriceRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_date = models.DateField(_('Actual from'), default=now)
    regular_price = models.DecimalField(_('Product price'), max_digits=8, decimal_places=2, default=0)
    discount_price_1 = models.DecimalField(_('Discount price'), max_digits=8, decimal_places=2, default=0)
    discount_price_2 = models.DecimalField(_('Discount price'), max_digits=8, decimal_places=2, default=0)
    discount_price_3 = models.DecimalField(_('Discount price'), max_digits=8, decimal_places=2, default=0)
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Price Record')
        verbose_name_plural = _('Price Records')

    def __str__(self):
        return str(self.regular_price) + ' ' + settings.DEFAULT_CURRENCY


class AttributeType(models.Model):
    name = models.CharField(_('Attribute'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('Attribute type')
        verbose_name_plural = _('Attribute types')

    def __str__(self):
        return self.name


class Attribute(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    type = models.ForeignKey(AttributeType, verbose_name=_('Attribute type'), on_delete=models.PROTECT)

    class Meta:
        unique_together = ('product', 'type')

    def __str__(self):
        return self.product.title + ' ' + self.type.name


class AttributeValue(models.Model):
    value = models.CharField(_('Attribute Value'), max_length=45)
    attribute = models.ForeignKey(Attribute, verbose_name=_('Attribute name'), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Attribute Value')
        verbose_name_plural = _('Attribute Values')

    def __str__(self):
        return self.value + ' ' + self.attribute.product.title


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    instance_name = models.CharField(_('Instance name'), max_length=64, blank=True)
    serial_number = models.CharField(_('Serial Number'), max_length=32, unique=True)
    warranty_end_date = models.DateField(_('Warranty end date'))
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Product Instance')
        verbose_name_plural = _('Product Instances')

    def __str__(self):
        return self.serial_number
