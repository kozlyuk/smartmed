""" Forms for managing accounts """

from django import forms
from PIL import Image
from accounts.models import Employee, Partner


class EmployeeForm(forms.ModelForm):
    """ EmployeeForm - form for employees creating or updating """
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Employee
        fields = ('avatar', 'x', 'y', 'width', 'height', )

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        photo = super(EmployeeForm, self).save(*args, **kwargs)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo


class EmployeeSelfUpdateForm(forms.ModelForm):
    """ PartnerSelfUpdateForm - form for employees self-creating self-updating """
#    x = forms.FloatField(widget=forms.HiddenInput())
#    y = forms.FloatField(widget=forms.HiddenInput())
#    width = forms.FloatField(widget=forms.HiddenInput())
#    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Employee
        fields = ('phone', 'avatar') #, 'x', 'y', 'width', 'height', )

#    def save(self):
#        photo = super(EmployeeSelfUpdateForm, self).save()

#        x = self.cleaned_data.get('x')
#        y = self.cleaned_data.get('y')
#        w = self.cleaned_data.get('width')
#        h = self.cleaned_data.get('height')

#        image = Image.open(photo.file)
#        cropped_image = image.crop((x, y, w+x, h+y))
#        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
#        resized_image.save(photo.file.path)

#        return photo


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
