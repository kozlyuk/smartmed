""" Forms for managing catalogues """

from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from purchases.models import Purchase, InvoiceLine
from django.utils.translation import gettext_lazy as _


class AddToBasketForm(forms.ModelForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = InvoiceLine
        fields = ['product', 'purchase', 'quantity', 'unit_price']

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')

        if quantity == 0:
            self.add_error('quantity', _('The quantity of goods can not be zero'))
        return cleaned_data



class BasketForm(forms.ModelForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = Purchase
        fields = ['invoice_number', 'invoice_date', 'value']
