from reports.serializers import (
    MembershipReportSerializer,
    AttendanceReportSerializer,
    FeedbackReportSerializer,
    EmptySerializer,
)
from plans.models import Membership
from classes.models import Attendance
from reviews.models import Feedback
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.db.models import Count, Avg, Sum, Q, F
from rest_framework.response import Response

# Create your views here.


class ReportViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    http_method_names = ["get"]

    def get_queryset(self):
        if self.action == "MembershipReport":
            return Membership.objects.all()
        if self.action == "AttendanceReport":
            return Attendance.objects.all()
        if self.action == "FeedbackReport":
            return Feedback.objects.all()

    def get_serializer_class(self):
        if self.action == "MembershipReport":
            return MembershipReportSerializer
        if self.action == "AttendanceReport":
            return AttendanceReportSerializer
        if self.action == "FeedbackReport":
            return FeedbackReportSerializer
        return EmptySerializer

    @action(detail=False, methods=["get"])
    def MembershipReport(self, request):
        report_data = Membership.objects.values("duration").annotate(
            total_members=Count("subscriptions"),
            total_revenue=Sum("subscriptions__membership__price"),
        )
        serializer = MembershipReportSerializer(report_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def AttendanceReport(self, request):
        queryset = Attendance.objects.all()

        """ SHOWING PER CALSS ATTENDANCE REPORT """

        report_data = (
            queryset.values("date", "fitness_class__name")
            .annotate(
                present_count=Count("id", filter=Q(status="PRESENT")),
                absent_count=Count("id", filter=Q(status="ABSENT")),
                total=Count("id"),
            )
            .annotate(attendance_rate=(F("present_count") * 100.0) / F("total"))
            .order_by("-date")
        )

        serializer = AttendanceReportSerializer(report_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def FeedbackReport(self, request):
        report_data = (
            Feedback.objects.values("fitness_class__name")
            .annotate(
                average_ratings=Avg("ratings"),
                total_feedbacks=Count("id"),
                positive_feedbacks=Count("id", filter=Q(ratings__gte=4)),
                negative_feedbacks=Count("id", filter=Q(ratings__lte=2)),
            )
            .order_by("-average_ratings")
        )

        serializer = FeedbackReportSerializer(report_data, many=True)
        return Response(serializer.data)
