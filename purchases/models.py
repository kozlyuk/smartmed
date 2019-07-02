""" Models for managing purchases """

import datetime
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_userforeignkey.models.fields import UserForeignKey
from catalogue.models import Product
from accounts.models import Partner
from warehouse.models import Warehouse
from purchases.formatChecker import ContentTypeRestrictedFileField


def docs_directory_path(filename):
    """  file will be uploaded to MEDIA_ROOT/projects/user_<id>/Year/Month/<filename> """
    return 'archive/{0}/{1}/{2}'\
        .format(datetime.datetime.now().year, datetime.datetime.now().month, filename)


class Company(models.Model):
    """ Model contains Companies requisites for using in Deals and Invoices """
    TAXATION_CHOICES = (
        ('wvat', _('With VAT')),
        ('wovat', _('Without VAT')),
    )
    name = models.CharField(_('Name'), max_length=45)
    fullname = models.CharField(_('Full name'), max_length=255)
    address = models.CharField(_('Legal address'), max_length=255, blank=True)
    requisites = models.CharField(_('Requisites'), max_length=255, blank=True)
    bank_requisites = models.CharField(_('Bank details'), max_length=255, blank=True)
    chief = models.CharField(_('Chief'), max_length=45, blank=True)
    phone = models.CharField(_('Phone'), max_length=13, blank=True)
    tax_system = models.CharField(_('Tax system'), max_length=5, choices=TAXATION_CHOICES, default='wvat')

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['name']

    def __str__(self):
        return self.name


class Deal(models.Model):
    """ Model contains Deals """
    DEAL_CHOICES = (
        ('sa', _('Sale')),
        ('pu', _('Purchase')),
    )
    type = models.CharField(_('Deal type'), max_length=2, choices=DEAL_CHOICES, default='sa')
    number = models.CharField(_('Deal number'), max_length=45)
    date = models.DateField(_('Deal date'), default=datetime.date.today)
    expire_date = models.DateField(_('Deal expire date'))
    partner = models.ForeignKey(Partner, verbose_name=_('Partner'), on_delete=models.PROTECT, null=True)
    company = models.ForeignKey(Company, verbose_name=_('Company'), on_delete=models.PROTECT)
    comment = models.TextField(_('Comment'), blank=True)
    upload = ContentTypeRestrictedFileField(_('Electronic copy'), upload_to=docs_directory_path,
                                            content_types=['application/pdf',
                                                           'application/vnd.openxmlformats-officedocument'
                                                           '.spreadsheetml.sheet',
                                                           'application/vnd.openxmlformats-officedocument'
                                                           '.wordprocessingml.document'],
                                            max_upload_size=26214400,
                                            blank=True, null=True)
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        unique_together = ('number', 'partner')
        verbose_name = _('Deal')
        verbose_name_plural = _('Deals')
        ordering = ['-date_created', 'partner', '-number']

    def __str__(self):
        return self.number + ' ' + self.partner.name


