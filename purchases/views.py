""" Views for managing purchases """

import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView

from purchases.forms import BasketForm, AddToBasketForm

from purchases.models import Purchase
from catalogue.models import Product


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class AddToBasketModal(CreateView):
    """ View for add to basket modal form """
    template_name = 'includes/shop/add2basket.html'
    form_class = AddToBasketForm
    context_object_name = 'invoice_line'
    success_url = reverse_lazy('shop_home')

    def get_initial(self):
        initials = super().get_initial()
        product = Product.objects.get(pk=self.kwargs['product'])
        initials['product'] = product.pk
        initials['unit_price'] = product.actual_price()
        if not self.request.session.get('purchase_id'):
            new_purchase = Purchase.objects.create(invoice_number='Basket')
            self.request.session['purchase_id'] = new_purchase.id
        initials['purchase'] = self.request.session.get('purchase_id')
        return initials


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PurchaseUpdate(UpdateView):
    """ Order review and confirmation """
    template_name = 'basket.html'
    form_class = BasketForm
    context_object_name = 'order'

    def get_initial(self):
        initials = super().get_initial()
        initials['invoice_number'] = self.object.invoice_number_generate()
        initials['invoice_date'] = datetime.date.today()
        return initials
