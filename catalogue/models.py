from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from crum import get_current_user
from warehouse.models import Stock
from stdimage.models import StdImageField


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product/product_upc/<filename>
    return 'product/{0}'.format(instance.upc)


class Category(models.Model):
    name = models.CharField(_('Category name'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(_('Group name'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(_('Brand name'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(_('Product title'), max_length=255)
    upc = models.CharField(_('Product UPC'), max_length=32, unique=True)
    category = models.ForeignKey(Category, verbose_name=_('Product Category'), on_delete=models.PROTECT)
    group = models.ForeignKey(Group, verbose_name=_('Product Group'), on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, verbose_name=_('Product Brand'), on_delete=models.PROTECT)
    description = models.TextField(_('Product description'), blank=True)
    warranty_terms = models.PositiveSmallIntegerField(_('Warranty terms'), blank=True)
    default_uom = models.CharField(_('Default units of measurement'), max_length=16, default=_('pcs.'))
    pack_size = models.PositiveSmallIntegerField(_('Pack size'), default=10)
    min_store_quantity = models.IntegerField(_('Minimal store quantity'), default=10)
    has_instances = models.BooleanField(_('Has instances'), default=True)
    has_attributes = models.BooleanField(_('Has attributes'), default=True)
    is_discountable = models.BooleanField(_('Discountable'), default=True)
    is_active = models.BooleanField(_('Active'), default=True)
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='products_creator', on_delete=models.PROTECT)
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title + ' ' + self.brand

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = get_current_user()
        super(Product, self).save(*args, **kwargs)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = StdImageField(_('Product Image'), upload_to=image_directory_path, default='product/no_image.jpg', variations={
                                   'large': (400, 400, True),
                                   'thumbnail': (100, 100, True),
                                })
    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')

    def __str__(self):
        return self.image


class PriceRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_date = models.DateField(_('Actual from'), default=now)
    price = models.DecimalField(_('Product price'), max_digits=8, decimal_places=2, default=0)
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='price_records_creator', on_delete=models.PROTECT)
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Price Record')
        verbose_name_plural = _('Price Records')

    def __str__(self):
        return self.price + ' ' + settings.DEFAULT_CURRENCY

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = get_current_user()
        super(PriceRecord, self).save(*args, **kwargs)


class AttributeType(models.Model):
    attribute_name = models.CharField(_('Attribute'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __str__(self):
        return self.attribute_name


class Attribute(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.PROTECT)
    attribute_type = models.ForeignKey(AttributeType, verbose_name=_('Attribute value'), on_delete=models.PROTECT)

    class Meta:
        unique_together = ('category', 'attribute_type')


class AttributeValue(models.Model):
    value = models.CharField(_('Value'), max_length=45)
    attribute = models.ForeignKey(Attribute, verbose_name=_('Attribute'), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Attribute Value')
        verbose_name_plural = _('Attribute Values')

    def __str__(self):
        return self.value


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    instance_name = models.CharField(_('Instance name'), max_length=64, blank=True)
    serial_number = models.CharField(_('Serial Number'), max_length=32, unique=True)
    warranty_end_date = models.DateField(_('Warranty end date'))
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='product_instances_creator', on_delete=models.PROTECT)
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Product Instance')
        verbose_name_plural = _('Product Instances')

    def __str__(self):
        return self.serial_number

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = get_current_user()
        super(ProductInstance, self).save(*args, **kwargs)
