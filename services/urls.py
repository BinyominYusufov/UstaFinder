from django.urls import path
from .views import (
    ServiceListView,
    ServiceCreateView,
    ServiceRetrieveView,
    ServiceUpdateView,
    ServiceDestroyView
)

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/create/', ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/', ServiceRetrieveView.as_view(), name='service-retrieve'),
    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete/', ServiceDestroyView.as_view(), name='service-destroy'),
]

