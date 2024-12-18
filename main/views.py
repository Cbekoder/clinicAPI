from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from .models import Doctor, Turn, Service
from .serializers import DoctorSerializer, ServiceSerializer, TurnSerializer, TurnGetSerializer


class DoctorsListCreateAPIView(ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'room']


class ServiceListCreateAPIView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'room']


class TurnListCreateAPIView(ListCreateAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TurnGetSerializer
        return TurnSerializer