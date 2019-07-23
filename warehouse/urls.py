from django.urls import path
from warehouse.views import *
from django.views.generic.base import TemplateView


urlpatterns = [
    # dashboard url's
    path('dashboard/warehouse/list/', TemplateView.as_view(template_name='warehouse_list.html'), name='warehouse_list'),

]
