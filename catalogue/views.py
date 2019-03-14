import json

from django.views.generic import TemplateView

from django_webix.formsets import WebixTabularInlineFormSet, WebixStackedInlineFormSet
from django_webix.views import WebixCreateWithInlinesView, WebixUpdateWithInlinesView, WebixDeleteView

from catalogue.forms import ProductForm
from catalogue.models import Product, PriceRecord, Attribute, Image


class HomeView(TemplateView):
    template_name = 'base.html'


class PriceRecordInline(WebixStackedInlineFormSet):
    model = PriceRecord
    fields = '__all__'


class AttributeInline(WebixStackedInlineFormSet):
    model = Attribute
    fields = '__all__'


class ImageInline(WebixStackedInlineFormSet):
    model = Image
    fields = '__all__'


class ProductListView(TemplateView):
    template_name = 'list.js'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['datalist'] = json.dumps([{
            'id': i.pk,
            'title': i.title
        } for i in Product.objects.all()])
        return context


class ProductCreateView(WebixCreateWithInlinesView):
    model = Product
    inlines = [PriceRecordInline, AttributeInline, ImageInline]
    form_class = ProductForm


class ProductUpdateView(WebixUpdateWithInlinesView):
    model = Product
    inlines = [PriceRecordInline, AttributeInline, ImageInline]
    form_class = ProductForm


class ProductDeleteView(WebixDeleteView):
    model = Product
