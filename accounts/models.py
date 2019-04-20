from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from crum import get_current_user


def avatar_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/user_<id>/<filename>
    return 'avatars/user_{0}/{1}'\
        .format(get_current_user().id, filename)


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
