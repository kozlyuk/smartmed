from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalogue.forms import *


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'base.html'


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

# test

@method_decorator(login_required, name='dispatch')
class ProductListFull(ListView):
    model = Product
    context_object_name = 'products'  # Default: object_list
    paginate_by = 50
    

# test



@method_decorator(login_required, name='dispatch')
class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    context_object_name = 'product'

    def get_success_url(self):
        self.success_url = reverse_lazy('product_list') + '?' + self.request.session.get('product_query_string')
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, instance=self.object)
            context['price_records_formset'] = PriceRecordsFormSet(self.request.POST, instance=self.object)
            context['attribute_formset'] = AttributeFormSet(self.request.POST, instance=self.object)
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
            context['price_records_formset'] = PriceRecordsFormSet(instance=self.object)
            context['attribute_formset'] = AttributeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        price_records_formset = context['price_records_formset']
        attribute_formset = context['attribute_formset']
        if image_formset.is_valid() and price_records_formset.is_valid() and attribute_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()
            price_records_formset.instance = self.object
            price_records_formset.save()
            attribute_formset.instance = self.object
            attribute_formset.save()
            return super(ProductCreate, self).form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = 'product'

    def get_success_url(self):
        self.success_url = reverse_lazy('product_list') + '?' + self.request.session.get('product_query_string')
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, instance=self.object)
            context['price_records_formset'] = PriceRecordsFormSet(self.request.POST, instance=self.object)
            context['attribute_formset'] = AttributeFormSet(self.request.POST, instance=self.object)
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
            context['price_records_formset'] = PriceRecordsFormSet(instance=self.object)
            context['attribute_formset'] = AttributeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        price_records_formset = context['price_records_formset']
        attribute_formset = context['attribute_formset']
        if image_formset.is_valid() and price_records_formset.is_valid() and attribute_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()
            price_records_formset.instance = self.object
            price_records_formset.save()
            attribute_formset.instance = self.object
            attribute_formset.save()
            return super(ProductUpdate, self).form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ProductDelete(DeleteView):
    model = Product

    def get_success_url(self):
        self.success_url = reverse_lazy('product_list') + '?' + self.request.session.get('product_query_string')
        return self.success_url


@method_decorator(login_required, name='dispatch')
class CategoryCreate(CreateView):
    model = Category


@method_decorator(login_required, name='dispatch')
class CategoryUpdate(UpdateView):
    model = Category


@method_decorator(login_required, name='dispatch')
class CategoryDelete(DeleteView):
    model = Category
