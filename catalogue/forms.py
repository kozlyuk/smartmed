from django import forms
from catalogue.models import Product
from django.utils.translation import gettext_lazy as _


class ProductFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)

        category = [(category.id, category.name) for category in Product.objects.all()]
        category.insert(0, (0, "Всі"))

        group = [(group.id, group.name) for group in Product.objects.all()]
        group.insert(0, (0, "Всі"))

        brand = [(brand.id, brand.name) for brand in Product.objects.all()]
        brand.insert(0, (0, "Всі"))

        self.fields['category'].choices = category
        self.fields['group'].choices = group
        self.fields['brand'].choices = brand

    category = forms.ChoiceField(label=_('Category'), required=False, widget=forms.Select(attrs={"onChange": 'submit()'}))
    group = forms.ChoiceField(label=_('Group'), required=False, widget=forms.Select(attrs={"onChange": 'submit()'}))
    brand = forms.ChoiceField(label=_('Brand'), required=False, widget=forms.Select(attrs={"onChange": 'submit()'}))
    filter = forms.CharField(label=_('Search string'), max_length=255, required=False)
