import django_tables2 as tables
from .models import ComponentInstance, Component
from rest_framework.serializers import ModelSerializer

class ComponentTable(tables.Table):

    class Meta:
        model = ComponentInstance
        template_name = "django_tables2/bootstrap.html"
        fields = ('component', 'serial_number', 'quantity', 'received_from', 'date_received', 'condition_received')