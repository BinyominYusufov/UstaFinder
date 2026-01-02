from rest_framework import serializers
from django.db.models import Avg
from .models import MasterProfile
from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Review
        fields = ('id', 'client', 'rating', 'comment', 'created_at')

class MasterProfileSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    rating_display = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = MasterProfile
        fields = (
            'specialization',
            'experience',
            'description',
            'average_rating',
            'review_count',
            'rating_display',
            'reviews',
        )

    def get_average_rating(self, instance):
        published_reviews = instance.received_reviews.filter(is_published=True)
        avg = published_reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else 0.0

    def get_review_count(self, instance):
        return instance.received_reviews.filter(is_published=True).count()

    def get_rating_display(self, instance):
        count = instance.received_reviews.filter(is_published=True).count()
        avg = instance.received_reviews.filter(is_published=True).aggregate(avg=Avg('rating'))['avg']
        if count > 0 and avg:
            return f"{round(avg, 1)} ({count})"
        return "Нет отзывов"

    def get_reviews(self, instance):
        published_reviews = instance.received_reviews.filter(is_published=True)
        return ReviewSerializer(published_reviews, many=True).data
