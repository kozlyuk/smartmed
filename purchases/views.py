""" Views for managing purchases """

import datetime
from bootstrap_modal_forms.generic import BSModalUpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.views.generic.edit import UpdateView

from purchases.models import Purchase, InvoiceLine
from purchases.forms import BasketForm, AddToBasketForm
from catalogue.models import Product
from catalogue.forms import ATTRIBUTE_FORMSET


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class AddToBasketModal(UpdateView):
    """ View for add to basket modal form """
    template_name = 'includes/shop/add2basket.html'
    form_class = AddToBasketForm
    context_object_name = 'invoice_line'
    success_url = reverse_lazy('shop_home')

    def get_object(self, queryset=None):
        # get the existing object or created a new one
        product = Product.objects.get(pk=self.kwargs['product'])
        if self.request.session.get('purchase_id'):
            purchase = Purchase.objects.get(pk=self.request.session.get('purchase_id'))
        else:
            purchase = Purchase.objects.create(invoice_number='Basket')
            self.request.session['purchase_id'] = purchase.id
        obj, created = InvoiceLine.objects.get_or_create(product=product, purchase=purchase,
                                                         unit_price=product.actual_price())
#        if not created:
#            obj.quantity = obj.quantity + 1
#            obj.save()
        return obj

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['product'] = Product.objects.get(pk=self.kwargs['product'])
#        if self.request.POST:
#            context['attribute_formset'] = ATTRIBUTE_FORMSET(self.request.POST, instance=self.object)
#        else:
#            context['attribute_formset'] = ATTRIBUTE_FORMSET(instance=self.object)
#        return context


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PurchaseUpdate(UpdateView):
    """ Order review and confirmation """
    template_name = 'basket.html'
    form_class = BasketForm
    context_object_name = 'order'

    def get_object(self, queryset=None):
        if self.request.session.get('purchase_id'):
            obj = Purchase.objects.get(pk=self.request.session.get('purchase_id'))
        else:
            obj = Purchase.objects.create(invoice_number='Basket')
            self.request.session['purchase_id'] = obj.id
        return obj

    def get_initial(self):
        initials = super().get_initial()
        initials['invoice_number'] = self.object.invoice_number_generate()
        initials['invoice_date'] = datetime.date.today()
        return initials

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('purchase_id'):
            context['products_count'] = InvoiceLine.objects.filter(purchase=self.request.session.get('purchase_id'))\
                                                           .count()
        else:
            context['products_count'] = 0
        return context
