from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address_line = models.TextField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.city}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username