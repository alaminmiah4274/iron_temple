from django.db import models
from django.conf import settings
from classes.models import FitnessClass
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)


# Create your models here.
class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedbacks"
    )
    fitness_class = models.ForeignKey(
        FitnessClass, on_delete=models.CASCADE, related_name="feedbacks"
    )
    ratings = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sent by {self.user.first_name} on {self.ratings}"
