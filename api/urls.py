from django.urls import path, include
from rest_framework_nested import routers
from classes.views import (
    FitnessClassViewSet,
    BookingViewSet,
    AttendanceViewSet,
)
from plans.views import (
    MembershipViewSet,
    SubscriptionViewSet,
    PaymentViewSet,
    PaymentReportViewSet,
)
from reviews.views import FeedbackViewSet
from reports.views import ReportViewSet


router = routers.DefaultRouter()

router.register("fitness-classes", FitnessClassViewSet, basename="fitness-classes")
router.register("memberships", MembershipViewSet, basename="memberships")
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions")
router.register("bookings", BookingViewSet, basename="bookings")
router.register("attendance", AttendanceViewSet, basename="attendance")
router.register("payments", PaymentViewSet, basename="payments")
router.register("payment-reports", PaymentReportViewSet, basename="payment-reports")
router.register("feedback", FeedbackViewSet, basename="feedback")
router.register("reports", ReportViewSet, basename="reports")


urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(router.urls)),
]
