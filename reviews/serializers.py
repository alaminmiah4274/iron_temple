from rest_framework import serializers
from reviews.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "user", "fitness_class", "ratings", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class UpdateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["ratings", "comment"]
