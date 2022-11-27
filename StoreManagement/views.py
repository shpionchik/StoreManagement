from itertools import chain

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import requires_csrf_token, csrf_protect
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from . import settings
from .models import StoreStaff, ComponentInstance, ComponentShipment
from django.views.generic import TemplateView
import json
from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.viewsets import ModelViewSet
from .serializers import StaffSerializer, ComponentInstanceSerializer, AllListSerializer, ShippedListSerializer
from rest_framework.response import Response
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import ComponentTable
import requests
from django.contrib.auth.decorators import login_required
from .forms import ReceivedForm, ShippedForm
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from .forms import RegisterForm
#
# def auth(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('action_page.php/')
#         else:
#             messages.success(request, ('Error, try again'))
#             return redirect('login')
#     else:
#         return render(
#             request,
#             template_name='loginold.html',
#             context={}
#           )


def hello(request):
    return render(
        request=request,
        template_name='home.html',
        context={}
    )


#
# class StoreStaffView(View):
#     def get(self, *args, **kwargs):
#         staff = StoreStaff.objects.all()
#
#         date = []
#         for person in staff:
#             date.append({
#                 'name': person.first_name,
#                 'surname': person.last_name,
#                 'phone': str(person.phone)
#             })
#
#         return JsonResponse(date)

#
# class ComponentInstanceViewSet(ModelViewSet):
#     # permission_classes = (IsAuthenticated,)
#     queryset = ComponentInstance.objects.all()
#     serializer_class = ComponentInstanceSerializer


@login_required(login_url="/login")
def home(request):
    return render(request, 'home.html')


@login_required(login_url="/login")
def create_receiving(request):
    if request.method == 'POST':
        form = ReceivedForm(request.POST, request.FILES)
        if form.is_valid():
            received_item = form.save(commit=False)
            received_item.created_by = request.user
            received_item.updated_by = request.user
            received_item.save()
            return redirect('/home')
    else:
        form = ReceivedForm()

    return render(request, 'create_received_item.html', {'form': form})


@login_required(login_url="/login")
def create_shipping(request):
    if request.method == 'POST':
        form = ShippedForm(request.POST)
        if form.is_valid():
            shipped_item = form.save(commit=False)
            shipped_item.save()
            return redirect('/home')
    else:
        form = ShippedForm()

    return render(request, 'create_shipped_item.html', {'form': form})

#
# def home1(request):
#     response = requests.get('http://127.0.0.1:8000/components/').json()
#     return render(request, 'sv_us_list.html', {'response': response})


@method_decorator(login_required(login_url="/login"), name='dispatch')
class UsList(TemplateView):
    template_name = 'sv_us_list.html'

    def get_context_data(self, **kwargs):
        queryset = ComponentInstance.objects.filter(condition_received=1).filter(componentshipment__date_shipped=None)

        context = {
            'response': queryset
        }
        return context


# class USViewSet(ModelViewSet):
#     queryset = ComponentInstance.objects.all()
#     serializer_class = ComponentInstanceSerializer
#
#
# @login_required(login_url="/login")
# def us_list(request):
#     response = requests.get('http://127.0.0.1:8000/us/').json()
#     return render(request, 'try.html', {'response': response})


@method_decorator(login_required(login_url="/login"), name='dispatch')
class SvList(TemplateView):
    template_name = 'sv_us_list.html'

    def get_context_data(self, **kwargs):
        queryset = ComponentInstance.objects.exclude(condition_received=1).filter(componentshipment__date_shipped=None)
        context = {
            'response': queryset
        }
        return context


# class SVViewSet(ModelViewSet):
#     # permission_classes = (IsAuthenticated,)
#     queryset = ComponentInstance.objects.exclude(condition_received=1).filter(componentshipment__date_shipped=None)
#     serializer_class = ComponentInstanceSerializer
#
#
# @login_required(login_url="/login")
# def sv_list(request):
#     response = requests.get('https://nordicstore.herokuapp.com/sv/').json()
#     return render(request, 'sv_us_list.html', {'response': response})

@method_decorator(login_required(login_url="/login"), name='dispatch')
class ShippedList(TemplateView):
    template_name = 'shipped_list.html'

    def get_context_data(self, **kwargs):
        queryset = ComponentShipment.objects.all()
        context = {
            'response': queryset
        }
        return context

# class ShippedViewSet(ModelViewSet):
#     # permission_classes = (IsAuthenticated,)
#     queryset = ComponentShipment.objects.all()
#     serializer_class = ShippedListSerializer


# @login_required(login_url="/login")
# def shipped_list(request):
#     response = requests.get('https://nordicstore.herokuapp.com/shipped/').json()
#     return render(request, 'shipped_list.html', {'response': response})


# class ComponentsFullList(generics.RetrieveAPIView):
#     queryset = ComponentInstance.objects.all()
#     renderer_classes = [TemplateHTMLRenderer]
#
#
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return Response({'component':self.object}, template_name=ComponentsFullList)

# #
# class ComponentListView(SingleTableView):
#     permission_classes = (IsAuthenticated,)
#     model = ComponentInstance
#     table_class = ComponentTable
#     template_name = 'ComponentFullList.html'

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
def list_with_shipment(request):
    components_shipped = ComponentInstance.objects.values_list('component__description',
                                                               'component__part_number',
                                                               'serial_number',
                                                               'date_received',
                                                               'condition_received__condition',
                                                               'received_from', 'quantity',
                                                               'unit__quantity_type',
                                                               'certificate_number',
                                                               'shelf_life',
                                                               'componentshipment__date_shipped',
                                                               'componentshipment__shipped_condition__condition',
                                                               'componentshipment__shipped_to',
                                                               'componentshipment__invoice',
                                                               'componentshipment__scrapped_company__company',
                                                               'certificate',
                                                               'componentshipment__shipped_quantity')
    date = []
    for i in components_shipped:
        date.append({
            'description': i[0],
            'part_number': i[1],
            'serial_number': i[2],
            'date_received': i[3],
            'condition_received': i[4],
            'received_from': i[5],
            'quantity': i[6],
            'unit': i[7],
            'certificate_number': i[8],
            'shelf_life': i[9],
            'date_shipped': i[10],
            'shipped_condition': i[11],
            'shipped_to': i[12],
            'invoice': i[13],
            'scrapped_company': i[14],
            'certificate': i[15],
            'shipped_quantity': i[16]
        }
        )

    return render(
        request,
        template_name='fulltable.html',
        context={'ser': date}
    )
