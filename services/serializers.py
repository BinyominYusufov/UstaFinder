from rest_framework import serializers
from .models import Service
from masters.models import MasterProfile

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'master', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at', 'master']

    def create(self, validated_data):
        request = self.context.get('request')
        if not hasattr(request.user, 'masterprofile'):
            raise serializers.ValidationError("Only masters can create services.")
        master = request.user.masterprofile
        validated_data['master'] = master
        return super().create(validated_data)
