from django import forms
from .models import *


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeSelfUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['phone', 'avatar']


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'


class PartnerSelfUpdateForm(forms.ModelForm):
    class Meta:
        model = Partner
        exclude = ['user']
