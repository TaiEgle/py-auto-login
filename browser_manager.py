#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器管理模块 - 优化启动和配置
"""

import os
import platform
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def get_base_dir() -> Path:
    """获取程序基准目录（兼容打包环境）"""
    import sys
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path.cwd()


def find_browser_executable() -> Optional[str]:
    """查找浏览器可执行文件路径
    
    优先级：
    1. 打包的浏览器（browser/chromium/）
    2. Playwright 下载的浏览器
    3. 系统安装的 Chrome
    """
    if not PLAYWRIGHT_AVAILABLE:
        return None
    
    base_dir = get_base_dir()
    system = platform.system()
    
    # 优先级 1: 打包的浏览器
    browser_dir = base_dir / "browser" / "chromium"
    if browser_dir.exists():
        entries = list(browser_dir.iterdir())
        chrome_subdir = None
        
        if system == "Windows":
            chrome_subdir = next((e for e in entries if e.name.startswith("chrome-win")), None)
        elif system == "Darwin":
            chrome_subdir = next((e for e in entries if e.name.startswith("chrome-mac")), None)
        elif system == "Linux":
            chrome_subdir = next((e for e in entries if e.name.startswith("chrome-linux")), None)
        
        if chrome_subdir:
            full_browser_dir = browser_dir / chrome_subdir
            if system == "Windows":
                chrome_path = full_browser_dir / "chrome.exe"
                if chrome_path.exists():
                    return str(chrome_path)
            elif system == "Darwin":
                chromium_app = full_browser_dir / "Chromium.app" / "Contents" / "MacOS" / "Chromium"
                chrome_direct = full_browser_dir / "chrome"
                if chromium_app.exists():
                    return str(chromium_app)
                elif chrome_direct.exists():
                    return str(chrome_direct)
            elif system == "Linux":
                chrome_path = full_browser_dir / "chrome"
                if chrome_path.exists():
                    return str(chrome_path)
    
    # 优先级 2: Playwright 下载的浏览器
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser_path = p.chromium.executable_path
            if browser_path and os.path.exists(browser_path):
                return browser_path
    except:
        pass
    
    # 优先级 3: 系统 Chrome
    if system == "Windows":
        chrome_candidates = [
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(os.environ.get("LOCALAPPDATA", "C:\\Users\\Default\\AppData\\Local")) / "Google" / "Chrome" / "Application" / "chrome.exe",
        ]
        for path in chrome_candidates:
            if path.exists():
                return str(path)
    elif system == "Darwin":
        mac_path = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if mac_path.exists():
            return str(mac_path)
    
    return None


def create_browser_launch_options(slow_mo: int = 50) -> Dict[str, Any]:
    """创建浏览器启动选项
    
    Args:
        slow_mo: 操作延迟（毫秒）
    
    Returns:
        启动选项字典
    """
    options = {
        'headless': False,
        'slow_mo': slow_mo,
    }
    
    browser_path = find_browser_executable()
    if browser_path:
        options['executable_path'] = browser_path
    
    return options


class BrowserManager:
    """浏览器管理器"""
    
    def __init__(self, slow_mo: int = 50):
        self.slow_mo = slow_mo
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    def start(self):
        """启动浏览器"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright 未安装。运行: pip install playwright && playwright install chromium")
        
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        
        launch_options = create_browser_launch_options(slow_mo=self.slow_mo)
        self.browser = self.playwright.chromium.launch(**launch_options)
        self.context = self.browser.new_context(viewport={'width': 1280, 'height': 800})
        self.page = self.context.new_page()
        
        return self.page
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            try:
                self.browser.close()
            except:
                pass
            self.browser = None
        
        if self.playwright:
            try:
                self.playwright.stop()
            except:
                pass
            self.playwright = None
        
        self.context = None
        self.page = None
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
