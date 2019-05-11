from .forms import *
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class EmployeeList(ListView):
    model = Employee
    success_url = reverse_lazy('base')


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
    success_url = reverse_lazy('base')

    def get_object(self):
        return Employee.objects.get(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class PartnerList(ListView):
    model = Partner
    success_url = reverse_lazy('base')


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
    success_url = reverse_lazy('base')

    def get_object(self):
        return Partner.objects.get(user=self.request.user)
