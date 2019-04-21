from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django.utils.translation import gettext_lazy as _


def avatar_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/user_<id>/<filename>
    return 'avatars/{1}'\
        .format(filename)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField('ПІБ', max_length=50, unique=True)
    position = models.CharField('Посада', max_length=50)
    phone = models.CharField('Телефон', max_length=13, blank=True)
    avatar = StdImageField('Фото', upload_to=avatar_directory_path, default='avatars/no_image.jpg', variations={
                           'large': (400, 400, True),
                           'thumbnail': (100, 100, True),
                           })
    birthday = models.DateField('День народження', blank=True, null=True)

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        ordering = ['name']

    def __str__(self):
        return self.name


class Partner(models.Model):
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
    tax_system = models.CharField(_('Tax system'), max_length=5, choices=TAXATION_CHOICES, default='wvat')
    avatar = StdImageField('Фото', upload_to=avatar_directory_path, default='avatars/no_image.jpg', variations={
                           'large': (400, 400, True),
                           'thumbnail': (100, 100, True),
                           })
    birthday = models.DateField('День народження', blank=True, null=True)

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
        ordering = ['name']

    def __str__(self):
        return self.name
