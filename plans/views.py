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
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.decorators import api_view
from decouple import config
from django.conf import settings as main_settings
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework import status

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
     - Allow authenticated Members to create, view and update their own subscriptions
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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

        if getattr(self, "swagger_fake_view", False):
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


""" SSL COMMERZ """


@api_view(["POST"])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")
    subscription_id = request.data.get("subscriptionId")
    
    settings = {
        "store_id": config("store_id"),
        "store_pass": config("store_pass"),
        "issandbox": True,
    }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body["total_amount"] = amount
    post_body["currency"] = "BDT"
    post_body["tran_id"] = f"txn_{subscription_id}"
    post_body["success_url"] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body["fail_url"] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body["cancel_url"] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body["emi_option"] = 0
    post_body["cus_name"] = f"{user.first_name} {user.last_name}"
    post_body["cus_email"] = user.email
    post_body["cus_phone"] = user.phone_number
    post_body["cus_add1"] = user.address
    post_body["cus_city"] = "Dhaka"
    post_body["cus_country"] = "Bangladesh"
    post_body["shipping_method"] = "NO"
    post_body["multi_card_name"] = ""
    post_body["num_of_item"] = 1
    post_body["product_name"] = "Gym Memberships"
    post_body["product_category"] = "general"
    post_body["product_profile"] = "general"

    response = sslcz.createSession(post_body)  # API response

    # Need to redirect user to response['GatewayPageURL']

    if response.get("status") == "SUCCESS":
        return Response({"payment_url": response["GatewayPageURL"]})

    return Response(
        {"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
def payment_success(request):
    sub_id = request.data.get("tran_id").split("_")[1]
    subscription = Subscription.objects.get(id=sub_id)
    subscription.status = "PAID"
    subscription.save()
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/makePayment")


@api_view(["POST"])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/makePayment")


@api_view(["POST"])
def payment_fail(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/makePayment")


class HasSubscribedMembership(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, membership_id):
        user = request.user
        has_subscribed = Subscription.objects.filter(
            user=user, membership_id=membership_id
        ).exists()

        return Response({"hasSubscribed": has_subscribed})


""" 
way of computing sum:
from django.db.models import Sum

total_amount = queryset.aggregate(Sum("amount"))["amount__sum"] or 0
"""
