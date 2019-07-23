""" Forms for managing catalogues """

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from PIL import Image as Img

from catalogue.models import Product, Category, Group, Brand, Image, PriceRecord, Attribute


class ProductFilterForm(forms.Form):
    """ ProductFilterForm - form for products filtering """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category = [(category.id, category.name) for category in Category.objects.all()]
        category.insert(0, (0, "Всі"))

        group = [(group.id, group.name) for group in Group.objects.all()]
        group.insert(0, (0, "Всі"))

        brand = [(brand.id, brand.name) for brand in Brand.objects.all()]
        brand.insert(0, (0, "Всі"))

        self.fields['category'].choices = category
        self.fields['group'].choices = group
        self.fields['brand'].choices = brand

    category = forms.ChoiceField(label=_('Category'), required=False,
                                 widget=forms.Select(attrs={"onChange": 'submit()'}))
    group = forms.ChoiceField(label=_('Group'), required=False,
                              widget=forms.Select(attrs={"onChange": 'submit()'}))
    brand = forms.ChoiceField(label=_('Brand'), required=False,
                              widget=forms.Select(attrs={"onChange": 'submit()'}))
    filter = forms.CharField(label=_('Search string'), max_length=255, required=False)


class ProductForm(forms.ModelForm):
    """ ProductForm - form for products creating or updating """
    class Meta:
        model = Product
        fields = ['title', 'upc', 'group', 'brand', 'description',
                  'warranty_terms', 'default_uom', 'pack_size', 'min_store_quantity',
                  'has_instances', 'is_discountable', 'is_active']


class ImageInlineForm(forms.ModelForm):
    """ ImageInlineForm - form for images inlines creating or updating """
    x = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    y = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    width = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    height = forms.FloatField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Image
        fields = ['image', 'x', 'y', 'width', 'height']

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        instance = super().save(*args, **kwargs)
        pos_x = self.cleaned_data.get('x')
        pos_y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')
        if width > 0 and height > 0:
            image = Img.open(instance.image)
            cropped_image = image.crop((pos_x, pos_y, width+pos_x, height+pos_y))
            resized_image = cropped_image.resize((200, 200), Img.ANTIALIAS)
            resized_image.save(instance.image.path)
        return instance


IMAGE_FORMSET = inlineformset_factory(Product, Image, form=ImageInlineForm, extra=0)


class PriceRecordInlineForm(forms.ModelForm):
    """ PriceRecordInlineForm - form for price records inlines creating or updating """
    class Meta:
        model = PriceRecord
        fields = ['from_date', 'regular_price',
                  'discount_price_1', 'discount_price_2', 'discount_price_3']


PRICE_RECORD_FORMSET = inlineformset_factory(Product, PriceRecord,
                                             form=PriceRecordInlineForm, extra=0)


class AttributeInlineForm(forms.ModelForm):
    """ AttributeInlineForm - form for attributes inlines creating or updating """
    class Meta:
        model = Attribute
        fields = ['type']


ATTRIBUTE_FORMSET = inlineformset_factory(Product, Attribute,
                                          form=AttributeInlineForm, extra=0)


class CategoryForm(forms.ModelForm):
    """ CategoryForm - form for categories inlines creating or updating """
    class Meta:
        model = Category
        fields = ['name']


class GroupForm(forms.ModelForm):
    """ GroupForm - form for attributes inlines creating or updating """
    class Meta:
        model = Group
        fields = ['name']


class BrandForm(forms.ModelForm):
    """ BrandForm - form for brands inlines creating or updating """
    class Meta:
        model = Brand
        fields = ['name']
