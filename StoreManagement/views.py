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
    response = requests.get('https://nordicstore.herokuapp.com/components/').json()
    return render(request, 'home.html', {'response': response})


class USViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = ComponentInstance.objects.filter(condition_received=1)
    serializer_class = ComponentInstanceSerializer


def us_list(request):
    response = requests.get('https://nordicstore.herokuapp.com/us/').json()
    return render(request, 'home.html', {'response': response})


class SVViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = ComponentInstance.objects.exclude(condition_received=1)
    serializer_class = ComponentInstanceSerializer


def sv_list(request):
    response = requests.get('https://nordicstore.herokuapp.com/sv/').json()
    return render(request, 'home.html', {'response': response})


class ShippedViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = ComponentShipment.objects.all()
    serializer_class = ShippedListSerializer


def shipped_list(request):
    response = requests.get('https://nordicstore.herokuapp.com/shipped/').json()
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
                                                                'component__part_number',
                                                               'serial_number',
                                                               'date_received',
                                                                'condition_received__condition',
                                                               'received_from', 'quantity',
                                                               'unit__quantity_type',
                                                            'componentshipment__date_shipped',
                                                               'componentshipment__shipped_condition__condition',
                                                               'componentshipment__shipped_to',
                                                           'componentshipment__invoice','componentshipment__scrapped_company__company')
    date = []
    for i in components_shipped:
        date.append({
            'description':i[0],
            'part_number':i[1],
            'serial_number':i[2],
            'date_received':i[3],
            'condition_received':i[4],
            'received_from':i[5],
            'quantity':i[6],
            'unit':i[7],
            'date_shipped':i[8],
            'shipped_condition':i[9],
            'shipped_to':i[10],
            'invoice':i[11],
            'scrapped_company':i[12]
        }
        )

    return render(
        request,
        template_name='fulltable.html',
        context={'ser':date}
    )
