from rest_framework.serializers import ModelSerializer
from .models import Doctor, Service, Turn


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class TurnSerializer(ModelSerializer):
    class Meta:
        model = Turn
        fields = "__all__"
        read_only_fields = ["turn_num", "created_at"]

class TurnGetSerializer(ModelSerializer):
    doctor = DoctorSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Turn
        fields = "__all__"
        read_only_fields = ["turn_num", "created_at"]