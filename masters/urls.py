from django.urls import path
from .views import CreateMasterProfileView

urlpatterns = [
    path('create/', CreateMasterProfileView.as_view()),
]
