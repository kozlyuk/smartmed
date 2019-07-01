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
    user = models.OneToOneField(User, on_delete=models.PROTECT)
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


class Partner(models.Model):
    """ Partner model - extending of User model for partners """
    TAXATION_CHOICES = (
        ('wvat', _('With VAT')),
        ('wovat', _('Without VAT')),
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=45)
    fullname = models.CharField(_('Full name'), max_length=255)
    address = models.CharField(_('Legal address'), max_length=255, blank=True)
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
