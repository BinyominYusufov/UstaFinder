from rest_framework import serializers
from .models import Review
from orders.models import Order


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'order',
            'client',
            'master',
            'rating',
            'comment',
            'created_at',
            'is_published'
        ]
        read_only_fields = ['id', 'client', 'master', 'created_at']

    def validate_order(self, value):
        user = self.context['request'].user
        
        if value.status != 'DONE':
            raise serializers.ValidationError("Отзыв можно оставить только к завершённому заказу")
            
        if value.client != user:
            raise serializers.ValidationError("Можно оставлять отзыв только к своим заказам")
            
        if hasattr(value, 'review'):
            raise serializers.ValidationError("На этот заказ уже оставлен отзыв")
            
        return value