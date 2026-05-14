#!/usr/bin/env python3
"""
PDF to Markdown Converter using RapidOCR for OCR support
轻量级OCR方案，无需下载大模型
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    import pypdfium2 as pdfium
except ImportError:
    print("Installing pypdfium2...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdfium2", "-q"])
    import pypdfium2 as pdfium

try:
    from rapidocr import RapidOCR
except ImportError:
    print("Installing rapidocr...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rapidocr", "-q"])
    from rapidocr import RapidOCR


def extract_text_from_pdf(pdf_path: str, use_ocr: bool = True) -> str:
    """
    Extract text from PDF using pypdfium2 and RapidOCR

    Args:
        pdf_path: Path to PDF file
        use_ocr: Whether to use OCR for image-based pages

    Returns:
        Extracted text in Markdown format
    """
    pdf = pdfium.PdfDocument(pdf_path)
    ocr_engine = RapidOCR() if use_ocr else None

    all_text = []
    all_text.append(f"# {Path(pdf_path).stem}\n")
    all_text.append(f"*Converted from PDF - {len(pdf)} pages*\n")

    for page_num in range(len(pdf)):
        page = pdf[page_num]
        all_text.append(f"\n---\n\n## Page {page_num + 1}\n")

        # Try to extract text directly first
        text_page = page.get_textpage()
        text = text_page.get_text_bounded()

        if text.strip():
            # Text-based PDF
            all_text.append(text.strip())
        elif use_ocr and ocr_engine:
            # Image-based PDF, use OCR
            print(f"  Page {page_num + 1}: Running OCR...")
            bitmap = page.render(scale=2.0)
            pil_image = bitmap.to_pil()

            result, elapse = ocr_engine(pil_image)
            if result:
                ocr_text = "\n".join([line[1] for line in result])
                all_text.append(ocr_text)
            else:
                all_text.append("*[No text detected on this page]*")
        else:
            all_text.append("*[No text content]*")

    pdf.close()
    return "\n".join(all_text)


def convert_pdf_to_markdown(pdf_path: str, output_path: Optional[str] = None) -> str:
    """
    Convert PDF file to Markdown with OCR support

    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path for output Markdown file

    Returns:
        Markdown content as string
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    if not pdf_file.suffix.lower() == '.pdf':
        print(f"Error: File must be a PDF: {pdf_path}")
        sys.exit(1)

    print(f"Converting: {pdf_path}")
    print("This may take a while for large files or if OCR is needed...\n")

    try:
        markdown_content = extract_text_from_pdf(str(pdf_file), use_ocr=True)

        # Determine output path
        if output_path is None:
            output_path = pdf_file.with_suffix('.md')
        else:
            output_path = Path(output_path)

        # Write output
        output_path.write_text(markdown_content, encoding='utf-8')

        print(f"\n{'='*50}")
        print(f"SUCCESS! Conversion completed.")
        print(f"{'='*50}")
        print(f"Output saved to: {output_path}")
        print(f"Output size: {len(markdown_content)} characters")
        print(f"{'='*50}")

        return markdown_content

    except Exception as e:
        print(f"\nError during conversion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert PDF to Markdown using RapidOCR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf
  %(prog)s input.pdf -o output.md
  %(prog)s ~/documents/file.pdf --output ~/notes/file.md

Requirements:
  - pypdfium2: PDF processing
  - rapidocr: OCR for scanned documents
        """
    )
    parser.add_argument(
        'input',
        help='Input PDF file path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output Markdown file path (default: same as input with .md extension)'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='pdf_to_md 1.0 (using RapidOCR)'
    )

    args = parser.parse_args()

    convert_pdf_to_markdown(args.input, args.output)


if __name__ == '__main__':
    main()
