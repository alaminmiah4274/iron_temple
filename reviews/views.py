from reviews.serializers import FeedbackSerializer, UpdateFeedbackSerializer
from rest_framework.viewsets import ModelViewSet
from reviews.models import Feedback
from rest_framework.response import Response
from reviews.permissions import IsReadOnly, IsWriteOnly
from rest_framework.decorators import action

# Create your views here.


class FeedbackViewSet(ModelViewSet):
    """
    API endpoints for managing feedback
     - Allow authenticated admin to view all feedbacks
     - Allow authenticated staff to view feedbacks for their classes
     - Allow authenticated members to create, update and delete their feedbacks
    """

    serializer_class = FeedbackSerializer
    http_method_names = ["post", "get", "delete", "patch"]

    def get_permissions(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return [IsReadOnly()]
        return [IsWriteOnly()]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Feedback.objects.all()
        if self.request.user.is_staff:
            return Feedback.objects.filter(fitness_class__instructor=self.request.user)
        return Feedback.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status": "Your feedback has been created"})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def update_review(self, request, pk=None):
        review = self.get_object()
        serializer = UpdateFeedbackSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "Your review has been updated"})

    def get_serializer_class(self):
        if self.action == "update_review":
            return UpdateFeedbackSerializer
        return FeedbackSerializer
