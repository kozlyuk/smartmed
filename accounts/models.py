""" Models for managing accounts """

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


THEME_CHOICES = (
    ('bl', _('Black')),
    ('wh', _('White')),
)


def avatar_directory_path(instance, filename):
    """ file will be uploaded to MEDIA_ROOT/avatars/user_id/<filename> """
    return 'avatars/user_{0}/{1}'.format(instance.user.id, filename)


class Employee(models.Model):
    """ Employee model - extending of User model for employees """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField('ПІБ', max_length=50, unique=True)
    position = models.CharField('Посада', max_length=50)
    phone = models.CharField('Телефон', max_length=13, blank=True)
    avatar = models.ImageField('Фото', upload_to=avatar_directory_path,
                               default='avatars/no_image.jpg')
    birthday = models.DateField('День народження', blank=True, null=True)
    theme = models.CharField(_('Theme'), max_length=2, choices=THEME_CHOICES, default='bl')

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['name']

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):  # pylint: disable=W0221
        self.user.delete()
        return super().delete(*args, **kwargs)


class Partner(models.Model):
    """ Partner model - extending of User model for partners """
    TAXATION_CHOICES = (
        ('wvat', _('With VAT')),
        ('wovat', _('Without VAT')),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=45)
    fullname = models.CharField(_('Full name'), max_length=255)
    legal_address = models.CharField(_('Legal address'), max_length=255, blank=True)
    requisites = models.CharField(_('Requisites'), max_length=255, blank=True)
    bank_requisites = models.CharField(_('Bank details'), max_length=255, blank=True)
    chief = models.CharField(_('Chief'), max_length=45, blank=True)
    phone = models.CharField(_('Phone'), max_length=13, blank=True)
    tax_system = models.CharField(_('Tax system'), max_length=5,
                                  choices=TAXATION_CHOICES, default='wvat')
    avatar = models.ImageField('Фото', upload_to=avatar_directory_path,
                               default='avatars/no_image.jpg')
    birthday = models.DateField('День народження', blank=True, null=True)
    theme = models.CharField(_('Theme'), max_length=2, choices=THEME_CHOICES, default='bl')

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
        ordering = ['name']

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):  # pylint: disable=W0221
        self.user.delete()
        return super().delete(*args, **kwargs)


class Address(models.Model):
    """ Model contains Addresses of delivery of Partners """
    DELIVERY_COMPANY_CHOICES = (
        ('NP', _('NEW POST')),
    )
    DELIVERY_METHOD_CHOICES = (
        ('OD', _('Delivery to post office')),
        ('AD', _('Address delivery')),
    )
    partner = models.ForeignKey(Partner, verbose_name=_('Partner'), on_delete=models.CASCADE)
    city = models.CharField(_('City'), max_length=45)
    delivery_company = models.CharField(_('Delivery company'), max_length=2,
                                        choices=DELIVERY_COMPANY_CHOICES, default='NP')
    delivery_method = models.CharField(_('Delivery method'), max_length=2,
                                       choices=DELIVERY_METHOD_CHOICES, default='OD')
    address_line = models.CharField(_('Address'), max_length=255, blank=True)
    post_office = models.PositiveSmallIntegerField(_('Post office number'), blank=True, null=True)
    main = models.BooleanField(_('Main address'), default=False)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Address')

    def __str__(self):
        return self.partner.name + self.get_delivery_method_display
