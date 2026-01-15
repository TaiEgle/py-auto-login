#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 引擎测试脚本
"""

from ocr_engine import get_available_engines, create_ocr_engine
from pathlib import Path


def main():
    print("=" * 60)
    print("OCR 引擎测试")
    print("=" * 60)
    
    # 检查可用引擎
    print("\n正在检查可用的 OCR 引擎...")
    engines = get_available_engines()
    
    if not engines:
        print("❌ 没有可用的 OCR 引擎！")
        print("\n请安装 OCR 引擎：")
        print("  - Tesseract: brew install tesseract (macOS)")
        print("  - EasyOCR: pip install easyocr")
        return
    
    print("\n✅ 可用的 OCR 引擎:")
    for engine_type, description in engines:
        print(f"  - {description}")
    
    # 测试 Tesseract
    print("\n" + "=" * 60)
    print("测试 Tesseract OCR")
    print("=" * 60)
    
    lang_path = Path.cwd() / "lang-data"
    lang_path = lang_path if lang_path.exists() else None
    
    try:
        ocr = create_ocr_engine('tesseract', lang_path)
        print("✅ Tesseract OCR 初始化成功")
        
        # 尝试获取 Tesseract 版本
        try:
            import pytesseract
            version = pytesseract.get_tesseract_version()
            print(f"  版本: {version}")
        except:
            pass
        
        print("✅ Tesseract 可用，可以正常使用")
    except Exception as e:
        print(f"❌ Tesseract 不可用: {e}")
    
    # 测试 EasyOCR（如果可用）
    print("\n" + "=" * 60)
    print("测试 EasyOCR")
    print("=" * 60)
    
    try:
        ocr = create_ocr_engine('easyocr', None)
        print("✅ EasyOCR 初始化成功")
        print("⚠️  注意：EasyOCR 首次运行需要下载模型文件（约 100MB）")
        print("✅ EasyOCR 可用，可以正常使用")
    except Exception as e:
        print(f"⚠️  EasyOCR 不可用: {e}")
        print("   这是正常的，EasyOCR 是可选的")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
