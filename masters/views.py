from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MasterProfileSerializer
from .models import MasterProfile


class CreateMasterProfileView(CreateAPIView):
    serializer_class = MasterProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user.role = 'MASTER'
        user.save()

        serializer.save(user=user)
