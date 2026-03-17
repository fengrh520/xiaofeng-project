# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromptViewSet, RegisterView

# 创建一个路由器，这是 DRF 提供的神器，自动帮我们生成所有增删改查的网址
router = DefaultRouter()
# 把我们之前写的 PromptViewSet 注册到 'prompts' 这个路径下
router.register(r'prompts', PromptViewSet, basename='prompt')

# 把生成的网址暴露出去
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]