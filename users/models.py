from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"  # use email instead of username
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


"""
Users:
admin@admin.com: 1234
stiven lisa: Tiven@2024
de arms: Arms@2024

------> supabase:
admin@admin.com: 1234
staff:
chris hameswoth: Hris@2024 --> id: 2
chris evans: Vans@2024 ---> id: 3
user:
tom cruise: Ruise@2024 --> id: 4
de arms: Arms@2024 --> id: 5
gal gadot: Gadot@2024 ---> id: 6
van diesel: Iesel@2024 --> id: 7

uSer@2024
"""
