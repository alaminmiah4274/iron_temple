from rest_framework import serializers
from classes.models import FitnessClass, Booking, Attendance, FitnessClassImage
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


""" FITNESS MODEL SERIALZIER """


class FitnessClassImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = FitnessClassImage
        fields = ["id", "image"]


class FitnessClassSerializer(serializers.ModelSerializer):
    images = FitnessClassImageSerializer(many=True, read_only=True)

    class Meta:
        model = FitnessClass
        fields = [
            "id",
            "name",
            "description",
            "instructor",
            "schedule",
            "duration",
            "capacity",
            "images",
        ]


""" BOOKING MODEL SERIALIZER """


# created to show user info in booking model
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "address", "phone_number"]


class BookedFitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ["id", "name"]


class BookingClassSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    fitness_class = BookedFitnessClassSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "fitness_class",
            "booking_date",
            "status",
        ]


class BookFitnessClassSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)
    fitness_class_id = serializers.PrimaryKeyRelatedField(
        queryset=FitnessClass.objects.all(),
        source="fitness_class",
        write_only=True,
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "fitness_class",
            "fitness_class_id",
            "booking_date",
            "status",
        ]
        read_only_fields = ["user", "fitness_class", "booking_date", "status"]

    def validate(self, data):
        """
        Validate the booking:
        - Class must be in the future
        - Class must have available capacity
        - User can't book same class twice
        """
        fitness_class = data["fitness_class"]
        booking_date = data.get("booking_date", timezone.now().date())
        user = self.context["user"]

        # Check if class is in the past
        if fitness_class.schedule < booking_date:
            raise serializers.ValidationError(
                "Cannot book a class that has already occurred."
            )

        # Check capacity
        current_bookings = Booking.objects.filter(
            fitness_class=fitness_class, status="BOOKED"
        ).count()
        if current_bookings >= fitness_class.capacity:
            raise serializers.ValidationError("This class is fully booked.")

        # Check for duplicate booking
        if Booking.objects.filter(
            user=user, fitness_class=fitness_class, status="BOOKED"
        ).exists():
            raise serializers.ValidationError("You have already booked this class.")

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        validated_data["status"] = "BOOKED"
        return super().create(validated_data)


class UpdateBookedFitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["status"]


""" ATTENDANCE MODEL SERIALZIER """


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "user", "fitness_class", "date", "status"]
