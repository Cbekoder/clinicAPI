from django.utils.dateparse import parse_date
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
    search_fields = ['doctor__first_name', 'doctor__last_name',
                     'doctor__room', 'service__name', 'service__room',
                     'first_name', 'last_name', 'turn_num']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Filter turns created on or after this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format="date"
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Filter turns created on or before this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format="date"
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by doctor(first_name, last_name, room), service(name, room), client(first_name, last_name), turn_num.",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TurnGetSerializer
        return TurnSerializer