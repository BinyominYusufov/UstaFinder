from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            password=validated_data['password'],
            role='USER'
        )
        return user
    
    
    # Проверка номера телефона
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Номер телефона должен содержать только цифры.")
        if len(value) != 9:
            raise serializers.ValidationError("Номер телефона должен быть длиной 9 цифр.")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером уже существует.")
        return value

    # Создание пользователя
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user


