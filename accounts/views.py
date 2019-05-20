from .forms import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from purchases.models import Purchase
from datetime import datetime, timedelta
from django.db.models import Sum


@method_decorator(login_required, name='dispatch')
class ManagerHome(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ManagerHome, self).get_context_data(*args, **kwargs)
        context['partners_count'] = Partner.objects.all().count()
        time_threshold = datetime.now() - timedelta(hours=24)
        context['sold'] = Purchase.objects.filter(created_by=self.request.user,
                                                  invoice_date__lt=time_threshold)\
                                          .exclude(status=Purchase.InBasket)\
                                          .aggregate(Sum('value'))
        context['new_orders_count'] = Purchase.objects.filter(created_by=self.request.user,
                                                              status=Purchase.NewOrder)\
                                                      .Count()
        return context


@method_decorator(login_required, name='dispatch')
class EmployeeList(ListView):
    model = Employee
    success_url = reverse_lazy('manager_home')


@method_decorator(login_required, name='dispatch')
class EmployeeCreate(CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')


@method_decorator(login_required, name='dispatch')
class EmployeeUpdate(UpdateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')


@method_decorator(login_required, name='dispatch')
class EmployeeDelete(DeleteView):
    model = Employee
    success_url = reverse_lazy('employee_list')


@method_decorator(login_required, name='dispatch')
class EmployeeSelfUpdate(UpdateView):
    model = Employee
    form_class = EmployeeSelfUpdateForm
    success_url = reverse_lazy('manager_home')

    def get_object(self):
        return Employee.objects.get(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class PartnerList(ListView):
    model = Partner
    success_url = reverse_lazy('manager_home')


@method_decorator(login_required, name='dispatch')
class PartnerCreate(CreateView):
    model = Partner
    form_class = PartnerForm
    success_url = reverse_lazy('partner_list')


@method_decorator(login_required, name='dispatch')
class PartnerUpdate(UpdateView):
    model = Partner
    form_class = PartnerForm
    success_url = reverse_lazy('partner_list')


@method_decorator(login_required, name='dispatch')
class PartnerDelete(DeleteView):
    model = Partner
    success_url = reverse_lazy('partner_list')


@method_decorator(login_required, name='dispatch')
class PartnerSelfUpdate(UpdateView):
    model = Partner
    form_class = PartnerSelfUpdateForm
    success_url = reverse_lazy('manager_home')

    def get_object(self):
        return Partner.objects.get(user=self.request.user)
