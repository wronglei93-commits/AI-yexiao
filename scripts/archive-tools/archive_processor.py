#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案件归档文件整理合并工具
功能：自动识别、排序并合并案件归档文件为PDF
"""

import os
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    try:
        from PyPDF2 import PdfReader, PdfWriter
    except ImportError:
        print("[错误] 未找到PDF处理库，请先安装: pip install pypdf")
        exit(1)


class ArchiveProcessor:
    """案件归档处理器"""

    def __init__(self, config_path: str = "config.json"):
        self.script_dir = Path(__file__).parent.absolute()
        self.config_path = self.script_dir / config_path
        self.config = self._load_config()
        self.setup_logging()

    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[错误] 加载配置文件失败: {e}")
            exit(1)

    def setup_logging(self):
        """设置日志"""
        logs_folder = self.script_dir / self.config['logs_folder']
        logs_folder.mkdir(exist_ok=True)

        log_file = logs_folder / f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"日志文件: {log_file}")

    def get_archive_folder(self) -> Path:
        """获取归档文件夹路径"""
        return self.script_dir / self.config['archive_folder']

    def get_output_folder(self) -> Path:
        """获取输出文件夹路径"""
        return self.script_dir / self.config['output_folder']

    def scan_files(self) -> List[Path]:
        """扫描归档文件夹中的所有PDF文件"""
        archive_folder = self.get_archive_folder()

        if not archive_folder.exists():
            self.logger.error(f"归档文件夹不存在: {archive_folder}")
            return []

        files = []
        for ext in self.config['supported_extensions']:
            files.extend(archive_folder.glob(f"*{ext}"))

        self.logger.info(f"扫描到 {len(files)} 个PDF文件")
        return sorted(files)

    def classify_file(self, filename: str) -> Tuple[Optional[int], Optional[str]]:
        """
        根据文件名分类文件到对应的顺序
        返回: (order, category_name) 或 (None, None) 表示无法分类
        """
        filename_lower = filename.lower()

        for category in self.config['file_order']:
            for keyword in category['keywords']:
                if keyword.lower() in filename_lower:
                    return category['order'], category['name']

        return None, None

    def organize_files(self, files: List[Path]) -> Dict[int, List[Tuple[Path, str]]]:
        """
        整理文件并按顺序分组
        返回: {order: [(file_path, category_name), ...]}
        """
        organized = {i: [] for i in range(1, 20)}  # 1-19的顺序
        skipped = []

        for file_path in files:
            order, category = self.classify_file(file_path.name)

            if order is not None:
                organized[order].append((file_path, category))
                self.logger.info(f"[匹配] {file_path.name} -> [{order}] {category}")
            else:
                skipped.append(file_path)
                self.logger.warning(f"[跳过] 无法识别: {file_path.name}")

        # 记录统计信息
        matched_count = sum(len(files) for files in organized.values())
        self.logger.info(f"\n整理完成: 匹配 {matched_count} 个, 跳过 {len(skipped)} 个")

        if skipped:
            self.logger.info("\n跳过的文件:")
            for f in skipped:
                self.logger.info(f"  - {f.name}")

        return organized

    def merge_pdfs(self, organized_files: Dict[int, List[Tuple[Path, str]]]) -> bool:
        """合并PDF文件"""
        output_folder = self.get_output_folder()
        output_folder.mkdir(exist_ok=True)

        output_path = output_folder / self.config['output_filename']

        # 如果输出文件已存在，先删除
        if output_path.exists():
            output_path.unlink()

        pdf_writer = PdfWriter()
        total_pages = 0
        file_count = 0

        # 添加封面页
        cover_added = self._add_cover_page(pdf_writer)

        # 按顺序处理文件
        for order in range(1, 20):
            files = organized_files.get(order, [])
            if not files:
                continue

            category_name = self.config['file_order'][order - 1]['name']
            self.logger.info(f"\n处理 [{order}] {category_name}: {len(files)} 个文件")

            for file_path, _ in files:
                try:
                    pdf_reader = PdfReader(str(file_path))
                    page_count = len(pdf_reader.pages)

                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)

                    total_pages += page_count
                    file_count += 1

                    self.logger.info(f"  ✓ {file_path.name} ({page_count}页)")

                except Exception as e:
                    self.logger.error(f"  ✗ {file_path.name} 读取失败: {e}")

        # 保存合并后的PDF
        if file_count == 0:
            self.logger.error("没有可合并的文件")
            return False

        try:
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)

            self.logger.info(f"\n{'='*50}")
            self.logger.info(f"合并完成!")
            self.logger.info(f"输出文件: {output_path}")
            self.logger.info(f"共合并 {file_count} 个文件, {total_pages} 页")
            self.logger.info(f"{'='*50}")

            return True

        except Exception as e:
            self.logger.error(f"保存PDF失败: {e}")
            return False

    def _add_cover_page(self, pdf_writer: PdfWriter) -> bool:
        """添加封面页（可选）"""
        # 如果需要添加封面，可以在这里实现
        # 目前直接返回True，不添加封面
        return True

    def generate_report(self, organized_files: Dict[int, List[Tuple[Path, str]]]) -> str:
        """生成归档报告"""
        report_lines = ["\n" + "="*60]
        report_lines.append("案件归档整理报告")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append("="*60)

        total_files = 0

        for order in range(1, 20):
            files = organized_files.get(order, [])
            category_name = self.config['file_order'][order - 1]['name']

            report_lines.append(f"\n[{order}] {category_name}")
            report_lines.append("-" * 40)

            if files:
                for file_path, _ in files:
                    report_lines.append(f"  • {file_path.name}")
                    total_files += 1
            else:
                report_lines.append("  (无)")

        report_lines.append(f"\n{'='*60}")
        report_lines.append(f"总计: {total_files} 个文件")
        report_lines.append("="*60)

        report = "\n".join(report_lines)
        return report

    def run(self):
        """运行归档处理流程"""
        self.logger.info("="*50)
        self.logger.info("案件归档文件整理工具")
        self.logger.info("="*50)

        # 1. 扫描文件
        files = self.scan_files()
        if not files:
            self.logger.error("归档文件夹中没有找到PDF文件")
            self.logger.info(f"请将PDF文件放入文件夹: {self.get_archive_folder()}")
            return False

        # 2. 整理文件
        organized = self.organize_files(files)

        # 3. 生成报告
        report = self.generate_report(organized)
        print(report)
        self.logger.info(report)

        # 4. 确认合并
        print("\n")
        confirm = input("确认合并以上文件? (Y/n): ").strip().lower()
        if confirm in ('', 'y', 'yes', '是'):
            return self.merge_pdfs(organized)
        else:
            self.logger.info("用户取消合并")
            return False


def main():
    """主函数"""
    processor = ArchiveProcessor()
    success = processor.run()

    if success:
        print("\n✓ 归档完成!")
    else:
        print("\n✗ 归档失败")

    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
