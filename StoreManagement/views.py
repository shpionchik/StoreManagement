from itertools import chain

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


def hello(request):
    return render(
        request=request,
        template_name='base_generic.html',
        context={}
    )


def get_numbers(request):
    values = []
    for value in range(20):
        values.append(
            {
                'value': value,
                'square': value ** 2

            }
        )

    return render(
        request=request,
        template_name='numbers.html',
        context={
            'values_list': values
        }
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


#
# class StoreStaffViewSet(ModelViewSet):
#     queryset = StoreStaff.objects.filter(first_name='Dmytro')
#     serializer_class = StaffSerializer


class ComponentInstanceViewSet(ModelViewSet):
    queryset = ComponentInstance.objects.all()
    serializer_class = ComponentInstanceSerializer


def home(request):
    response = requests.get('http://127.0.0.1:8000/components/').json()
    return render(request, 'home.html', {'response': response})


class USViewSet(ModelViewSet):
    queryset = ComponentInstance.objects.exclude(condition_received=1)
    serializer_class = ComponentInstanceSerializer


def us_list(request):
    response = requests.get('http://127.0.0.1:8000/us/').json()
    return render(request, 'home.html', {'response': response})


class SVViewSet(ModelViewSet):
    queryset = ComponentInstance.objects.exclude(condition_received=2)
    serializer_class = ComponentInstanceSerializer


def sv_list(request):
    response = requests.get('http://127.0.0.1:8000/sv/').json()
    return render(request, 'home.html', {'response': response})


class ShippedViewSet(ModelViewSet):
    queryset = ComponentShipment.objects.all()
    serializer_class = ShippedListSerializer


def shipped_list(request):
    response = requests.get('http://127.0.0.1:8000/shipped/').json()
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
    model = ComponentInstance
    table_class = ComponentTable
    template_name = 'ComponentFullList.html'


def get_fulllist_with_shipment(request):
    """ Get full list list of components joined with shipping table

                Example:

                [
                    {
                        Components object


                    }
                ]

        """

    components_received = ComponentInstance.objects.all()
    components_shipped = ComponentShipment.objects.all()
    result = []
    for component_received in components_received:
        component_received_dict = {}

        component_received_dict['id'] = component_received.id
        component_received_dict['component'] = {}
        component_received_dict['component']['description'] = component_received.component.description
        component_received_dict['component']['part_number'] = component_received.component.part_number
        component_received_dict['serial_number'] = component_received.serial_number
        component_received_dict['condition_received'] = component_received.condition_received
        component_received_dict['date_received'] = component_received.date_received
        component_received_dict['received_from'] = component_received.received_from
        component_received_dict['quantity'] = component_received.quantity
        component_received_dict['unit'] = component_received.unit
        component_received_dict['shipped'] = {}
        for component_shipped in components_shipped:
            if component_shipped.component == component_received_dict['component']:
                component_received_dict['shipped']['date_shipped'] = component_shipped.date_shipped
        result.append(component_received_dict)
    return HttpResponse(result)
    #     render(
    #     request,
    #     'fulllist.html',
    #     context={
    #         'components': result
    #     }
    # )
