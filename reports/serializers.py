from rest_framework import serializers


class MembershipReportSerializer(serializers.Serializer):
    membership_type = serializers.CharField(source="duration")
    total_members = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)


class AttendanceReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    class_name = serializers.CharField(source="fitness_class__name")
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    attendance_rate = serializers.FloatField()


class FeedbackReportSerializer(serializers.Serializer):
    fitness_class = serializers.CharField(source="fitness_class__name")
    average_ratings = serializers.FloatField()
    total_feedbacks = serializers.IntegerField()
    positive_feedbacks = serializers.IntegerField()
    negative_feedbacks = serializers.IntegerField()


class EmptySerializer(serializers.Serializer):
    pass
