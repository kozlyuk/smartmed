from django.urls import path

from django.contrib.auth import views

from accounts.views import *

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='auth.html'), name='login'),
    path('logout/', views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('employee/list/', EmployeeList.as_view(), name='employee_list'),
    path('employee/create', EmployeeCreate.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDelete.as_view(), name='employee_delete'),
    path('employee/self_update/', EmployeeSelfUpdate.as_view(), name='employee_self_update'),

    path('partner/list/', PartnerList.as_view(), name='partner_list'),
    path('partner/create', PartnerCreate.as_view(), name='partner_create'),
    path('partner/update/<int:pk>/', PartnerUpdate.as_view(), name='partner_update'),
    path('partner/delete/<int:pk>/', PartnerDelete.as_view(), name='partner_delete'),
    path('partner/self_update/', PartnerSelfUpdate.as_view(), name='partner_self_update'),
]
