from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalogue.forms import *
from catalogue.models import Product, PriceRecord, Attribute, Image


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'main.html'


@method_decorator(login_required, name='dispatch')
class ProductList(ListView):
    model = Product
    context_object_name = 'products'  # Default: object_list
    paginate_by = 50
    success_url = reverse_lazy('home_page')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='Manager').exists():
            return super(ProductList, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        products = Product.objects.all()
        search_string = self.request.GET.get('filter', '').split()
        category = self.request.GET.get('category', '0')
        group = self.request.GET.get('group', '0')
        brand = self.request.GET.get('brand', '0')
        order = self.request.GET.get('o', '0')
        for word in search_string:
            products = products.filter(Q(title__icontains=word) |
                                       Q(upc__icontains=word) |
                                       Q(description__icontains=word))
        if category != '0':
            products = products.filter(category=category)
        if group != '0':
            products = products.filter(group=group)
        if brand != '0':
            products = products.filter(brand=brand)
        if order != '0':
            products = products.order_by(order)
        return products

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['products_count'] = Product.objects.all().count()
        context['products_filtered'] = self.get_queryset().count()
        self.request.session['products_query_string'] = self.request.META['QUERY_STRING']
        if self.request.POST:
            context['filter_form'] = ProductFilterForm(self.request.POST)
        else:
            context['filter_form'] = ProductFilterForm(self.request.GET)
        return context



@method_decorator(login_required, name='dispatch')
class ProductCreate(CreateView):
    model = Product


@method_decorator(login_required, name='dispatch')
class ProductUpdate(UpdateView):
    model = Product


@method_decorator(login_required, name='dispatch')
class ProductDelete(DeleteView):
    model = Product
