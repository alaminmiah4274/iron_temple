from django.urls import path, include
from rest_framework_nested import routers
from classes.views import (
    FitnessClassViewSet,
    BookingViewSet,
    AttendanceViewSet,
    FitenessClassImageViewSet,
)
from plans.views import (
    MembershipViewSet,
    SubscriptionViewSet,
    PaymentViewSet,
    PaymentReportViewSet,
    MembershipImageViewSet,
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

membership_router = routers.NestedDefaultRouter(
    router, "memberships", lookup="membership"
)
membership_router.register(
    "images", MembershipImageViewSet, basename="membership-images"
)
fitness_class_router = routers.NestedDefaultRouter(
    router, "fitness-classes", lookup="fitness_class"
)
fitness_class_router.register(
    "images", FitenessClassImageViewSet, basename="fitness-class-images"
)


urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(router.urls)),
    path("", include(membership_router.urls)),
    path("", include(fitness_class_router.urls)),
]
