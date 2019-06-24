""" Forms for managing catalogues """

from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from purchases.models import Purchase, InvoiceLine


class AddToBasketForm(BSModalForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = InvoiceLine
        fields = ['product', 'purchase', 'quantity', 'unit_price']


class BasketForm(forms.ModelForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = Purchase
        fields = ['invoice_number', 'invoice_date', 'products', 'value']
