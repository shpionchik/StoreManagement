from rest_framework.serializers import ModelSerializer
from .models import StoreStaff


class StaffSerializer(ModelSerializer):
    class Meta:
        model = StoreStaff
        fields = "__all__"
