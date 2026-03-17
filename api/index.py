import os
import sys
import traceback

try:
    # 将 backend 目录添加到 sys.path 的最前面，避免命名冲突
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

    # 导入 Django wsgi application
    from config.wsgi import application
    app = application
except Exception as e:
    # 如果启动失败，返回详细的错误信息
    error_details = traceback.format_exc()
    
    def app(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [f"Server Error:\n{error_details}".encode('utf-8')]
