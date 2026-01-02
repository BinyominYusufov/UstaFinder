from rest_framework import serializers
from django.db.models import Q
from django.utils import timezone
from .models import Order, Service, MasterProfile

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client','master', 'service', 'booking_date', 'status']
        read_only_fields = ['id', 'client','master','status']

    def validate(self, data):
        service = data['service']
        booking_date = data['booking_date']

        # Проверка, что у услуги есть длительность
        duration_minutes = service.duration
        if not duration_minutes:
            raise serializers.ValidationError("The service does not specify duration.")

        start_time = booking_date
        end_time = start_time + timezone.timedelta(minutes=duration_minutes)

        # Найти свободного мастера для выбранного времени
        available_masters = MasterProfile.objects.filter(services=service)
        free_master = None

        for master in available_masters:
            conflicting_orders = Order.objects.filter(
                master=master,
                status__in=['NEW', 'ACCEPTED']
            ).filter(
                Q(booking_date__lt=end_time, booking_date__gte=start_time) |
                Q(booking_date__lte=start_time, end_time__gt=start_time)
            )

            if self.instance:
                conflicting_orders = conflicting_orders.exclude(pk=self.instance.pk)

            if not conflicting_orders.exists():
                free_master = master
                break

        if not free_master:
            raise serializers.ValidationError(
                "No available master for the selected service at this time."
            )

        # Сохраняем выбранного мастера в data
        data['master'] = free_master
        return data

    def create(self, validated_data):
        # client берем из запроса
        user = self.context['request'].user
        validated_data['client'] = user
        return super().create(validated_data)
