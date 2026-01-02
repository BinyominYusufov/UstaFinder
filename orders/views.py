from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class IsClientOrMaster(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.client == request.user or obj.master.user == request.user

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrMaster]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
