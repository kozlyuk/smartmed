from django.db import models
from oscar.apps.partner.models import Partner, StockRecord
from oscar.apps.catalogue.models import Product
from django.contrib.auth.models import User
from django.conf import settings
from .formatChecker import ContentTypeRestrictedFileField
from datetime import datetime
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from crum import get_current_user


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/projects/user_<id>/Year/Month/<filename>
    return 'archive/{0}/{1}/{2}'\
        .format(datetime.now().year, datetime.now().month, filename)


class Company(models.Model):
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

    def __str__(self):
        return self.name


class Deal(models.Model):
    number = models.CharField(_('Deal number'), max_length=45)
    date = models.DateField(_('Deal date'), default=now)
    customer = models.ForeignKey(Partner, verbose_name=_('Partner'), on_delete=models.PROTECT)
    company = models.ForeignKey(Company, verbose_name=_('Company'), on_delete=models.PROTECT)
    expire_date = models.DateField(_('Deal expire date'))
    comment = models.TextField(_('Comment'), blank=True)
    upload = ContentTypeRestrictedFileField(_('Electronic copy'), upload_to=user_directory_path,
                                              content_types=['application/pdf',
                                                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                                             'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
                                              max_upload_size=26214400,
                                              blank=True, null=True)
    # Creator and Date information
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='deals_creator', on_delete=models.PROTECT)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        unique_together = ('number', 'customer')
        verbose_name = _('Deal')
        verbose_name_plural = _('Deals')
        ordering = ['-date_created', 'customer', '-number']

    def __str__(self):
        return self.number + ' ' + self.customer.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = get_current_user()
        super(Deal, self).save(*args, **kwargs)


class Purchase(models.Model):
    deal = models.ForeignKey(Deal, verbose_name=_('Deal'), on_delete=models.PROTECT)
    invoice_number = models.CharField(_('Invoice number'), max_length=45)
    invoice_date = models.DateField(_('Invoice date'), default=now)
    products = models.ManyToManyField(Product, through='InvoiceLine', related_name='products',
                                   verbose_name=_('Goods'), blank=True)
    in_stock = models.BooleanField(_('Available in stock'), default=False)
    value = models.DecimalField(_('Value'), max_digits=8, decimal_places=2, default=0)
    currency = models.CharField(_('Currency'), max_length=12, default=settings.OSCAR_DEFAULT_CURRENCY)
    upload = ContentTypeRestrictedFileField(_('Electronic copy'), upload_to=user_directory_path,
                                              content_types=['application/pdf',
                                                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                                             'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
                                              max_upload_size=26214400,
                                              blank=True, null=True)
    # Creator and Date information
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='purchases_creator', on_delete=models.PROTECT)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        unique_together = ('invoice_number', 'deal')
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')
        ordering = ['-date_created', '-invoice_number']

    def __str__(self):
        return self.invoice_number + ' ' + self.deal.customer.name

    def value_wc(self):
        return str(self.value) + ' ' + self.currency

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = get_current_user()
        super(Purchase, self).save(*args, **kwargs)


class Payment(models.Model):
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
    payment_date = models.DateField(_('Payment date'), default=now)
    payment_value = models.DecimalField(_('Value'), max_digits=8, decimal_places=2)
    # Creator and Date information
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name=_('payments_creator'), on_delete=models.PROTECT)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.name


class InvoiceLine(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Goods'), on_delete=models.PROTECT)
    purchase = models.ForeignKey(Purchase, verbose_name=_('Purchase'), on_delete=models.PROTECT)
    stockrecord = models.OneToOneField(StockRecord, null=True, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(_('Amount'), default=1)
    units = models.CharField(_('Units'), max_length=16, default=_('pcs.'))
    unit_price = models.DecimalField(_('Unit price'), max_digits=8, decimal_places=2, default=0)