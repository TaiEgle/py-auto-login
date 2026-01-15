#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 引擎封装 - 支持多种 OCR 实现
"""

import platform
import os
from pathlib import Path
from io import BytesIO
from typing import Optional

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


class OCREngine:
    """OCR 引擎基类"""
    
    def recognize(self, image_data: bytes, language: str = 'eng') -> str:
        """识别图片中的文字"""
        raise NotImplementedError
    
    def is_available(self) -> bool:
        """检查引擎是否可用"""
        return False


class TesseractEngine(OCREngine):
    """Tesseract OCR 引擎（轻量级，体积小）"""
    
    def __init__(self, lang_data_path: Optional[Path] = None):
        self.lang_data_path = lang_data_path
        self._tesseract_cmd = None
        self._configured = False
    
    def _configure_tesseract(self):
        """配置 Tesseract 路径"""
        if self._configured:
            return
        
        system = platform.system()
        tesseract_cmd = None
        
        if system == "Windows":
            candidates = [
                os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), 
                           "Tesseract-OCR", "tesseract.exe"),
                os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), 
                           "Tesseract-OCR", "tesseract.exe"),
                "tesseract.exe"
            ]
            for path in candidates:
                if os.path.exists(path):
                    tesseract_cmd = path
                    break
            
            if not tesseract_cmd and os.environ.get("TESSDATA_PREFIX"):
                tesseract_path = os.path.join(
                    os.path.dirname(os.environ.get("TESSDATA_PREFIX")), "tesseract.exe"
                )
                if os.path.exists(tesseract_path):
                    tesseract_cmd = tesseract_path
        elif system == "Darwin":
            mac_paths = [
                "/usr/local/bin/tesseract",
                "/opt/homebrew/bin/tesseract",
                "/usr/bin/tesseract"
            ]
            for path in mac_paths:
                if os.path.exists(path):
                    tesseract_cmd = path
                    break
        else:
            tesseract_cmd = "tesseract"
        
        if tesseract_cmd and TESSERACT_AVAILABLE:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            self._tesseract_cmd = tesseract_cmd
        
        # 设置语言数据路径
        if self.lang_data_path and self.lang_data_path.exists():
            os.environ['TESSDATA_PREFIX'] = str(self.lang_data_path)
        
        self._configured = True
    
    def is_available(self) -> bool:
        """检查 Tesseract 是否可用"""
        if not TESSERACT_AVAILABLE:
            return False
        try:
            self._configure_tesseract()
            # 测试是否能调用
            pytesseract.get_tesseract_version()
            return True
        except:
            return False
    
    def recognize(self, image_data: bytes, language: str = 'eng') -> str:
        """使用 Tesseract 识别"""
        if not TESSERACT_AVAILABLE:
            raise RuntimeError("Tesseract 未安装")
        
        self._configure_tesseract()
        
        # 加载图片
        image = Image.open(BytesIO(image_data))
        
        # 构建配置（限制字符集为英文数字，提高识别速度和准确率）
        config_parts = ['-c', 'tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']
        if self.lang_data_path and self.lang_data_path.exists():
            config_parts.insert(0, f'--tessdata-dir "{self.lang_data_path}"')
        
        custom_config = ' '.join(config_parts)
        
        # 识别
        try:
            text = pytesseract.image_to_string(image, lang=language, config=custom_config)
            # 移除所有空白字符
            return ''.join(text.split())
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR 识别失败: {e}")


class EasyOCREngine(OCREngine):
    """EasyOCR 引擎（准确率高，但体积较大）"""
    
    def __init__(self):
        self._reader = None
        self._initialized = False
    
    def _initialize(self):
        """初始化 EasyOCR 读取器（延迟加载，减少启动时间）"""
        if self._initialized:
            return
        
        if not EASYOCR_AVAILABLE:
            raise RuntimeError("EasyOCR 未安装")
        
        try:
            # 只加载英文识别器（减小内存占用）
            self._reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            self._initialized = True
        except Exception as e:
            raise RuntimeError(f"EasyOCR 初始化失败: {e}")
    
    def is_available(self) -> bool:
        """检查 EasyOCR 是否可用"""
        if not EASYOCR_AVAILABLE:
            return False
        try:
            self._initialize()
            return True
        except:
            return False
    
    def recognize(self, image_data: bytes, language: str = 'en') -> str:
        """使用 EasyOCR 识别"""
        if not EASYOCR_AVAILABLE:
            raise RuntimeError("EasyOCR 未安装")
        
        self._initialize()
        
        # 加载图片
        image = Image.open(BytesIO(image_data))
        
        # 识别（EasyOCR 返回结果格式: [(bbox, text, confidence), ...]）
        try:
            results = self._reader.readtext(image, paragraph=False)
            # 合并所有识别到的文字
            text = ''.join([result[1] for result in results])
            # 移除空白字符
            return ''.join(text.split())
        except Exception as e:
            raise RuntimeError(f"EasyOCR 识别失败: {e}")


def get_available_engines() -> list:
    """获取所有可用的 OCR 引擎"""
    available = []
    
    # 测试 Tesseract
    test_engine = TesseractEngine()
    if test_engine.is_available():
        available.append(('tesseract', 'Tesseract OCR（轻量级，推荐）'))
    
    # 测试 EasyOCR
    if EASYOCR_AVAILABLE:
        try:
            test_engine = EasyOCREngine()
            if test_engine.is_available():
                available.append(('easyocr', 'EasyOCR（高准确率，体积较大）'))
        except:
            pass
    
    return available


def create_ocr_engine(engine_type: str = 'auto', lang_data_path: Optional[Path] = None) -> OCREngine:
    """创建 OCR 引擎实例
    
    Args:
        engine_type: 引擎类型 ('tesseract', 'easyocr', 'auto')
        lang_data_path: Tesseract 语言数据路径（仅 Tesseract 使用）
    
    Returns:
        OCREngine 实例
    """
    if engine_type == 'auto':
        # 自动选择：优先使用 Tesseract（更轻量）
        tesseract_engine = TesseractEngine(lang_data_path)
        if tesseract_engine.is_available():
            return tesseract_engine
        
        if EASYOCR_AVAILABLE:
            easyocr_engine = EasyOCREngine()
            if easyocr_engine.is_available():
                return easyocr_engine
        
        raise RuntimeError("没有可用的 OCR 引擎。请安装 Tesseract 或 EasyOCR。")
    
    elif engine_type == 'tesseract':
        engine = TesseractEngine(lang_data_path)
        if not engine.is_available():
            raise RuntimeError("Tesseract 不可用。请安装 Tesseract OCR。")
        return engine
    
    elif engine_type == 'easyocr':
        if not EASYOCR_AVAILABLE:
            raise RuntimeError("EasyOCR 未安装。运行: pip install easyocr")
        engine = EasyOCREngine()
        if not engine.is_available():
            raise RuntimeError("EasyOCR 初始化失败。")
        return engine
    
    else:
        raise ValueError(f"未知的 OCR 引擎类型: {engine_type}")
