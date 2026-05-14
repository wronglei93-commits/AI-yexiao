#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归档工具重置脚本
功能：清空归档文件夹和日志文件夹，恢复到初始状态
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


def reset_archive_tool():
    """重置归档工具到初始状态"""
    script_dir = Path(__file__).parent.absolute()

    print("="*50)
    print("案件归档工具 - 重置")
    print("="*50)
    print()

    # 需要清空的文件夹
    folders_to_clean = [
        (script_dir / "archive", "归档文件夹"),
        (script_dir / "logs", "日志文件夹"),
        (script_dir / "output", "输出文件夹")
    ]

    # 统计信息
    deleted_files = 0
    deleted_folders = 0

    for folder_path, folder_name in folders_to_clean:
        print(f"处理: {folder_name} ({folder_path.name})")

        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ 创建文件夹")
            continue

        # 获取文件夹内容
        items = list(folder_path.iterdir())

        if not items:
            print(f"  - 文件夹为空")
            continue

        # 删除所有内容
        for item in items:
            try:
                if item.is_file():
                    item.unlink()
                    deleted_files += 1
                    print(f"  ✓ 删除文件: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    deleted_folders += 1
                    print(f"  ✓ 删除文件夹: {item.name}")
            except Exception as e:
                print(f"  ✗ 删除失败 {item.name}: {e}")

        print()

    # 记录重置日志
    logs_folder = script_dir / "logs"
    logs_folder.mkdir(exist_ok=True)

    log_file = logs_folder / f"reset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"重置时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"删除文件数: {deleted_files}\n")
        f.write(f"删除文件夹数: {deleted_folders}\n")

    print("="*50)
    print("重置完成!")
    print(f"  删除文件: {deleted_files} 个")
    print(f"  删除文件夹: {deleted_folders} 个")
    print(f"  记录日志: {log_file.name}")
    print("="*50)
    print("\n归档工具已恢复到初始状态")


if __name__ == "__main__":
    print("警告: 此操作将删除归档文件夹和日志文件夹中的所有内容!")
    confirm = input("确认重置? (yes/no): ").strip().lower()

    if confirm in ('yes', 'y', '是'):
        reset_archive_tool()
    else:
        print("\n已取消重置操作")

    input("\n按回车键退出...")
