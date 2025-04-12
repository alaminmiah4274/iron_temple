from rest_framework import serializers
from plans.models import Membership, Subscription, Payment, MembershipImage
from django.utils import timezone
from datetime import timedelta


""" MEMBERSHIP SERIALIZER """


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["id", "name", "price", "duration"]


class MembershipImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = MembershipImage
        fields = ["id", "image"]


""" MEMBERSHIP SERIALIZER """


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "membership",
            "start_date",
            "end_date",
            "status",
        ]


class UpdateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["status"]


class SubscribeMembershipSerializer(serializers.ModelSerializer):
    membership = MembershipSerializer(read_only=True)
    membership_id = serializers.PrimaryKeyRelatedField(
        queryset=Membership.objects.all(),
        source="membership",
        write_only=True,
    )

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "membership",
            "membership_id",
            "start_date",
            "end_date",
            "status",
        ]
        read_only_fields = ["user", "start_date", "end_date", "status"]

    # def validate(self, data):
    #     membership = data["membership"]
    #     user = self.context["user"]

    #     # to prevent subscribing same membership twice
    #     if Subscription.objects.filter(
    #         user=user,
    #         membership=membership,
    #         status="ACTIVE",
    #     ).exists():
    #         raise serializers.ValidationError(
    #             "You have already subscribed this membership"
    #         )

    #     return data

    def create(self, validated_data):
        membership = validated_data["membership"]
        user = self.context["user"]

        start_date = timezone.now().date()

        if membership.duration == "WEEKLY":
            end_date = start_date + timedelta(weeks=1)
        elif membership.duration == "MONTHLY":
            end_date = start_date + timedelta(days=30)
        else:
            end_date = start_date + timedelta(days=365)

        # to prevent subscribing same membership twice
        if Subscription.objects.filter(
            user=user,
            membership=membership,
            status="ACTIVE",
        ).exists():
            return "You have already subscribed this membership"

        subscription = Subscription.objects.create(
            user=user,
            membership=membership,
            start_date=start_date,
            end_date=end_date,
            status="ACTIVE",
        )

        return subscription


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "subscription", "amount", "payment_date", "status"]
        read_only_fields = ["id"]


class MakePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "subscription", "amount", "payment_date", "status"]
        read_only_fields = ["id", "user", "payment_date", "status"]
