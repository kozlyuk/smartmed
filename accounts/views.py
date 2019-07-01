""" Views for managing accounts """

from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
        context['partners_count'] = Partner.objects.all().count()
        time_threshold = datetime.now() - timedelta(hours=24)
        context['sold'] = Purchase.objects.filter(created_by=self.request.user,
                                                  invoice_date__lt=time_threshold)\
                                          .exclude(status=Purchase.InBasket)\
                                          .aggregate(Sum('value')).get('value_sum') or 0.00
        context['new_orders_count'] = Purchase.objects.filter(created_by=self.request.user,
                                                              status=Purchase.NewOrder)\
                                                      .count()
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
    success_url = reverse_lazy('partner_list')


@method_decorator(login_required, name='dispatch')  # pylint: disable=too-many-ancestors
class PartnerSelfUpdate(UpdateView):
    """ PartnerSelfUpdate - view for partners self updating """
    form_class = PartnerSelfUpdateForm
    success_url = reverse_lazy('manager_home')

    def get_object(self, queryset=None):
        return Partner.objects.get(user=self.request.user)
