"""account URL Configuration"""
from django.urls import path, reverse_lazy

from django.contrib.auth import views

from accounts.views import ManagerHome
from accounts.views import EmployeeList, EmployeeCreate, EmployeeUpdate, EmployeeDelete, EmployeeSelfUpdate
from accounts.views import PartnerList, PartnerCreate, PartnerUpdate, PartnerDelete, PartnerSelfUpdate

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='auth.html'), name='login'),
    path('logout/', views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # dashboard url's
    path('dashboard/', ManagerHome.as_view(), name='manager_home'),

    path('dashboard/employee/', EmployeeList.as_view(), name='employee_list'),
    path('dashboard/employee/create/', EmployeeCreate.as_view(), name='employee_create'),
    path('dashboard/employee/update/<int:pk>/', EmployeeUpdate.as_view(), name='employee_update'),
    path('dashboard/employee/delete/<int:pk>/', EmployeeDelete.as_view(), name='employee_delete'),
    path('dashboard/employee/self_update/', EmployeeSelfUpdate.as_view(), name='employee_self_update'),

    path('dashboard/partner/list/', PartnerList.as_view(), name='partner_list'),
    path('dashboard/partner/create', PartnerCreate.as_view(), name='partner_create'),
    path('dashboard/partner/update/<int:pk>/', PartnerUpdate.as_view(), name='partner_update'),
    path('dashboard/partner/delete/<int:pk>/', PartnerDelete.as_view(), name='partner_delete'),
    path('dashboard/partner/self_update/', PartnerSelfUpdate.as_view(), name='partner_self_update'),
]
