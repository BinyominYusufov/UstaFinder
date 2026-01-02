from django.db import models
from masters.models import MasterProfile


class Service(models.Model):
    master = models.ForeignKey(
        MasterProfile,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(default=60)

    def __str__(self):
        return self.name
