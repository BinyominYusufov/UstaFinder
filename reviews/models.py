from django.db import models
from django.conf import settings
from orders.models import Order
from masters.models import MasterProfile

class Review(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name="Заказ"
    )
    
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        verbose_name="Клиент"
    )
    
    master = models.ForeignKey(
        MasterProfile,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        verbose_name="Мастер"
    )
    
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name="Оценка"
    )
    
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    is_published = models.BooleanField(
        default=True,
        verbose_name="Показывать публично"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['order'], name='unique_review_per_order')
        ]

    def __str__(self):
        return f"Отзыв {self.client} → {self.master} | {self.rating}★"

    def save(self, *args, **kwargs):
        # Автоматически заполняем поля, если они не указаны
        if not self.client:
            self.client = self.order.client
        if not self.master:
            self.master = self.order.master
        super().save(*args, **kwargs)