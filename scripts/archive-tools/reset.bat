@echo off
chcp 65001 >nul
REM Windows重置脚本 - 双击重置归档工具

REM 获取脚本所在目录
cd /d "%~dp0"

echo ========================================
echo 案件归档工具 - 重置
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python
    pause
    exit /b 1
)

REM 运行重置脚本
python reset.py

pause
