from rest_framework.viewsets import ModelViewSet
from classes.models import FitnessClass, Booking, Attendance, FitnessClassImage
from classes.serializers import (
    FitnessClassSerializer,
    BookingClassSerializer,
    BookFitnessClassSerializer,
    UpdateBookedFitnessClassSerializer,
    AttendanceSerializer,
    FitnessClassImageSerializer,
)
from classes.permissions import AdminOrReadOnlyFitnessClass
from api.permissions import IsAdminOrReadOnly, IsAdminOrStaff
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.


class FitnessClassViewSet(ModelViewSet):
    """
    API endpoints for managing fitness class:
     - Allow authenticated Admin to manage all fitness classes
     - Allow authenticated Staff to create, update and delete fitness class
     - Allow authenticated Members to view fitness classes and info
    """

    queryset = FitnessClass.objects.prefetch_related("images").all()
    permission_classes = [AdminOrReadOnlyFitnessClass]
    serializer_class = FitnessClassSerializer


class FitenessClassImageViewSet(ModelViewSet):
    """
    API endpoints for managing this class:
     - Allow only admin to manage and add image for fitness classes
    """

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = FitnessClassImageSerializer

    def get_queryset(self):
        return FitnessClassImage.objects.filter(
            fitness_class_id=self.kwargs.get("fitness_class_pk")
        )

    def perform_create(self, serializer):
        serializer.save(fitness_class_id=self.kwargs.get("fitness_class_pk"))


class BookingViewSet(ModelViewSet):
    """
    API endpoints for managing bookings
     - Allow authenticated admin to manage all bookings
     - Allow authenticated members to book classes and view their
        booking history and update booking status
    """

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
        if self.request.user.is_staff:
            return Booking.objects.select_related("user", "fitness_class")
            .prefetch_related("fitness_class__image").all()
        return (
            Booking.objects.select_related("user", "fitness_class")
            .prefetch_related("fitness_class__image")
            .filter(user=self.request.user)
        )


class AttendanceViewSet(ModelViewSet):
    """
    API endpoints for managing Attendance
     - Allow authenticated admin to manage attendance
     - Allow authenticated staff to mark attendance for members in fitness classes
     - Allow authenticated members to view their attendance history
    """

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
