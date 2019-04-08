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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

from catalogue.views import HomeView, ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^django-webix/', include('django_webix.urls')),
    url(r'^', include('accounts.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^product/list$', ProductListView.as_view(), name='product_list'),
    url(r'^product/create$', ProductCreateView.as_view(), name='product_create'),
    url(r'^product/update/(?P<pk>\d+)$', ProductUpdateView.as_view(), name='product_update'),
    url(r'^product/delete/(?P<pk>\d+)$', ProductDeleteView.as_view(), name='product_delete'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
