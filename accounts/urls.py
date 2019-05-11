from django.urls import path

from django.contrib.auth.views import(
    LoginView,
    LogoutView,
#    PasswordResetView,
#    PasswordResetDoneView,
#    PasswordChangeView,
#    PasswordChangeDoneView,
#    PasswordResetConfirmView,
#    PasswordResetCompleteView
)
from accounts.views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

#    path('password_change/',
#         PasswordChangeView.as_view(template_name='accounts/password_change_form.html'),
#         name='password_change'),
#    path('password_change/done/',
#         PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
#         name='password_change_done'),
#    path('password_reset/',
#         PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
#         name='password_reset'),
#    path('password_reset/done/',
#         PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
#         name='password_reset_done'),
#    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
#         name='password_reset_confirm'),
#    path('reset/done/',
#         PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
#         name='password_reset_complete'),

    path('employee/list/', EmployeeList.as_view(), name='employee_list'),
    path('employee/create', EmployeeCreate.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDelete.as_view(), name='employee_delete'),

    path('partner/list/', PartnerList.as_view(), name='partner_list'),
    path('partner/create', PartnerCreate.as_view(), name='partner_create'),
    path('partner/update/<int:pk>/', PartnerUpdate.as_view(), name='partner_update'),
    path('partner/delete/<int:pk>/', PartnerDelete.as_view(), name='partner_delete'),
]
