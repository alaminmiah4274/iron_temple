from rest_framework.viewsets import ModelViewSet
from plans.models import Membership, Subscription, Payment
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from plans.serializers import (
    MembershipSerializer,
    SubscriptionSerializer,
    SubscribeMembershipSerializer,
    UpdateSubscriptionSerializer,
    PaymentSerializer,
    MakePaymentSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from plans.permissions import IsOwner, IsStaffUser
from rest_framework import permissions, generics
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class MembershipViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class SubscriptionViewSet(ModelViewSet):
    http_method_names = ["post", "get", "delete", "patch"]

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {"user": self.request.user}

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
        if self.request.user.is_superuser:
            return SubscriptionSerializer
        if self.action == "update_status":
            return UpdateSubscriptionSerializer
        return SubscribeMembershipSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Subscription.objects.all()
        return Subscription.objects.filter(user=self.request.user)


class PaymentViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminOrReadOnly()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return PaymentSerializer
        return MakePaymentSerializer

    def get_queryset(self):
        if self.request.user.is_superuser and self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status": "Your paymant done"})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentReportViewSet(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Payment.objects.all()

    def list(self, request, *args, **kwrgs):
        # to get the queryset of this model viewset
        queryset = self.filter_queryset(self.get_queryset())

        report_data = {
            "total_payments": queryset.count(),
            "total_amount": sum([payment.amount for payment in queryset]),
            "completed_payments": queryset.filter(status="COMPLETED").count(),
            "pending_payments": queryset.filter(status="PENDING").count(),
            "failed_payments": queryset.filter(status="FAILED").count(),
            "payments": self.get_serializer(queryset, many=True).data,
        }

        return Response(report_data)
