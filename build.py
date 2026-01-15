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
    
    # 检查 pip 是否可用（通过尝试运行 pip 命令）
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, timeout=5)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args)
        print("✓ pip 可用")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("错误：pip 未安装或不可用。请先安装 pip。")
        print("安装方法：")
        print(f"  - 运行: {sys.executable} -m ensurepip --upgrade")
        print("  - 或访问: https://pip.pypa.io/en/stable/installation/")
        sys.exit(1)
    
    # 检查并安装 PyInstaller
    pyinstaller_cmd_path = None
    try:
        import PyInstaller
        # 尝试找到 pyinstaller 可执行文件
        import shutil
        pyinstaller_cmd_path = shutil.which("pyinstaller")
        if not pyinstaller_cmd_path:
            # 如果找不到命令行工具，使用模块方式
            pyinstaller_cmd_path = f"{sys.executable} -m PyInstaller"
            print("✓ PyInstaller 已安装，使用模块方式运行")
        else:
            print("✓ PyInstaller 已安装")
    except ImportError:
        print("未安装 PyInstaller，正在安装...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✓ PyInstaller 安装成功")
            # 安装后再次尝试找到
            import shutil
            pyinstaller_cmd_path = shutil.which("pyinstaller")
            if not pyinstaller_cmd_path:
                pyinstaller_cmd_path = f"{sys.executable} -m PyInstaller"
        except subprocess.CalledProcessError as e:
            print(f"❌ PyInstaller 安装失败: {e}")
            sys.exit(1)
    
    # 构建 PyInstaller 命令（优化体积）
    # 根据是否找到命令行工具选择执行方式
    if isinstance(pyinstaller_cmd_path, str) and " -m " in pyinstaller_cmd_path:
        # 使用模块方式：python -m PyInstaller
        pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]
    else:
        # 使用命令行方式：pyinstaller
        pyinstaller_cmd = [pyinstaller_cmd_path or "pyinstaller"]
    
    # 添加 PyInstaller 参数
    pyinstaller_cmd.extend([
        "--name=auto-login",
        "--onefile",
        "--console",
        "--clean",
        "--noconfirm",
        "--strip",  # 去除符号信息（减小体积）
        "--noupx",  # 不使用 UPX 压缩（提高兼容性，但体积稍大）
        "--optimize=2",  # Python 字节码优化级别
    ])
    
    # Windows 特定选项
    if system == "Windows":
        pyinstaller_cmd.extend([
            "--icon=NONE",  # 可以添加 .ico 图标文件
        ])
    
    # 添加隐藏导入（仅必需模块）
    hidden_imports = [
        "playwright.sync_api",
        "playwright._impl._driver",
        "config",
        "browser_manager",
        "lock_manager",
    ]
    
    
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
        "pytesseract",
        "PIL",
        "easyocr",
    ]
    for exc in excludes:
        pyinstaller_cmd.extend(["--exclude-module", exc])
    
    # 添加要打包的主脚本文件
    pyinstaller_cmd.append("main.py")
    
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
        print("1. 如果使用系统浏览器，用户需要安装 Chrome/Edge")
        print("2. 如果需要打包浏览器，运行：playwright install chromium")
        print("3. 然后将 browser 目录复制到 dist 目录")
    else:
        print()
        print("=" * 60)
        print("❌ 打包失败！")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
