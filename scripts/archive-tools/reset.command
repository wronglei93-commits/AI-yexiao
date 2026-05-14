#!/bin/bash
# macOS重置脚本 - 双击重置归档工具

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3"
    read -p "按回车键退出..."
    exit 1
fi

# 运行重置脚本
python3 "$SCRIPT_DIR/reset.py"
