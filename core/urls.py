from django.contrib import admin
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from main.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Clinic Turn API",
      default_version='v1',
      description="API for Clinic Turn System",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="cbekoder@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('doctors/', DoctorsListCreateAPIView.as_view(), name='doctors'),
    path('services/', ServiceListCreateAPIView.as_view(), name='services'),
    path('turns/', TurnListCreateAPIView.as_view(), name='turns')
]
