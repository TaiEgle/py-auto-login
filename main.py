#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动登录脚本 - Python 版本（优化版）
功能：使用 Playwright 和 OCR 自动登录系统
"""

import sys
import time
import base64
import re
import signal
import traceback
import platform
from pathlib import Path
from datetime import datetime
from io import BytesIO

from config import Config, get_base_dir
from lock_manager import LockFile
from browser_manager import BrowserManager
from ocr_engine import create_ocr_engine, get_available_engines


def log_error(log_file: Path, message: str):
    """记录错误日志"""
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp} {message}\n\n")
    except:
        pass


def setup_signal_handlers(lock: LockFile, log_file: Path):
    """设置信号处理器"""
    def cleanup_handler(signum, frame):
        lock.release()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, cleanup_handler)
    signal.signal(signal.SIGTERM, cleanup_handler)
    if platform.system() == "Windows":
        signal.signal(signal.SIGBREAK, cleanup_handler)


def wait_for_captcha_image(page, img_selector: str, max_retries: int = 5) -> str:
    """等待并获取验证码图片 Base64 数据"""
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 等待图片元素
            page.wait_for_selector(img_selector, timeout=20000, state='visible')
            print("✓ 验证码图片元素已找到，等待数据加载...")
            
            # 等待 Base64 数据完整加载
            def check_image_loaded():
                img = page.query_selector(img_selector)
                if not img:
                    return False
                src = img.get_attribute('src') or ''
                if not src.startswith('data:image'):
                    return False
                match = re.match(r'^data:image/\w+;base64,(.+)$', src)
                return match and match.group(1) and len(match.group(1)) > 100
            
            # 轮询检查
            start_time = time.time()
            while time.time() - start_time < 30:
                if check_image_loaded():
                    break
                time.sleep(0.5)
            
            print("✓ 验证码数据加载完成，正在验证...")
            
            # 提取 Base64
            img = page.query_selector(img_selector)
            src = img.get_attribute('src') or ''
            if src.startswith('data:image'):
                match = re.match(r'^data:image/\w+;base64,(.+)$', src)
                if match and match.group(1) and len(match.group(1)) > 100:
                    return src
            
            raise Exception("验证码数据不完整")
            
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"⚠ 验证码加载中... (重试 {retry_count}/{max_retries})")
                time.sleep(2)
                # 尝试刷新验证码
                try:
                    page.click(img_selector)
                    time.sleep(1)
                    print("  -> 已刷新验证码")
                except:
                    pass
            else:
                print("⚠ 验证码加载超时，正在刷新页面...")
                page.reload(wait_until='networkidle', timeout=60000)
    
    return None


def perform_login(page, username: str, password: str, captcha_code: str):
    """执行登录操作"""
    page.fill('#form_item_principal', username)
    page.fill('#form_item_credentials', password)
    page.fill('#form_item_verificationCode', '')
    page.fill('#form_item_verificationCode', captcha_code)
    
    print("正在提交登录...")
    page.click('.ant-btn-block')
    time.sleep(3)


def handle_post_login(page):
    """处理登录后的操作"""
    try:
        time.sleep(2)
        
        # 关闭可能存在的弹窗
        close_btn = page.locator('button:has-text("关 闭"), button:has-text("关闭")').first
        if close_btn.is_visible(timeout=5000):
            close_btn.click()
            print("-> 已自动关闭提示弹窗")
        
        # 进入目标模块
        menu_selector = 'li[data-menu-id="/aqhb/home"]'
        page.wait_for_selector(menu_selector, timeout=10000)
        page.click(menu_selector)
        print("-> 已成功跳转至：安全环保首页")
    except Exception as biz_error:
        print(f"登录后业务操作提示: {biz_error}")


def main():
    """主函数"""
    base_dir = get_base_dir()
    config_path = base_dir / "config.json"
    lang_path = base_dir / "lang-data"
    log_file = base_dir / "error.log"
    lock_file = base_dir / "python-auto-login.lock"
    
    # 单实例锁
    lock = LockFile(str(lock_file))
    if not lock.acquire():
        print("无法获取锁文件，程序可能已在运行。")
        sys.exit(1)
    
    setup_signal_handlers(lock, log_file)
    
    try:
        # 加载配置
        config = Config(config_path)
        if not config_path.exists():
            print("--------------------------------------------------")
            print("【首次运行提示】已在当前目录生成 config.json")
            print("请填写账号密码后重新运行程序。")
            print("--------------------------------------------------")
            time.sleep(5)
            return
        
        config_data = config.load()
        username = config.username
        password = config.password
        headless = config.headless
        ocr_engine_type = config.ocr_engine
        max_retries = config.max_retries
        slow_mo = config.slow_mo
        
        # 检查并显示可用的 OCR 引擎
        available_engines = get_available_engines()
        if not available_engines:
            print("错误：没有可用的 OCR 引擎。请安装 Tesseract 或 EasyOCR。")
            sys.exit(1)
        
        print("可用的 OCR 引擎:")
        for engine_type, description in available_engines:
            print(f"  - {description}")
        
        # 初始化 OCR 引擎
        try:
            ocr_engine = create_ocr_engine(ocr_engine_type, lang_path if lang_path.exists() else None)
            engine_name = 'Tesseract' if 'tesseract' in ocr_engine_type.lower() else 'EasyOCR'
            print(f"✓ 使用 OCR 引擎: {engine_name}")
        except Exception as e:
            print(f"错误：OCR 引擎初始化失败: {e}")
            sys.exit(1)
        
        # 启动浏览器
        print(f"[系统]: {platform.system()} | 正在尝试启动浏览器...")
        if headless:
            print("-> 使用无头模式（减少资源占用）")
        
        browser_manager = None
        try:
            browser_manager = BrowserManager(headless=headless, slow_mo=slow_mo)
            page = browser_manager.start()
            print("✅ 浏览器启动成功")
            
            # 访问登录页面
            print("正在访问登录页面...")
            page.goto("https://aqsc.ykjt.cc/login?origin=sso", wait_until='networkidle', timeout=60000)
            
            login_success = False
            img_selector = "img.img-code"
            
            # 登录重试循环
            for attempt in range(1, max_retries + 1):
                print(f"\n>>> 正在尝试第 {attempt}/{max_retries} 次登录...")
                
                print("正在等待验证码加载...")
                
                # 等待并获取验证码图片
                base64_string = wait_for_captcha_image(page, img_selector)
                if not base64_string:
                    print("无法获取验证码图片，正在刷新页面重试...")
                    page.reload(wait_until='networkidle', timeout=60000)
                    continue
                
                # 验证并提取图片数据
                match = re.match(r'^data:image/\w+;base64,(.+)$', base64_string)
                if not match or not match.group(1) or len(match.group(1)) < 100:
                    print("验证码数据不完整，正在刷新页面重试...")
                    page.reload(wait_until='networkidle', timeout=60000)
                    continue
                
                image_data = base64.b64decode(match.group(1))
                
                # OCR 识别
                captcha_result = ""
                try:
                    captcha_result = ocr_engine.recognize(image_data)
                except Exception as ocr_err:
                    error_msg = str(ocr_err)
                    print(f"OCR 失败: {error_msg}")
                    try:
                        page.click(img_selector)
                        time.sleep(1.5)
                    except:
                        pass
                    continue
                
                print(f"识别验证码: [{captcha_result}]")
                
                # 执行登录
                perform_login(page, username, password, captcha_result)
                
                # 检查登录结果
                current_url = page.url
                if 'login' not in current_url:
                    print("✅ 登录成功！正在进入业务页面...")
                    login_success = True
                    break
                else:
                    print("❌ 识别错误或账号密码有误，重试中...")
                    if attempt < max_retries:
                        try:
                            page.click(img_selector)
                            time.sleep(1)
                        except:
                            pass
            
            # 登录后的后续操作
            if login_success:
                handle_post_login(page)
                
                print("\n--------------------------------------------------")
                print("提示：请勿关闭终端，关闭浏览器窗口即可退出程序。")
                print("--------------------------------------------------")
                
                # 等待浏览器关闭
                try:
                    if browser_manager.context:
                        browser_manager.context.wait_for_event('close', timeout=None)
                except:
                    while browser_manager.browser and browser_manager.browser.is_connected():
                        time.sleep(1)
            else:
                print(f"\n[失败]: 已重试 {max_retries} 次，登录未能成功。")
            
        except Exception as error:
            error_msg = f"[程序异常] {error}\n{traceback.format_exc()}"
            log_error(log_file, error_msg)
            print(f"\n[程序异常]: {error}")
            traceback.print_exc()
        finally:
            if browser_manager:
                browser_manager.close()
            print("程序已安全退出。")
    
    finally:
        lock.release()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        log_error(get_base_dir() / "error.log", f"[未捕获异常] {e}\n{traceback.format_exc()}")
        print(f"\n未捕获的异常: {e}")
        traceback.print_exc()
        sys.exit(1)
