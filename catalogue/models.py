from django.db import models
from django.utils.translation import gettext_lazy as _


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product/product_upc/<filename>
    return 'product/{0}/{1}'\
        .format(instance.upc, filename)


class Category(models.Model):
    category_name = models.CharField(_('Category'), max_length=45, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Attribute_type(models.Model):
    attribute_name = models.CharField(_('Attribute'), max_length=45, unique=True)

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')


class Attribute(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.PROTECT)
    attribute_type = models.ForeignKey(Attribute_type, verbose_name=_('Attribute value'), on_delete=models.PROTECT)

    class Meta:
        unique_together = ('category', 'attribute_type')


class Attribute_value(models.Model):
    value = models.CharField(_('Value'), max_length=45)
    attribute = models.ForeignKey(Attribute, verbose_name=_('Attribute'), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')


class Product(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    upc = models.CharField(_('UPC'), max_length=64, unique=True)
    category = models.ForeignKey(Category, _('Product Category'), on_delete=models.PROTECT)
    attribute_value = models.ForeignKey(Attribute_value, verbose_name=_('Attribute value'), on_delete=models.PROTECT)
    price = models.DecimalField(_('Price'), max_digits=8, decimal_places=2, default=0)
    warranty = models.PositiveSmallIntegerField(_('Warranty'), blank=True)
    description = models.TextField(_('Description'), blank=True)
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)
    is_discountable = models.BooleanField(_('Discountable'), default=True)


    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.Foreignkey(Product)
    image = models.ImageField(upload_to='user_images')

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
