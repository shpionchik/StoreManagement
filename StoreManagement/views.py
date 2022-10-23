from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import StoreStaff
import json

from rest_framework.viewsets import ModelViewSet
from .serializers import StaffSerializer


def hello(request):
    return HttpResponse("Hello Richardas")


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


class StoreStaffViewSet(ModelViewSet):
    queryset = StoreStaff.objects.filter(first_name='Dmytro')
    serializer_class = StaffSerializer
