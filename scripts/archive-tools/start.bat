@echo off
chcp 65001 >nul
REM Windows启动脚本 - 双击运行案件归档工具

REM 获取脚本所在目录
cd /d "%~dp0"

echo ========================================
echo 案件归档工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖库
echo 检查依赖...
python -c "from pypdf import PdfReader, PdfWriter" 2>nul || (
    echo 安装PDF处理库...
    pip install pypdf -q
)

echo.
echo 启动案件归档工具...
echo.
python archive_processor.py

pause
