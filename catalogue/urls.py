from django.urls import path
from catalogue.views import *
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', ManagerHome.as_view(), name='manager_home'),

    path('product/image/', TemplateView.as_view(template_name='image_form.html')),
    path('product/list/', ProductList.as_view(), name='product_list'),
    path('product/create', ProductCreate.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdate.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDelete.as_view(), name='product_delete'),

    path('category/list/', CategoryList.as_view(), name='category_list'),
    path('category/create', CategoryCreate.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdate.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDelete.as_view(), name='category_delete'),

    path('group/list/', GroupList.as_view(), name='group_list'),
    path('group/create', GroupCreate.as_view(), name='group_create'),
    path('group/update/<int:pk>/', GroupUpdate.as_view(), name='group_update'),
    path('group/delete/<int:pk>/', GroupDelete.as_view(), name='group_delete'),

    path('brand/list/', BrandList.as_view(), name='brand_list'),
    path('brand/create', BrandCreate.as_view(), name='brand_create'),
    path('brand/update/<int:pk>/', BrandUpdate.as_view(), name='brand_update'),
    path('brand/delete/<int:pk>/', BrandDelete.as_view(), name='brand_delete'),

]
