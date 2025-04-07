from django.urls import path, include
from rest_framework_nested import routers
from classes.views import FitnessClassViewSet


router = routers.DefaultRouter()

router.register("fitness-classes", FitnessClassViewSet, basename="fitness-classes")


urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(router.urls)),
]

""" 
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDAzOTgwNywiaWF0IjoxNzQzOTUzNDA3LCJqdGkiOiI3ZWMxY2JhNjE5ZWM0NzQyOGUzNTRhMTc0YTBhMzkwYyIsInVzZXJfaWQiOjF9.Y3gNY58iw76KeQ3Tx_aI6Vx7AzB7mPShwh-DxaSmur0",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0ODE3NDA3LCJpYXQiOjE3NDM5NTM0MDcsImp0aSI6IjUyODVlOWZhMjg0YTQzMWE5NGE1OGU0MzBiOTEzNDY4IiwidXNlcl9pZCI6MX0.g1aCvIZMRE1v_PxJUNFPi8Ux8PR_ihaDdjzJth3w6qo"
}

"""
