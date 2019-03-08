from django.db import models
from django.utils.translation import gettext_lazy as _
#from catalogue.models import Product


class Warehouse(models.Model):
    name = models.CharField(_('Warehouse name'), max_length=32, unique=True)
    address = models.CharField(_('Warehouse address'), max_length=255)

    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey('catalogue.Product', verbose_name=_('Product'), on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('Warehouse'), on_delete=models.PROTECT)
    quantity_in_hand = models.IntegerField(_('Quantity in hand'))

    class Meta:
        unique_together = ('product', 'warehouse')
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')

    def __str__(self):
        return self.quantity_in_hand
