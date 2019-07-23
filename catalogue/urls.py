"""smartmed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from catalogue.views import ShopGroups, ShopHome
from catalogue.views import ProductList, ProductCreate, ProductUpdate, ProductDelete
from catalogue.views import CategoryList, CategoryCreate, CategoryUpdate, CategoryDelete
from catalogue.views import GroupList, GroupCreate, GroupUpdate, GroupDelete
from catalogue.views import BrandList, BrandCreate, BrandUpdate, BrandDelete

from django.views.generic import TemplateView                                                   ##delete after create view


urlpatterns = [

    # shop url's
    path('', ShopGroups.as_view(), name='shop_home'),
    path('product/list/', ShopHome.as_view(), name='shop_product_list'),

    # dashboard url's
    path('dashboard/product/list/', ProductList.as_view(), name='product_list'),
    path('dashboard/product/create', ProductCreate.as_view(), name='product_create'),
    path('dashboard/product/update/<int:pk>/', ProductUpdate.as_view(), name='product_update'),
    path('dashboard/product/delete/<int:pk>/', ProductDelete.as_view(), name='product_delete'),
    path('dashboard/product/attributes/', TemplateView.as_view(template_name="product_attributes.html")),  ##change after create view

    path('dashboard/category/list/', CategoryList.as_view(), name='category_list'),
    path('dashboard/category/create', CategoryCreate.as_view(), name='category_create'),
    path('dashboard/category/update/<int:pk>/', CategoryUpdate.as_view(), name='category_update'),
    path('dashboard/category/delete/<int:pk>/', CategoryDelete.as_view(), name='category_delete'),

    path('dashboard/group/list/', GroupList.as_view(), name='group_list'),
    path('dashboard/group/create', GroupCreate.as_view(), name='group_create'),
    path('dashboard/group/update/<int:pk>/', GroupUpdate.as_view(), name='group_update'),
    path('dashboard/group/delete/<int:pk>/', GroupDelete.as_view(), name='group_delete'),

    path('dashboard/brand/list/', BrandList.as_view(), name='brand_list'),
    path('dashboard/brand/create', BrandCreate.as_view(), name='brand_create'),
    path('dashboard/brand/update/<int:pk>/', BrandUpdate.as_view(), name='brand_update'),
    path('dashboard/brand/delete/<int:pk>/', BrandDelete.as_view(), name='brand_delete'),

]
