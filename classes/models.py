from django.db import models
from django.conf import settings

# Create your models here.


class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="instructor"
    )
    schedule = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    capacity = models.PositiveIntegerField(help_text="Max number of participants")


class Booking(models.Model):
    STATUS_CHOICES = [
        ("BOOKED", "Booked"),
        ("CANCELLED", "Cancelled"),
        ("ATTENDED", "Attended"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    fitness_class = models.ForeignKey(
        FitnessClass, on_delete=models.CASCADE, related_name="bookings"
    )
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="BOOKED")


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance"
    )
    fitness_class = models.ForeignKey(
        FitnessClass, on_delete=models.CASCADE, related_name="attendance"
    )
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Present")
