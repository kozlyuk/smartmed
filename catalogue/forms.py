from django import forms
from django.forms import inlineformset_factory
from catalogue.models import *
from django.utils.translation import gettext_lazy as _


class ProductFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)

        category = [(category.id, category.name) for category in Category.objects.all()]
        category.insert(0, (0, "Всі"))

        group = [(group.id, group.name) for group in Group.objects.all()]
        group.insert(0, (0, "Всі"))

        brand = [(brand.id, brand.name) for brand in Brand.objects.all()]
        brand.insert(0, (0, "Всі"))

        self.fields['category'].choices = category
        self.fields['group'].choices = group
        self.fields['brand'].choices = brand

    category = forms.ChoiceField(label=_('Category'), required=False, widget=forms.Select(attrs={"onChange": 'submit()'}))
    group = forms.ChoiceField(label=_('Group'), required=False, widget=forms.Select(attrs={"onChange": 'submit()'}))
    brand = forms.ChoiceField(label=_('Brand'), required=False, widget=forms.Select(attrs={"onChange": 'submit()'}))
    filter = forms.CharField(label=_('Search string'), max_length=255, required=False)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'upc', 'category', 'group', 'brand', 'description',
                  'warranty_terms', 'default_uom', 'pack_size', 'min_store_quantity',
                  'has_instances', 'has_attributes', 'is_discountable', 'is_active']


class ImageInlineForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


ImageFormSet = inlineformset_factory(Product, Image, form=ImageInlineForm, extra=1)


class PriceRecordsInlineForm(forms.ModelForm):
    class Meta:
        model = PriceRecord
        fields = ['from_date', 'regular_price', 'discount_price_1', 'discount_price_2', 'discount_price_3']


PriceRecordsFormSet = inlineformset_factory(Product, PriceRecord, form=PriceRecordsInlineForm, extra=1)


class AttributeInlineForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['type']


AttributeFormSet = inlineformset_factory(Product, Attribute, form=AttributeInlineForm, extra=1)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']