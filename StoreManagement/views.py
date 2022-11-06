from itertools import chain
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import StoreStaff, ComponentInstance, ComponentShipment
import json
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.viewsets import ModelViewSet
from .serializers import StaffSerializer, ComponentInstanceSerializer, AllListSerializer, ShippedListSerializer
from rest_framework.response import Response
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import ComponentTable
import requests
from django.views.decorators.csrf import requires_csrf_token

def auth(request):
    return render(
        request,
        template_name='auth.html',
        context={}
    )


def hello(request):
    return render(
        request=request,
        template_name='base_generic.html',
        context={}
    )




class StoreStaffView(View):
    def get(self, *args, **kwargs):
        staff = StoreStaff.objects.all()

        date = []
        for person in staff:
            date.append({
                'name': person.first_name,
                'surname': person.last_name,
                'phone': str(person.phone)
            })

        return JsonResponse(date)


class ComponentInstanceViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = ComponentInstance.objects.all()
    serializer_class = ComponentInstanceSerializer


def home(request):
    response = requests.get('/components/').json()
    return render(request, 'home.html', {'response': response})


class USViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = ComponentInstance.objects.exclude(condition_received=1)
    serializer_class = ComponentInstanceSerializer


def us_list(request):
    response = requests.get('/us/').json()
    return render(request, 'home.html', {'response': response})


class SVViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = ComponentInstance.objects.exclude(condition_received=2)
    serializer_class = ComponentInstanceSerializer


def sv_list(request):
    response = requests.get('/sv/').json()
    return render(request, 'home.html', {'response': response})


class ShippedViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = ComponentShipment.objects.all()
    serializer_class = ShippedListSerializer


def shipped_list(request):
    response = requests.get('/shipped/').json()
    return render(request, 'shipped_list.html', {'response': response})


# class ComponentsFullList(generics.RetrieveAPIView):
#     queryset = ComponentInstance.objects.all()
#     renderer_classes = [TemplateHTMLRenderer]
#
#
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return Response({'component':self.object}, template_name=ComponentsFullList)


class ComponentListView(SingleTableView):
    # permission_classes = (IsAuthenticated,)
    model = ComponentInstance
    table_class = ComponentTable
    template_name = 'ComponentFullList.html'



def list_with_shipment(request):
    components_shipped = ComponentInstance.objects.values_list('component__description',
                                                               'serial_number', 'date_received',
                                                               'componentshipment__date_shipped',
                                                               'componentshipment__shipped_condition')
    return HttpResponse(components_shipped)

