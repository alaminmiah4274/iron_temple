from rest_framework.viewsets import ModelViewSet
from plans.models import Membership, Subscription, Payment, MembershipImage
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly, IsAdminOrStaff
from plans.serializers import (
    MembershipSerializer,
    SubscriptionSerializer,
    SubscribeMembershipSerializer,
    UpdateSubscriptionSerializer,
    PaymentSerializer,
    MakePaymentSerializer,
    MembershipImageSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Q
from rest_framework.filters import SearchFilter

# Create your views here.


class MembershipViewSet(ModelViewSet):
    """
    API endpoints for managing membership
     - Allow authenticated Admin to manage all membership plans
     - Allow authenticated Staff to create, update and delete membership plans
     - Allow authenticated Members to view memberships
    """
    
    filter_backends = [SearchFilter]
    search_fields = ["name", "price", "duration"]

    permission_classes = [IsAdminOrReadOnly]
    queryset = Membership.objects.prefetch_related("images").all()
    serializer_class = MembershipSerializer


class MembershipImageViewSet(ModelViewSet):
    """
    API endpoints for managing Membership Image
     - Allow authenticated admin to manage all
    """

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MembershipImageSerializer

    def get_queryset(self):
        return MembershipImage.objects.filter(
            membership_id=self.kwargs.get("membership_pk")
        )

    def perform_create(self, serializer):
        serializer.save(membership_id=self.kwargs.get("membership_pk"))


class SubscriptionViewSet(ModelViewSet):
    """
    API endpoints for managing subsciptions
     - Allow authenticated Admin to manage all subscriptions
     - Allow authenticated Staff to view and delete only cancelled and expired
        subscriptions of the members
     - Allow authenticated Members to view and update their own subscriptions
    """
    filter_backends = [SearchFilter]
    search_fields = ["user__email", "membership__name", "status"]
    http_method_names = ["post", "get", "delete", "patch"]

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsAdminOrStaff()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        subscription = self.get_object()
        serializer = UpdateSubscriptionSerializer(
            subscription, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"status": f"Subscription status updated to {request.data['status']}"}
        )

    def get_serializer_class(self):
        if getattr(self, "swagger_fake_view", False):
            return SubscribeMembershipSerializer
        
        user = self.request.user

        if user.is_superuser:
            return SubscriptionSerializer
        if self.action == "update_status":
            return UpdateSubscriptionSerializer
        return SubscribeMembershipSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # Return empty queryset during schema generation
            return Subscription.objects.none()

        user = self.request.user

        if user.is_superuser:
            return (
                Subscription.objects.select_related("user", "membership")
                .prefetch_related("membership__images")
                .all()
            )
        if user.is_staff:
            return Subscription.objects.select_related("user", "membership").filter(
                Q(status="CANCELLED") | Q(status="EXPIRED")
            )
        return (
            Subscription.objects.select_related("membership")
            .prefetch_related("membership__images")
            .filter(user=user)
        )


class PaymentViewSet(ModelViewSet):
    """
    API endpoints for managing Payment
     - Allow authenticated Admin to manage all payments
     - Allow authenticated Staff to view payments
     - Allow authenticated Members to make payments for their subscriptions
    """

    filter_backends = [SearchFilter]
    search_fields = ["user__email", "amount", "status"]

    def get_permissions(self):
        user = self.request.user

        if user.is_staff:
            return [IsAdminOrReadOnly()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        user = self.request.user

        if user.is_superuser:
            return PaymentSerializer
        return MakePaymentSerializer

    def get_queryset(self):
        user = self.request.user

        if getattr(self, 'swagger_fake_view', False):
            # Return empty queryset during schema generation
            return Payment.objects.none()

        if user.is_superuser and user.is_staff:
            return Payment.objects.select_related("user", "subscription").all()
        return Payment.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status": "Your paymant done"})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentReportViewSet(ModelViewSet):
    """
    API endpoints for managing Payment Report
     - Allow authenticated Admin to generate and manage payment reports
    """

    http_method_names = ["get"]
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Payment.objects.all()

    def list(self, request, *args, **kwrgs):
        # to get the queryset of this model viewset
        queryset = self.filter_queryset(self.get_queryset())

        status_counts = queryset.aggregate(
            total_payments=Count("id"),
            completed_payments=Count("id", filter=Q(status="COMPLETED")),
            pending_payments=Count("id", filter=Q(status="PENDING")),
            failed_payments=Count("id", filter=Q(status="FAILED")),
        )

        total_amount = sum([payment.amount for payment in queryset])

        report_data = {
            "total_payments": status_counts["total_payments"],
            "total_amount": total_amount,
            "completed_payments": status_counts["completed_payments"],
            "pending_payments": status_counts["pending_payments"],
            "failed_payments": status_counts["failed_payments"],
            "payments": self.get_serializer(queryset, many=True).data,
        }

        return Response(report_data)


""" 
way of computing sum:
from django.db.models import Sum

total_amount = queryset.aggregate(Sum("amount"))["amount__sum"] or 0
"""