class Purchase(models.Model):
    """ Model contains Purchases, Orders, Baskets """
    InBasket = 'IB'
    NewOrder = 'NO'
    Cancelled = 'CN'
    Confirmed = 'CF'
    Sent = 'ST'
    Received = 'RC'
    Returned = 'RT'
    STATUS_CHOICES = (
        (InBasket, _('Products in  basket')),
        (NewOrder, _('New order')),
        (Cancelled, _('Order canceled')),
        (Confirmed, _('Order confirmed')),
        (Sent, _('Order sent')),
        (Received, _('Order received')),
        (Returned, _('Order returned')),
    )
    NotPaid = 'NP'
    AdvancePaid = 'AP'
    PaidUp = 'PU'
    PAYMENT_STATUS_CHOICES = (
        (NotPaid, 'Не оплачений'),
        (AdvancePaid, 'Оплачений аванс'),
        (PaidUp, 'Оплачений')
        )
    deal = models.ForeignKey(Deal, verbose_name=_('Deal'), blank=True, null=True, on_delete=models.PROTECT)
    status = models.CharField(_('Deal type'), max_length=2, choices=STATUS_CHOICES, default=InBasket)
    pay_status = models.CharField('Статус оплати', max_length=2, choices=PAYMENT_STATUS_CHOICES, default=NotPaid)
    invoice_number = models.CharField(_('Invoice number'), max_length=45)
    invoice_date = models.DateField(_('Invoice date'), default=datetime.date.today)
    products = models.ManyToManyField(Product, through='InvoiceLine', related_name='products',
                                      verbose_name=_('Goods'), blank=True)
    in_stock = models.BooleanField(_('Available in stock'), default=False)
    arrival_date = models.DateField(_('Arrival date'), default=datetime.date.today)
    value = models.DecimalField(_('Value'), max_digits=8, decimal_places=2, default=0)
    upload = ContentTypeRestrictedFileField(_('Electronic copy'), upload_to=docs_directory_path,
                                            content_types=['application/pdf',
                                                           'application/vnd.openxmlformats-officedocument'
                                                           '.spreadsheetml.sheet',
                                                           'application/vnd.openxmlformats-officedocument'
                                                           '.wordprocessingml.document'],
                                            max_upload_size=26214400,
                                            blank=True, null=True)
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        unique_together = ('invoice_number', 'deal')
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')
        ordering = ['-date_created', '-invoice_number']

    def __str__(self):
        return self.invoice_number

    def value_wc(self):
        """ return purchase value with currency"""
        return str(self.value) + ' ' + settings.DEFAULT_CURRENCY
    value_wc.short_description = _('Invoice Value')

    def value_total(self):
        """ return calculated from invoice_lines purchase value"""
        return self.invoiceline_set.extra(select={"item_total": "quantity * unit_price"})\
                                   .aggregate(total=Sum("item_total"))
    value_total.short_description = _('Calculated invoice value')

    def value_total_wc(self):
        """ return calculated from invoice_lines purchase value with currency"""
        return str(self.value_total) + ' ' + settings.DEFAULT_CURRENCY
    value_total_wc.short_description = _('Calculated invoice value')

    @classmethod
    def invoice_number_generate(cls):
        """ return autogenerated invoice number"""
        today_str = datetime.date.today().strftime('%Y%m%d')
        today_orders_count = cls.objects.filter(invoice_number__startswith=today_str).count()
        return today_str + '-' + str(today_orders_count + 1)
    value_total_wc.short_description = _('Generated invoice number')


class Payment(models.Model):
    """ Model contains Payments for Purchases model """
    PayOnDelivery = 'PD'
    BankPayment = 'BP'
    BankCard = 'BC'
    PAYMENT_TYPE_CHOICES = (
        (PayOnDelivery, _('Pay on delivery')),
        (BankPayment, _('Bank payment')),
        (BankCard, _('Bank card'))
    )
    purchase = models.ForeignKey(Partner, verbose_name=_('Partner'), on_delete=models.CASCADE)
    payment_type = models.CharField(_('Payment type'), max_length=2, choices=PAYMENT_TYPE_CHOICES, default='BP')
    payment_date = models.DateField(_('Payment date'), default=datetime.date.today)
    payment_value = models.DecimalField(_('Value'), max_digits=8, decimal_places=2)
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.payment_value


class InvoiceLine(models.Model):
    """ Model contains InvoiceLines for Purchases model """
    product = models.ForeignKey(Product, verbose_name=_('Goods'), on_delete=models.PROTECT)
    purchase = models.ForeignKey(Purchase, verbose_name=_('Purchase'), on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(_('Amount'), default=1)
    units = models.CharField(_('Units'), max_length=16, default=_('pcs.'))
    unit_price = models.DecimalField(_('Unit price'), max_digits=8, decimal_places=2, default=0)
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('Warehouse'), blank=True, null=True,
                                  on_delete=models.PROTECT)

    def value_total(self):
        """ return calculated invoice_line value"""
        return self.unit_price * self.quantity
    value_total.short_description = _('Calculated invoice_line value')

    def value_total_wc(self):
        """ return calculated invoice_line value with currency"""
        return str(self.value_total) + ' ' + settings.DEFAULT_CURRENCY
    value_total_wc.short_description = _('Calculated invoice value')
