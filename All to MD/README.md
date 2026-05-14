# All to MD - PDF转Markdown工具

## 使用方法

### 方式一：双击启动（推荐）

1. 将需要转换的 **PDF 文件** 放入 `input` 文件夹
2. **双击** `启动转换.command`
3. 等待转换完成，结果会自动保存到 `output` 文件夹

### 方式二：命令行启动

```bash
cd "All to MD"
python3 convert_all.py
```

或转换单个文件：

```bash
python3 pdf_to_md.py input/文件名.pdf -o output/文件名.md
```

## 文件夹结构

```
All to MD/
├── input/              # 放入待转换的PDF文件
├── output/             # 转换后的Markdown文件
├── convert_all.py      # 批量转换脚本
├── pdf_to_md.py        # 单文件转换脚本
├── 启动转换.command     # 双击启动文件
└── README.md           # 本说明文件
```

## 功能特点

- ✅ 自动识别文本PDF和扫描PDF
- ✅ 扫描PDF自动使用OCR识别文字
- ✅ 支持批量转换
- ✅ 保留文档结构和分页
- ✅ 输出标准Markdown格式

## 依赖说明

- 使用 `pypdfium2` 处理PDF
- 使用 `RapidOCR` 进行OCR识别
- 首次运行时会自动下载所需模型

## 注意事项

1. 首次使用需要联网下载OCR模型（约20MB）
2. 大文件或扫描件转换可能需要较长时间
3. 转换质量取决于PDF的清晰度
