#users/views

from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from masters.models import MasterProfile  
from masters.serializers import MasterProfileSerializer



User = get_user_model()


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []



class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'date_joined': user.date_joined.isoformat() if user.date_joined else None,
        }

        try:
            master_profile = MasterProfile.objects.get(user=user)
            profile_serializer = MasterProfileSerializer(master_profile)
            data['master_profile'] = profile_serializer.data
        except MasterProfile.DoesNotExist:
            data['is_master'] = False
            data['master_profile'] = None

        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"detail": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)