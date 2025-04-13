from django.contrib import admin
from plans.models import Membership, Subscription, Payment, MembershipImage


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status"]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "duration"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "membership", "status"]


admin.site.register(MembershipImage)
