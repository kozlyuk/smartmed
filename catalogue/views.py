""" Views for managing catalogues """

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalogue.forms import Product, ProductForm, ProductFilterForm
from catalogue.forms import IMAGE_FORMSET, PRICE_RECORD_FORMSET, ATTRIBUTE_FORMSET
from catalogue.forms import Category, CategoryForm, Group, GroupForm, Brand, BrandForm


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class ShopHome(ListView):
    """ ShopHome - view for main shop template """
    template_name = 'shop_home.html'
    model = Product
    context_object_name = 'products'  # Default: object_list
    paginate_by = 50

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

    def get_context_data(self, **kwargs):  # pylint: disable=W0221
        context = super().get_context_data(**kwargs)
        context['products_count'] = Product.objects.all().count()
        context['products_filtered'] = self.get_queryset().count()
        self.request.session['products_query_string'] = self.request.META['QUERY_STRING']
        if self.request.POST:
            context['filter_form'] = ProductFilterForm(self.request.POST)
        else:
            context['filter_form'] = ProductFilterForm(self.request.GET)
        return context


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class ProductList(ListView):
    """ ProductList - view for products listing """
    model = Product
    context_object_name = 'products'  # Default: object_list
    paginate_by = 50
    success_url = reverse_lazy('manager_home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='Manager').exists():
            return super().dispatch(request, *args, **kwargs)
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

    def get_context_data(self, **kwargs):  # pylint: disable=W0221
        context = super().get_context_data(**kwargs)
        context['products_count'] = Product.objects.all().count()
        context['products_filtered'] = self.get_queryset().count()
        self.request.session['products_query_string'] = self.request.META['QUERY_STRING']
        if self.request.POST:
            context['filter_form'] = ProductFilterForm(self.request.POST)
        else:
            context['filter_form'] = ProductFilterForm(self.request.GET)
        return context


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class ProductCreate(CreateView):
    """ ProductCreate - view for creating products """
    model = Product
    form_class = ProductForm
    context_object_name = 'product'

    def get_success_url(self):
        self.success_url = reverse_lazy('product_list') + '?' +\
                           self.request.session.get('product_query_string')
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = IMAGE_FORMSET(self.request.POST,
                                                     instance=self.object)
            context['price_records_formset'] = PRICE_RECORD_FORMSET(self.request.POST,
                                                                    instance=self.object)
            context['attribute_formset'] = ATTRIBUTE_FORMSET(self.request.POST,
                                                             instance=self.object)
        else:
            context['image_formset'] = IMAGE_FORMSET(instance=self.object)
            context['price_records_formset'] = PRICE_RECORD_FORMSET(instance=self.object)
            context['attribute_formset'] = ATTRIBUTE_FORMSET(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        price_records_formset = context['price_records_formset']
        attribute_formset = context['attribute_formset']
        if image_formset.is_valid() and price_records_formset.is_valid()\
                and attribute_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()
            price_records_formset.instance = self.object
            price_records_formset.save()
            attribute_formset.instance = self.object
            attribute_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class ProductUpdate(UpdateView):
    """ ProductUpdate - view for updating products """
    model = Product
    form_class = ProductForm
    context_object_name = 'product'

    def get_success_url(self):
        self.success_url = reverse_lazy('product_list') + '?' +\
                           self.request.session.get('product_query_string')
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = IMAGE_FORMSET(self.request.POST, instance=self.object)
            context['price_records_formset'] = PRICE_RECORD_FORMSET(self.request.POST,
                                                                    instance=self.object)
            context['attribute_formset'] = ATTRIBUTE_FORMSET(self.request.POST,
                                                             instance=self.object)
        else:
            context['image_formset'] = IMAGE_FORMSET(instance=self.object)
            context['price_records_formset'] = PRICE_RECORD_FORMSET(instance=self.object)
            context['attribute_formset'] = ATTRIBUTE_FORMSET(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        price_records_formset = context['price_records_formset']
        attribute_formset = context['attribute_formset']
        if image_formset.is_valid() and price_records_formset.is_valid()\
                and attribute_formset.is_valid():
            image_formset.instance = self.object
            image_formset.save()
            price_records_formset.instance = self.object
            price_records_formset.save()
            attribute_formset.instance = self.object
            attribute_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class ProductDelete(DeleteView):
    """ ProductUpdate - view for deleting products """
    model = Product

    def get_success_url(self):
        self.success_url = reverse_lazy('product_list') + '?' +\
                           self.request.session.get('product_query_string')
        return self.success_url


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class CategoryList(ListView):
    """ CategoryList - view for categories listing """
    model = Category
    context_object_name = 'categories'  # Default: object_list
    success_url = reverse_lazy('manager_home')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class CategoryCreate(CreateView):
    """ CategoryCreate - view for creating categories """
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class CategoryUpdate(UpdateView):
    """ CategoryUpdate - view for updating categories """
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class CategoryDelete(DeleteView):
    """ CategoryDelete - view for deleting categories """
    model = Category
    success_url = reverse_lazy('category_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class GroupList(ListView):
    """ GroupList - view for groups listing """
    model = Group
    context_object_name = 'groups'  # Default: object_list
    success_url = reverse_lazy('manager_home')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class GroupCreate(CreateView):
    """ GroupCreate - view for creating groups """
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('group_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class GroupUpdate(UpdateView):
    """ GroupUpdate - view for updating groups """
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('group_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class GroupDelete(DeleteView):
    """ GroupDelete - view for deleting groups """
    model = Group
    success_url = reverse_lazy('group_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class BrandList(ListView):
    """ BrandList - view for brands listing """
    model = Brand
    context_object_name = 'brands'  # Default: object_list
    success_url = reverse_lazy('manager_home')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class BrandCreate(CreateView):
    """ BrandCreate - view for creating brands """
    model = Brand
    form_class = BrandForm
    success_url = reverse_lazy('brand_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class BrandUpdate(UpdateView):
    """ BrandUpdate - view for updating brands """
    model = Brand
    form_class = BrandForm
    success_url = reverse_lazy('brand_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class BrandDelete(DeleteView):
    """ BrandDelete - view for deleting brands """
    success_url = reverse_lazy('brand_list')
