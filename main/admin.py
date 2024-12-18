from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Doctor, Service, Turn


admin.site.unregister(Group)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'major', 'room')
    search_fields = ('first_name', 'last_name', 'major')
    list_filter = ('major',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'room')
    search_fields = ('name',)
    list_filter = ('room',)


@admin.register(Turn)
class TurnAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'service', 'doctor', 'price', 'turn_num', 'created_at')
    search_fields = ('first_name', 'last_name', 'service__name', 'doctor__first_name', 'doctor__last_name')
    list_filter = ('service', 'doctor', 'created_at')
    ordering = ('-created_at',)
