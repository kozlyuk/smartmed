""" Forms for managing catalogues """

from django import forms
from purchases.models import Purchase


#class AddToBasketForm(forms.Form):
#    """ ProductFilterForm - form for products filtering """

#    class Meta:
#        model = InvoiceLine
#        fields = ['product', 'purchase', 'quantity', 'unit_price']


class BasketForm(forms.Form):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = Purchase
        fields = ['__all__']
