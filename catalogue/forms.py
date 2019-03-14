from django_webix.forms import WebixModelForm
from catalogue.models import Product


class ProductForm(WebixModelForm):
    class Meta:
        model = Product
        fields = ['title', 'upc', 'category', 'group', 'brand', 'pack_size', 'min_store_quantity', 'default_uom',
                  'warranty_terms', 'has_instances', 'has_attributes', 'is_discountable', 'is_active', 'description',
                  ]
