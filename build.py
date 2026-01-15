#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 用于本地打包
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


def main():
    """主函数"""
    system = platform.system()
    
    print("=" * 60)
    print("Python 自动登录脚本 - 打包工具")
    print("=" * 60)
    print(f"系统: {system}")
    print(f"Python: {sys.version}")
    print()
    
    # 检查依赖
    print("正在检查依赖...")
    try:
        import PyInstaller
    except ImportError:
        print("错误：未安装 PyInstaller，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 构建 PyInstaller 命令（优化体积）
    pyinstaller_cmd = [
        "pyinstaller",
        "--name=auto-login",
        "--onefile",
        "--console",
        "--clean",
        "--noconfirm",
        "--strip",  # 去除符号信息（减小体积）
        "--noupx",  # 不使用 UPX 压缩（提高兼容性，但体积稍大）
    ]
    
    # Windows 特定选项
    if system == "Windows":
        pyinstaller_cmd.extend([
            "--icon=NONE",  # 可以添加 .ico 图标文件
        ])
    
    # 添加隐藏导入（仅必需模块）
    hidden_imports = [
        "playwright.sync_api",
        "playwright._impl._driver",
        "pytesseract",
        "PIL",
        "PIL.Image",
        "PIL.ImageTk",
        "config",
        "browser_manager",
        "lock_manager",
        "ocr_engine",
    ]
    
    # 可选导入（检查是否安装）
    optional_imports = ["psutil", "easyocr"]
    for imp in optional_imports:
        try:
            __import__(imp)
            hidden_imports.append(imp)
        except ImportError:
            pass
    
    for imp in hidden_imports:
        pyinstaller_cmd.extend(["--hidden-import", imp])
    
    # 排除不必要的模块（减小体积）
    excludes = [
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "tkinter",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "pytest",
        "unittest",
        "email",
        "http",
        "urllib3",
    ]
    for exc in excludes:
        pyinstaller_cmd.extend(["--exclude-module", exc])
    
    # 执行打包
    print("正在执行打包...")
    print(f"命令: {' '.join(pyinstaller_cmd)}")
    print()
    
    result = subprocess.run(pyinstaller_cmd, cwd=Path(__file__).parent)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print(f"输出目录: {Path(__file__).parent / 'dist'}")
        print()
        print("注意：")
        print("1. 需要手动安装 Playwright 浏览器：")
        print("   playwright install chromium")
        print("2. 需要安装 Tesseract OCR")
        print("3. 可能需要将浏览器和语言数据复制到 dist 目录")
    else:
        print()
        print("=" * 60)
        print("❌ 打包失败！")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
