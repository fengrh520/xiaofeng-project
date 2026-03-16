# api/serializers.py
from rest_framework import serializers
from .models import Prompt

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt        # 告诉它要翻译哪个模型
        fields = '__all__'    # 告诉它要翻译所有字段
        read_only_fields = ['user'] # 用户字段由后端自动设置，前端无需传递