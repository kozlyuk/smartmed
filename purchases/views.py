""" Views for managing purchases """

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic.edit import CreateView, UpdateView

from purchases.forms import BasketForm

from purchases.models import Purchase, InvoiceLine


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class AddToBasketModal(CreateView):
    """ AddToBasketModal - view for add to basket modal form """
    template_name = 'add2basket.html'
    model = InvoiceLine
#    form_class = AddToBasketForm
    context_object_name = 'invoice_line'

    def get_initial(self):
        initials = super().get_initial()
        initials['product'] = self.request.GET['product']
        if not self.request.session('purchase_id'):
            new_purchase = Purchase.objects.create(invoice_number='Basket')
            self.request.session['purchase_id'] = new_purchase.id
        initials['purchase'] = self.request.session['purchase_id']
        return initials


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PurchaseUpdate(UpdateView):
    """ AddToBasketModal - view for add to basket modal form """
    template_name = 'add2basket.html'
    form_class = BasketForm
    context_object_name = 'invoice_line'
