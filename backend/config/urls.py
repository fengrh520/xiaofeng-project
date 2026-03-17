# config/urls.py
from django.contrib import admin
from django.urls import path, include  # 引入 include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 这是我们刚才进的后台网址
    path("admin/", admin.site.urls),
    
    # 我们把 api 模块的所有网址，都挂在 /api/ 下面
    # 比如前端想获取提示词，访问的就是 /api/prompts/
    path("api/", include("api.urls")),
    
    # 认证接口 (由于前端代码向 /api/token/ 发请求，这里保持不变)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # 登录拿 Token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 刷新 Token
]


