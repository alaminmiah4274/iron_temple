from rest_framework import serializers
from classes.models import FitnessClass


class FitnessClassSerializer(serializers.ModelSerializer):
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
        ]
