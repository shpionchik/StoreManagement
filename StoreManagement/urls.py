"""StoreManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from .views import hello, get_numbers, StoreStaffView, ComponentInstanceViewSet, ComponentListView, home, USViewSet, \
    us_list, sv_list, SVViewSet, ShippedViewSet, shipped_list, get_fulllist_with_shipment, auth

from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views
router = SimpleRouter()
router.register('components', ComponentInstanceViewSet)
router.register('action_page.php', USViewSet)
router.register('sv', SVViewSet)
router.register('shipped', ShippedViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello),
    path('api-token-auth/', views.obtain_auth_token),
    path('numbers/', get_numbers),
    path('staff/', StoreStaffView.as_view()),
    path('components1/', ComponentListView.as_view()),
    path('test', home),
    # path('action_page.php', get_numbers),
    path('us_components', us_list),
    path('nordicstore.herokuapp/sv_components', sv_list),
    path('shipped_components', shipped_list),
    path('try/', get_fulllist_with_shipment),

] + router.urls
