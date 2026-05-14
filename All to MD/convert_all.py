#!/usr/bin/env python3
"""
All to MD - PDF to Markdown Converter
自动监控 input 文件夹，转换后输出到 output 文件夹
"""

import sys
import os
from pathlib import Path

# 确保能找到依赖包
current_dir = Path(__file__).parent.resolve()

# 添加 Python 包路径
site_packages = Path.home() / "Library/Python/3.9/lib/python/site-packages"
if str(site_packages) not in sys.path:
    sys.path.insert(0, str(site_packages))

try:
    import pypdfium2 as pdfium
    from rapidocr import RapidOCR
except ImportError:
    print("缺少依赖，正在安装...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdfium2", "rapidocr", "onnxruntime", "-q"])
    import pypdfium2 as pdfium
    from rapidocr import RapidOCR


def extract_text_from_pdf(pdf_path: str, ocr_engine) -> str:
    """从PDF提取文本"""
    pdf = pdfium.PdfDocument(pdf_path)

    all_text = []
    all_text.append(f"# {Path(pdf_path).stem}\n")
    all_text.append(f"*Converted from PDF - {len(pdf)} pages*\n")

    for page_num in range(len(pdf)):
        page = pdf[page_num]
        all_text.append(f"\n---\n\n## Page {page_num + 1}\n")

        text_page = page.get_textpage()
        text = text_page.get_text_bounded()

        if text.strip():
            all_text.append(text.strip())
        elif ocr_engine:
            print(f"  第 {page_num + 1} 页: 使用OCR识别...")
            bitmap = page.render(scale=2.0)
            pil_image = bitmap.to_pil()
            result, _ = ocr_engine(pil_image)
            if result:
                ocr_text = "\n".join([line[1] for line in result])
                all_text.append(ocr_text)
            else:
                all_text.append("*[未检测到文本]*")
        else:
            all_text.append("*[无文本内容]*")

    pdf.close()
    return "\n".join(all_text)


def main():
    input_dir = current_dir / "input"
    output_dir = current_dir / "output"

    print("=" * 60)
    print("All to MD - PDF转Markdown工具")
    print("=" * 60)
    print(f"输入文件夹: {input_dir}")
    print(f"输出文件夹: {output_dir}")
    print("=" * 60)

    # 确保文件夹存在
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # 查找PDF文件
    pdf_files = list(input_dir.glob("*.pdf")) + list(input_dir.glob("*.PDF"))

    if not pdf_files:
        print("\n未找到PDF文件，请将PDF放入 input 文件夹后重试。")
        input("\n按回车键退出...")
        return

    print(f"\n找到 {len(pdf_files)} 个PDF文件")
    print("\n正在初始化OCR引擎...")
    ocr_engine = RapidOCR()
    print("OCR引擎就绪！\n")

    success_count = 0
    for pdf_file in pdf_files:
        output_file = output_dir / f"{pdf_file.stem}.md"
        print(f"转换中: {pdf_file.name}")

        try:
            markdown_content = extract_text_from_pdf(str(pdf_file), ocr_engine)
            output_file.write_text(markdown_content, encoding='utf-8')
            print(f"  ✓ 完成: {output_file.name}")
            success_count += 1
        except Exception as e:
            print(f"  ✗ 失败: {e}")

    print("\n" + "=" * 60)
    print(f"转换完成: {success_count}/{len(pdf_files)} 成功")
    print(f"输出位置: {output_dir}")
    print("=" * 60)

    input("\n按回车键退出...")


if __name__ == '__main__':
    main()
