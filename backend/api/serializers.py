# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prompt

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt        # 告诉它要翻译哪个模型
        fields = '__all__'    # 告诉它要翻译所有字段
        read_only_fields = ['user'] # 用户字段由后端自动设置，前端无需传递