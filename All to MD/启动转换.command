#!/bin/zsh

# All to MD 启动脚本
# 将此文件放入 All to MD 文件夹，双击即可运行

cd "$(dirname "$0")"

echo "正在启动 PDF 转 Markdown 工具..."
echo ""

# 使用系统 Python3 运行脚本
/usr/bin/python3 "convert_all.py"
