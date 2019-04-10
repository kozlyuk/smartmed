import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView
from django.views.generic.list import ListView

from django_webix.formsets import WebixTabularInlineFormSet, WebixStackedInlineFormSet
from django_webix.views import WebixCreateWithInlinesView, WebixUpdateWithInlinesView, WebixDeleteView

from catalogue.forms import ProductForm
from catalogue.models import Product, PriceRecord, Attribute, Image


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class ProductListView(TemplateView):
    template_name = 'list.js'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['datalist'] = json.dumps([{
            'id': product.pk,
            'title': product.title,
            'upc': product.upc,
            'brand': product.brand.name,
            'category': product.category.name,
            'group': product.group.name,
        } for product in Product.objects.all()])
        return context


@method_decorator(login_required, name='dispatch')
class ProductCreateView(WebixCreateWithInlinesView):
    model = Product
    inlines = [PriceRecordInline, AttributeInline, ImageInline]
    form_class = ProductForm


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(WebixUpdateWithInlinesView):
    model = Product
    inlines = [PriceRecordInline, AttributeInline, ImageInline]
    form_class = ProductForm


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(WebixDeleteView):
    model = Product
