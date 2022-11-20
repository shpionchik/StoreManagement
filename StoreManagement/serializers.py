from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from .models import StoreStaff, ComponentInstance, Component, Condition, ComponentShipment, Warehouse,\
    RepairCompany
from rest_framework.fields import SerializerMethodField




class StaffSerializer(ModelSerializer):
    class Meta:
        model = StoreStaff
        fields = "__all__"


class ComponentNestedSerialized(ModelSerializer):
    class Meta:
        model = Component
        fields = ['description', 'part_number']


class StaffReceivedNestedSerializer(ModelSerializer):
    class Meta:
        model = StoreStaff
        fields = ['first_name', 'last_name']


class StatusNestedSerializer(ModelSerializer):
    class Meta:
        model = Condition
        fields = ['condition']

class ComponentCardNestedSerializer(ModelSerializer):
    class Meta:
        model = ComponentShipment
        fields = '__all__'


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['name']




class ComponentInstanceSerializer(ModelSerializer):

    component = ComponentNestedSerialized()
    staff_received = StaffReceivedNestedSerializer()
    condition_received = StatusNestedSerializer()


    class Meta:
        model = ComponentInstance
        fields = '__all__'

class ComponentStatusSerializer(ModelSerializer):
    class Meta:
        model = ComponentShipment
        fields = '__all__'


class AllListSerializer(ModelSerializer):
    component = ComponentInstanceSerializer

    class Meta:
        model = ComponentShipment
        fields = '__all__'


class ComponentInstanceNestedSerializer(ModelSerializer):
    component = ComponentNestedSerialized()
    class Meta:
        model = ComponentInstance
        fields = ['component', 'serial_number']

class ScrappedCompanySerializer(ModelSerializer):
    class Meta:
        model = RepairCompany
        fields = ['company']


class ShippedListSerializer(ModelSerializer):
    shipped_component = ComponentInstanceNestedSerializer()
    staff_shipped = StaffReceivedNestedSerializer()
    shipped_condition = StatusNestedSerializer()
    scrapped_company = ScrappedCompanySerializer()

    class Meta:
        model = ComponentShipment
        fields = '__all__'

