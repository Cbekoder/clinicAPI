from datetime import date

from django.db import models, transaction
from rest_framework.exceptions import ValidationError


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    major = models.CharField(max_length=200)
    room = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Shifokor"
        verbose_name_plural = "Shifokorlar"
        ordering = ['-id']

    def __str__(self):
        return self.first_name + self.last_name


class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    room = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ['-id']

    def __str__(self):
        return self.name


class Turn(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    turn_num = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Navbat"
        verbose_name_plural = "Navbatlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name + self.last_name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            today = date.today()
            if self.doctor:
                self.service = None
                room = self.doctor.room
                last_turn = Turn.objects.filter(
                    doctor__room=room,
                    created_at__date=today
                ).order_by('-turn_num').first()
            elif self.service:
                self.doctor = None
                room = self.service.room
                last_turn = Turn.objects.filter(
                    service__room=room,
                    created_at__date=today
                ).order_by('-turn_num').first()
            else:
                raise ValidationError({"error": "Service or Doctor is required."})

            self.turn_num = last_turn.turn_num + 1 if last_turn else 1

            super().save(*args, **kwargs)


