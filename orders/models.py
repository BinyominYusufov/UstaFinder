# models.py
from django.conf import settings
from django.db import models
from django.utils import timezone
from masters.models import MasterProfile
from services.models import Service

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('ACCEPTED', 'Accepted'),
        ('DONE', 'Done'),
        ('CANCELLED', 'Cancelled'),
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    master = models.ForeignKey(
        MasterProfile,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    booking_date = models.DateTimeField()        
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='NEW'
    )
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        default=None
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        default=None
    )

    def save(self, *args, **kwargs):
        if self.booking_date and self.service:
            self.start_time = self.booking_date
            self.end_time = self.booking_date + timezone.timedelta(
                minutes=self.service.duration
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.master} - {self.booking_date}"