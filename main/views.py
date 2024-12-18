from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

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



class ReportView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date for the report (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format="date"),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date for the report (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format="date"),
            openapi.Parameter('doctor', openapi.IN_QUERY, description="Doctor ID to filter by",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('service', openapi.IN_QUERY, description="Service ID to filter by",
                              type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', str(date.today()))
        end_date = request.query_params.get('end_date', str(date.today()))

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if not start_date or not end_date:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        turns = Turn.objects.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

        doctor_id = request.query_params.get('doctor')
        service_id = request.query_params.get('service')

        if doctor_id:
            turns = turns.filter(doctor_id=doctor_id)

        if service_id:
            turns = turns.filter(service_id=service_id)

        total_sum = turns.aggregate(total_price=Sum('price'))['total_price']

        doctors = Doctor.objects.all()
        services = Service.objects.all()

        doctor_report = []
        for doctor in doctors:
            total_price = Turn.objects.filter(doctor=doctor).aggregate(total_price=Sum('price'))[
                              'total_price'] or 0
            doctor_data = DoctorSerializer(doctor).data
            if total_price > 0:
                doctor_report.append({
                    "doctor": doctor_data,
                    "total_price": total_price
                })

        service_report = []
        for service in services:
            total_price = Turn.objects.filter(service=service).aggregate(total_price=Sum('price'))[
                              'total_price'] or 0
            service_data = ServiceSerializer(service).data
            if total_price > 0:
                service_report.append({
                    "service": service_data,
                    "total_price": total_price
                })

        return Response({
            # "total_price": total_sum,
            "start_date": start_date,
            "end_date": end_date,
            "doctor_report": doctor_report,
            "service_report": service_report
        })
