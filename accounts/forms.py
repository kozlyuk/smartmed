from django import forms
from accounts.models import Employee, Partner
from PIL import Image


class EmployeeForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Employee
        fields = ('avatar', 'x', 'y', 'width', 'height', )

    def save(self):
        photo = super(EmployeeForm, self).save()

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
    class Meta:
        model = Partner
        fields = '__all__'


class PartnerSelfUpdateForm(forms.ModelForm):
    class Meta:
        model = Partner
        exclude = ['user']
