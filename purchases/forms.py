""" Forms for managing catalogues """

from django import forms
from purchases.models import Purchase, InvoiceLine


class AddToBasketForm(forms.ModelForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = InvoiceLine
        fields = ['product', 'purchase', 'quantity', 'unit_price']


class BasketForm(forms.ModelForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = Purchase
        fields = ['invoice_number', 'invoice_date', 'products', 'value']