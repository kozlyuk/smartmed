""" Views for managing purchases """

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic.edit import CreateView

from purchases.forms import AddToBasketForm


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class AddToBasketModal(CreateView):
    """ AddToBasketModal - view for add to basket modal form """
    template_name = 'add2basket.html'
    form_class = AddToBasketForm
    context_object_name = 'invoice_line'
