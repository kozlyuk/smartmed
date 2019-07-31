""" Forms for managing accounts """

from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from PIL import Image
from accounts.models import Employee, Partner


class EmployeeForm(forms.ModelForm):
    """ EmployeeForm - form for employees creating or updating """
    username = forms.CharField(label=_('Login'), max_length=255, required=True)
    password = forms.CharField(label=_('Password'), max_length=255, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=_('Confirm password'), max_length=255, required=True,
                                       widget=forms.PasswordInput)
    email = forms.EmailField(label=_('Email'), max_length=255, required=True)

    class Meta:
        model = Employee
        fields = ['name', 'position', 'phone', 'birthday', 'theme']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if password != password_confirm:
            self.add_error('password_confirm', _('Password does not match'))
        if User.objects.filter(username=username).exists():
            self.add_error('username', _('User with such username already exist'))
        if User.objects.filter(email=email).exists():
            self.add_error('email', _('User with such email already exist'))

    def save(self, commit=True):
        instance = super().save(commit=False)

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')

        user = User(username=username, email=email, is_staff=True)
        user.set_password(password)

        if commit:
            user.save()
            instance.user = user
            instance.save()
        return instance


class EmployeeSelfUpdateForm(forms.ModelForm):
    """ PartnerSelfUpdateForm - form for employees self-creating self-updating """
    x = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    y = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    width = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    height = forms.FloatField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Employee
        fields = ['name', 'phone', 'avatar', 'theme', 'birthday']

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        instance = super().save(*args, **kwargs)
        pos_x = self.cleaned_data.get('x')
        pos_y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')
        if width > 0 and height > 0:
            image = Image.open(instance.avatar)
            cropped_image = image.crop((pos_x, pos_y, width+pos_x, height+pos_y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(instance.avatar.path)
        return instance


class PartnerForm(forms.ModelForm):
    """ PartnerForm - form for partners creating or updating """
    class Meta:
        model = Partner
        fields = '__all__'


class PartnerSelfUpdateForm(forms.ModelForm):
    """ PartnerSelfUpdateForm - form for partners self-creating or self-updating """
    class Meta:
        model = Partner
        fields = ['name', 'fullname', 'legal_address', 'requisites', 'bank_requisites', 'chief',
                  'phone', 'tax_system', 'avatar', 'birthday', 'theme']
