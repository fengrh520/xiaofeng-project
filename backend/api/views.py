import os
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from openai import OpenAI
from dotenv import load_dotenv
from .models import Prompt
from .serializers import PromptSerializer, RegisterSerializer

# 加载 .env 里的 Key
load_dotenv()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all() # 用于生成路由名称，实际查询会被 get_queryset 覆盖
    serializer_class = PromptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # 搜索和筛选配置
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_starred', 'is_pinned'] # 支持按星标/置顶筛选
    search_fields = ['title', 'original_prompt', 'optimized_prompt'] # 支持搜索这些字段
    ordering_fields = ['created_at', 'updated_at'] # 支持排序
    ordering = ['-is_pinned', '-created_at'] # 默认排序：置顶优先，然后按时间倒序

    # 只返回当前登录用户的数据
    def get_queryset(self):
        # 基础查询：只看当前用户的
        queryset = Prompt.objects.filter(user=self.request.user)
        
        # 修复：手动处理搜索逻辑，确保中文搜索正常工作
        # 这里的 'search' 对应前端传来的 ?search=xxx 参数
        search_query = self.request.query_params.get('search', None)
        if search_query:
            from django.db.models import Q
            # 修复：SQLite 对中文的 icontains 支持不好，改用 contains
            queryset = queryset.filter(
                Q(title__contains=search_query) |
                Q(original_prompt__contains=search_query) |
                Q(optimized_prompt__contains=search_query)
            )
            
        return queryset

    # 重写 create 方法 (当即前端点击“立即优化”时会触发这里)
    def create(self, request, *args, **kwargs):
        # 1. 拿到前端发来的原始提示词
        original_prompt = request.data.get('original_prompt')
        
        # 2. 呼叫 Kimi (Moonshot AI)
        client = OpenAI(
            api_key=os.getenv("MOONSHOT_API_KEY"),
            base_url="https://api.moonshot.cn/v1", # Kimi 的专用地址
        )

        try:
            # 3. 发送指令给 Kimi
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[
                    {"role": "system", "content": "你是一个资深的提示词(Prompt)优化专家。请优化用户输入的提示词，使其更加结构化、清晰、且能被AI更好地理解。直接输出优化后的内容，不要啰嗦。"},
                    {"role": "user", "content": original_prompt}
                ],
                temperature=0.3,
            )
            
            # 4. 拿到 Kimi 的回复
            optimized_content = completion.choices[0].message.content

            # 4.1 自动生成标题：取原始提示词的前10个字符，如果太长就加省略号
            # 也可以让 AI 帮忙总结，但为了省钱和速度，先用截取法
            auto_title = original_prompt[:10] + ('...' if len(original_prompt) > 10 else '')

            # 5. 保存到我们自己的数据库
            # 注意：我们创建一个新的 Prompt 对象，而不是直接保存 request.data
            prompt_instance = Prompt.objects.create(
                user=request.user,  # 关联当前用户
                title=request.data.get('title') or auto_title, # 优先用前端传的，没有就用自动生成的
                original_prompt=original_prompt,
                optimized_prompt=optimized_content
            )

            # 6. 把结果返回给前端
            serializer = self.get_serializer(prompt_instance)
            return Response(serializer.data)

        except Exception as e:
            print(f"调用 Kimi 出错了: {e}")
            # 如果出错，就返回一个错误提示，不存数据库了
            return Response({"error": str(e)}, status=500)