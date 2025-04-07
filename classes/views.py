from rest_framework.viewsets import ModelViewSet
from classes.models import FitnessClass
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from classes.serializers import FitnessClassSerializer

# Create your views here.


class FitnessClassViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer
