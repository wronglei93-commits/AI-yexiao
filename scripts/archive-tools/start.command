#!/bin/bash
# macOS启动脚本 - 双击运行案件归档工具

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python"
    echo "下载地址: https://www.python.org/downloads/"
    read -p "按回车键退出..."
    exit 1
fi

# 检查依赖库
echo "检查依赖..."
python3 -c "from pypdf import PdfReader, PdfWriter" 2>/dev/null || \
python3 -c "from PyPDF2 import PdfReader, PdfWriter" 2>/dev/null || {
    echo "安装PDF处理库..."
    pip3 install pypdf -q || pip install pypdf -q
}

# 运行主程序
echo "启动案件归档工具..."
echo ""
python3 "$SCRIPT_DIR/archive_processor.py"
