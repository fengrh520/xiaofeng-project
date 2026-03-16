#!/bin/bash
# 1. 安装后端依赖
echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

# 2. 构建前端
echo "Building Frontend..."
cd frontend
npm install
npm run build
cd ..

# 3. 收集静态文件 (如果有 Django admin 的话，可选)
# python backend/manage.py collectstatic --noinput
