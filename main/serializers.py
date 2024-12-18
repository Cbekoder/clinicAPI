from rest_framework.serializers import DateTimeField
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
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Turn
        fields = "__all__"
        read_only_fields = ["turn_num", "created_at"]

class TurnGetSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    doctor = DoctorSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Turn
        fields = "__all__"
        read_only_fields = ["turn_num", "created_at"]