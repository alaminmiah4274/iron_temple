from rest_framework import serializers
from reviews.models import Feedback
from classes.models import FitnessClass
from django.contrib.auth import get_user_model

User = get_user_model()


# for user field
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "address", "phone_number"]
        ref_name = "ReviewsSimpleUser"


# for fitness class field
class SimpleFitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = [
            "id",
            "name",
            "description",
            "schedule",
            "duration",
            "capacity",
        ]


class FeedbackSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    fitness_class = SimpleFitnessClassSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ["id", "user", "fitness_class", "ratings", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "fitness_class", "ratings", "comment"]


class UpdateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["ratings", "comment"]
