from django.urls import path
from .views import (
    ReviewCreateView,
    ReviewListView,
    ReviewDeleteView,
    ReviewDetailView,
)

urlpatterns = [
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    
    path('reviews/list/', ReviewListView.as_view(), name='review-list'),
    
    path('reviews/<int:pk>/', ReviewDeleteView.as_view(), name='review-delete'),
    
    path('reviews/<int:pk>/detail/', ReviewDetailView.as_view(), name='review-detail'),
]