from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class MasterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    description = models.TextField()
    rating = models.FloatField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
