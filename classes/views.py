from rest_framework.viewsets import ModelViewSet
from classes.models import FitnessClass, Booking, Attendance
from classes.serializers import (
    FitnessClassSerializer,
    BookingClassSerializer,
    BookFitnessClassSerializer,
    UpdateBookedFitnessClassSerializer,
    AttendanceSerializer,
)
from classes.permissions import AdminOrReadOnlyFitnessClass
from api.permissions import IsAdminOrReadOnly, IsAdminOrStaff
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.


class FitnessClassViewSet(ModelViewSet):
    queryset = FitnessClass.objects.all()
    permission_classes = [AdminOrReadOnlyFitnessClass]
    serializer_class = FitnessClassSerializer


class BookingViewSet(ModelViewSet):
    http_method_names = ["post", "get", "delete", "patch"]

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {"user": self.request.user}

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        booked_class = self.get_object()
        serializer = UpdateBookedFitnessClassSerializer(
            booked_class, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"status": f"Booking status updated to {request.data['status']}"}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status": "Your class booked successfuly."})

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return BookingClassSerializer
        if self.action == "update_status":
            return UpdateBookedFitnessClassSerializer
        return BookFitnessClassSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)


class AttendanceViewSet(ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrStaff()]
        if self.request.method == "DELETE":
            return [IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Attendance.objects.all()
        return Attendance.objects.filter(user=self.request.user)
