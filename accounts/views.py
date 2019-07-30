""" Views for managing accounts """

from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.db.models import Sum

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from accounts.models import Employee, Partner
from accounts.forms import EmployeeForm, EmployeeSelfUpdateForm, PartnerForm, PartnerSelfUpdateForm
from purchases.models import Purchase


@method_decorator(login_required, name='dispatch')
class ManagerHome(TemplateView):
    """ ShopHome - view for manager dashboard template """
    template_name = 'manager_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time_threshold = datetime.now() - timedelta(hours=24)
        orders_total = Purchase.objects.filter(Q(status=Purchase.NewOrder),
                                               Q(status=Purchase.Confirmed),
                                               Q(status=Purchase.Sent))
        context['orders_value_tth'] = orders_total.filter(invoice_date__lt=time_threshold)\
                                                  .aggregate(Sum('value')).get('value_sum') or 0.00
        context['new_orders_count'] = Purchase.objects.filter(status=Purchase.NewOrder)\
                                                      .count()
        context['confirmed_orders_count'] = Purchase.objects.filter(status=Purchase.Confirmed)\
                                                            .count()
        context['sent_orders_count_tth'] = Purchase.objects.filter(invoice_date__lt=time_threshold,
                                                                   status=Purchase.Sent)\
                                                           .count()
        context['not_paid_orders_count'] = orders_total.filter(pay_status=Purchase.NotPaid) \
                                                       .count()
        context['advance_orders_count'] = orders_total.filter(pay_status=Purchase.AdvancePaid) \
                                                      .count()
        context['paid_orders_count'] = orders_total.filter(pay_status=Purchase.PaidUp) \
                                                   .count()

        context['partners_count'] = Partner.objects.all().count()
        paid_orders_sum = orders_total.filter(pay_status=Purchase.PaidUp)\
                                      .aggregate(Sum('value')).get('value_sum') or 0.00
        advance_orders_sum = orders_total.filter(pay_status=Purchase.PaidUp)\
                                         .aggregate(Sum('value')).get('value_sum') or 0.00

        return context


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class EmployeeList(ListView):
    """ EmployeeList - view for employees listing """
    model = Employee
    context_object_name = 'employees'  # Default: object_list
    success_url = reverse_lazy('manager_home')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class EmployeeCreate(CreateView):
    """ EmployeeCreate - view for creating employees """
    template_name = 'employee_create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class EmployeeUpdate(UpdateView):
    """ EmployeeUpdate - view for updating employees """
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class EmployeeDelete(DeleteView):
    """ EmployeeDelete - view for deleting employees """
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class EmployeeSelfUpdate(UpdateView):
    """ EmployeeSelfUpdate - view for employees self updating """
    form_class = EmployeeSelfUpdateForm
    success_url = reverse_lazy('manager_home')

    def get_object(self, queryset=None):
        return Employee.objects.get(user=self.request.user)


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PartnerList(ListView):
    """ PartnerList - view for partners listing """
    model = Partner
    context_object_name = 'partners'  # Default: object_list
    success_url = reverse_lazy('manager_home')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PartnerCreate(CreateView):
    """ PartnerCreate - view for partners creating """
    form_class = PartnerForm
    success_url = reverse_lazy('partner_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PartnerUpdate(UpdateView):
    """ PartnerUpdate - view for partners updating """
    form_class = PartnerForm
    success_url = reverse_lazy('partner_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PartnerDelete(DeleteView):
    """ PartnerDelete - view for partners deleting """
    model = Partner
    template_name = 'partner_confirm_delete.html'
    success_url = reverse_lazy('partner_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PartnerSelfUpdate(UpdateView):
    """ PartnerSelfUpdate - view for partners self updating """
    form_class = PartnerSelfUpdateForm
    success_url = reverse_lazy('manager_home')

    def get_object(self, queryset=None):
        return Partner.objects.get(user=self.request.user)
