""" Views for managing purchases """

import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy

from django.views.generic.edit import UpdateView

from purchases.models import Purchase, InvoiceLine
from purchases.forms import AddToBasketForm
from catalogue.models import Product, Category, Group, Brand
from purchases.forms import INVOICE_LINE_FORMSET


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class AddToBasketModal(UpdateView):
    """ View for add to basket modal form """
    template_name = 'includes/shop/add2basket.html'
    form_class = AddToBasketForm
    context_object_name = 'invoice_line'

    def get_object(self, queryset=None):
        # get the existing object or created a new one
        product = Product.objects.get(pk=self.kwargs['product'])
        if 'purchase_id' in self.request.session and \
                Purchase.objects.filter(pk=self.request.session.get('purchase_id')).exists():
            purchase = Purchase.objects.get(pk=self.request.session.get('purchase_id'))
        else:
            purchase = Purchase.objects.create(invoice_number='Basket')
            self.request.session['purchase_id'] = purchase.id
        obj, created = InvoiceLine.objects.get_or_create(product=product,
                                                         purchase=purchase,
                                                         defaults={'unit_price': product.actual_price()})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs['product'])
        context['product'] = product
        context['unit_price'] = str(product.actual_price())
#        if self.request.POST:
#            context['attribute_formset'] = ATTRIBUTE_FORMSET(self.request.POST, instance=self.object)
#        else:
#            context['attribute_formset'] = ATTRIBUTE_FORMSET(instance=self.object)
        return context

    def get_success_url(self):
        if self.request.POST.get('save_go_basket'):
            return reverse('basket')
        return reverse('shop_products')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PurchaseUpdate(UpdateView):
    """ Order review and confirmation """
    template_name = 'basket.html'
    context_object_name = 'order'
    fields = []
    success_url = reverse_lazy('shop_products')

    def get_object(self, queryset=None):
        if 'purchase_id' in self.request.session and \
                Purchase.objects.filter(pk=self.request.session.get('purchase_id')).exists():
            purchase = Purchase.objects.get(pk=self.request.session.get('purchase_id'))
        else:
            purchase = Purchase.objects.create(invoice_number='Basket')
            self.request.session['purchase_id'] = purchase.id
        return purchase

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_id = self.request.session.get('purchase_id')
        if purchase_id:
            context['products_count'] = InvoiceLine.objects.filter(purchase=purchase_id).count()
        else:
            context['products_count'] = 0
        context['categories'] = [(category.id, category.name) for category in Category.objects.all()]
        context['groups'] = [(group.id, group.name) for group in Group.objects.all()]
        context['brands'] = [(brand.id, brand.name) for brand in Brand.objects.all()]
        if self.request.POST:
            context['invoice_line_formset'] = INVOICE_LINE_FORMSET(self.request.POST, instance=self.object)
        else:
            context['invoice_line_formset'] = INVOICE_LINE_FORMSET(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Check if invoice_line_formset is valid then save it and call form_valid for main form.
        """
        context = self.get_context_data()
        invoice_line_formset = context['invoice_line_formset']
        if invoice_line_formset.is_valid():
            invoice_line_formset.instance = self.object
            invoice_line_formset.save()
            form.instance.invoice_number = self.object.invoice_number_generate()
            form.instance.invoice_date = datetime.date.today()
            form.instance.status = Purchase.Confirmed
            form.instance.value = self.object.value_total()
            if self.request.session.get('purchase_id'):
                del self.request.session['purchase_id']
            return super().form_valid(form)
        return self.form_invalid(form)
