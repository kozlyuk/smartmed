""" Forms for managing catalogues """

from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from purchases.models import Purchase, InvoiceLine
from django.utils.translation import gettext_lazy as _


class AddToBasketForm(forms.ModelForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = InvoiceLine
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=65535)


class BasketForm(forms.ModelForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = Purchase
        fields = ['invoice_number', 'invoice_date', 'value']
