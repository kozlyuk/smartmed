from django.urls import path
from catalogue.views import ProductList   #, ProductCreate, ProductUpdate, ProductDelete


urlpatterns = [
    path('product/list/', ProductList.as_view(), name='product_list'),
    #path(r'^product/create$', ProductCreateView.as_view(), name='product_create'),
    #path(r'^product/update/(?P<pk>\d+)$', ProductUpdateView.as_view(), name='product_update'),
    #path(r'^product/delete/(?P<pk>\d+)$', ProductDeleteView.as_view(), name='product_delete'),
]