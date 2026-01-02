from rest_framework import serializers
from django.db.models import Q
from django.utils import timezone
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client', 'master', 'service', 'booking_date', 'status']
        read_only_fields = ['id', 'client', 'status']

    def validate(self, data):
        master = data['master']
        booking_date = data['booking_date']
        service = data['service']

        duration_minutes = service.duration  
        if not duration_minutes:
            raise serializers.ValidationError("The services do not specify duration.")

        start_time = booking_date
        end_time = start_time + timezone.timedelta(minutes=duration_minutes)

        conflicting_orders = Order.objects.filter(
            master=master,
            status__in=['NEW', 'ACCEPTED']
        ).filter(
            Q(booking_date__lt=end_time, booking_date__gte=start_time) |
            Q(booking_date__lte=start_time, end_time__gt=start_time)
        )

        if self.instance:
            conflicting_orders = conflicting_orders.exclude(pk=self.instance.pk)

        if conflicting_orders.exists():
            raise serializers.ValidationError(
                f"The technician is already busy at the specified time.({start_time} — {end_time})"
            )

        return data