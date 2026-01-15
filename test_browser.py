#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器测试脚本
"""

from browser_manager import BrowserManager, find_browser_executable
import time


def main():
    print("=" * 60)
    print("浏览器测试")
    print("=" * 60)
    
    # 检查浏览器路径
    print("\n正在查找浏览器可执行文件...")
    browser_path = find_browser_executable()
    
    if browser_path:
        print(f"✅ 找到浏览器: {browser_path}")
    else:
        print("⚠️  未找到打包的浏览器，将使用 Playwright 默认浏览器")
    
    # 测试浏览器启动
    print("\n" + "=" * 60)
    print("测试浏览器启动（有界面模式）")
    print("=" * 60)
    
    try:
        print("\n正在启动浏览器...")
        with BrowserManager(headless=False, slow_mo=100) as bm:
            page = bm.page
            print("✅ 浏览器启动成功")
            
            print("\n正在访问测试页面...")
            page.goto("https://www.example.com", timeout=30000)
            print("✅ 页面加载成功")
            
            title = page.title()
            print(f"✅ 页面标题: {title}")
            
            print("\n浏览器将保持打开 5 秒，你可以看到浏览器窗口...")
            time.sleep(5)
            
            print("✅ 浏览器测试通过")
    except Exception as e:
        print(f"❌ 浏览器启动失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 测试无头模式
    print("\n" + "=" * 60)
    print("测试浏览器启动（无头模式）")
    print("=" * 60)
    
    try:
        print("\n正在启动浏览器（无头模式）...")
        with BrowserManager(headless=True, slow_mo=50) as bm:
            page = bm.page
            print("✅ 浏览器启动成功（无头模式）")
            
            print("\n正在访问测试页面...")
            page.goto("https://www.example.com", timeout=30000)
            print("✅ 页面加载成功")
            
            title = page.title()
            print(f"✅ 页面标题: {title}")
            
            print("✅ 无头模式测试通过")
    except Exception as e:
        print(f"❌ 无头模式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("所有测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
