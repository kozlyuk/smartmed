from django_webix.forms import WebixModelForm
from catalogue.models import Product


class ProductForm(WebixModelForm):
    class Meta:
        model = Product
        fields = '__all__'
