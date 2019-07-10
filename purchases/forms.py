""" Forms for managing catalogues """

from django import forms
from django.forms import inlineformset_factory
from purchases.models import Purchase, InvoiceLine


class AddToBasketForm(forms.ModelForm):
    """ ProductFilterForm - form for products filtering """

    class Meta:
        model = InvoiceLine
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=65535)


class InvoiceLineInlineForm(forms.ModelForm):
    """ PriceRecordInlineForm - form for price records inlines creating or updating """
    class Meta:
        model = InvoiceLine
        fields = ['quantity']


INVOICE_LINE_FORMSET = inlineformset_factory(Purchase, InvoiceLine, form=InvoiceLineInlineForm, extra=0)
