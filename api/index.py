import os
import sys

# 将 backend 目录添加到 sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# 导入 Django wsgi application
from config.wsgi import application

# Vercel 需要一个名为 app 的可调用对象
app = application
