from django.contrib import admin
from classes.models import FitnessClass, FitnessClassImage, Booking, Attendance


# Register your models here.
@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ["name", "instructor", "capacity"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["user", "fitness_class", "status"]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["user", "fitness_class", "status"]


admin.site.register(FitnessClassImage)
