""" Forms for managing catalogues """

from django import forms
from purchases.models import InvoiceLine


class AddToBasketForm(forms.Form):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = InvoiceLine
        fields = ['quantity']


#class BasketForm(forms.Form):
#    """ ProductFilterForm - form for products filtering """

#    class Meta:
#        model = Purchase
#        fields = ['quantity']
