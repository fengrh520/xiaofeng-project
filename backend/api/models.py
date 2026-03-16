from django.db import models
from django.contrib.auth.models import User # 引入用户模型

class Prompt(models.Model):
    # 标题，最多200个字
        # 新增：关联用户 (外键)
    # on_delete=models.CASCADE 表示如果用户被删了，他的数据也一起删
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户")
    # 新增：星标/收藏功能
    is_starred = models.BooleanField(default=False, verbose_name="是否星标")
    
    # 新增：置顶功能
    is_pinned = models.BooleanField(default=False, verbose_name="是否置顶")

    # 标题，最多200个字
    title = models.CharField(max_length=200, verbose_name="标题")
    
    # 原始提示词，TextField适合存长文本
    original_prompt = models.TextField(verbose_name="原始提示词")
    
    # 优化后提示词，blank=True 和 null=True 表示允许为空（因为还没优化时它是空的）
    optimized_prompt = models.TextField(verbose_name="优化后提示词", blank=True, null=True)
    
    # 创建时间，auto_now_add=True 表示在数据第一次创建时自动填入当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    # 更新时间，auto_now=True 表示每次修改这条数据时，自动更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "提示词"
        verbose_name_plural = "提示词列表"
        # 默认按创建时间倒序排列（最新的在最前面）
        ordering = ['-created_at']

    # 这个方法决定了在 Django 后台管理系统中，这条数据长什么名字
    def __str__(self):
        return self.title