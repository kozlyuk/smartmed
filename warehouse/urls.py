from django.urls import path
from warehouse.views import *
from django.views.generic.base import TemplateView


urlpatterns = [
    path('warehouse/list/', TemplateView.as_view(template_name='warehouse_list.html'), name='warehouse_list'),

]
