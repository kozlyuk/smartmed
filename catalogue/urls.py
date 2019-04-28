from django.urls import path
from catalogue.views import Home, ProductList, ProductCreate, ProductUpdate, ProductDelete
from django.views.generic.base import TemplateView


urlpatterns = [
    path('product/image/', TemplateView.as_view(template_name='image_form.html')),
    path('product/list/', ProductList.as_view(), name='product_list'),
    path('product/create', ProductCreate.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdate.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDelete.as_view(), name='product_delete'),

    path('', Home.as_view(), name='base'),
]
