""" Forms for managing accounts """

from django import forms
from PIL import Image
from accounts.models import Employee, Partner


class EmployeeForm(forms.ModelForm):
    """ EmployeeForm - form for employees creating or updating """

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeSelfUpdateForm(forms.ModelForm):
    """ PartnerSelfUpdateForm - form for employees self-creating self-updating """
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Employee
        fields = ['phone', 'avatar', 'x', 'y', 'width', 'height']

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        instance = super(EmployeeSelfUpdateForm, self).save(*args, **kwargs)
        pos_x = self.cleaned_data.get('x')
        pos_y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')
        image = Image.open(instance.avatar)
        cropped_image = image.crop(pos_x, pos_y, width+pos_x, height+pos_y)
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
        fields = ['name', 'fullname', 'address', 'requisites', 'bank_requisites', 'chief',
                  'phone', 'tax_system', 'avatar', 'birthday', 'theme']
