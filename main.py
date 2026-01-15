#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动登录脚本 - Python 版本（精简优化版）
功能：使用 Playwright 自动登录系统（无需 OCR）
"""

import sys
import time
import signal
import traceback
import platform
from pathlib import Path
from datetime import datetime

from config import Config, get_base_dir
from lock_manager import LockFile
from browser_manager import BrowserManager


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


def main():
    """主函数"""
    base_dir = get_base_dir()
    config_path = base_dir / "config.json"
    log_file = base_dir / "error.log"
    lock_file = base_dir / "python-auto-login.lock"
    
    # 单实例锁
    lock = LockFile(str(lock_file))
    if not lock.acquire():
        print("无法获取锁文件，程序可能已在运行。")
        sys.exit(1)
    
    setup_signal_handlers(lock, log_file)
    
    try:
        # 加载配置（如果不存在会自动创建）
        config = Config(config_path)
        config_exists = config_path.exists()
        config_data = config.load()
        
        # 检查是否是首次运行（配置文件刚被创建或配置为空）
        if not config_exists or not config.username or config.username == "你的账号":
            print("--------------------------------------------------")
            print("【首次运行提示】已在当前目录生成 config.json")
            print(f"配置文件位置: {config_path}")
            print("请填写账号密码后重新运行程序。")
            print("--------------------------------------------------")
            time.sleep(5)
            return
        
        username = config.username
        password = config.password
        slow_mo = config.slow_mo
        
        # 启动浏览器
        print(f"[系统]: {platform.system()} | 正在尝试启动浏览器...")
        browser_manager = None
        try:
            browser_manager = BrowserManager(slow_mo=slow_mo)
            page = browser_manager.start()
            print("✅ 浏览器启动成功")
            
            # 访问登录页面
            print("正在访问登录页面...")
            page.goto("https://iam.ykjt.cc:8443/login/#/", wait_until='domcontentloaded', timeout=60000)
            
            print("\n>>> 正在尝试登录...")
            page.wait_for_selector("div.login-box-sw", state='visible', timeout=15000)
            
            # 切换到账号密码登录
            try:
                is_username_mode = page.locator('input[placeholder="请输入用户名"]').is_visible(timeout=2000)
            except:
                is_username_mode = False
            
            if not is_username_mode:
                print("切换到账号密码登录方式...")
                page.locator("div.login-box-sw").click()
                time.sleep(0.5)
            
            # 填写账号密码
            page.wait_for_selector('input[placeholder="请输入用户名"]', state='visible', timeout=10000)
            page.fill('input[placeholder="请输入用户名"]', username)
            page.fill('input[placeholder="请输入密码"]', password)
            print("✓ 账号密码填写完成")
            
            # 提交登录
            print("正在提交登录...")
            login_url = page.url
            page.click('button:has-text("登录")')
            
            # 等待登录结果
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
            except:
                pass
            time.sleep(3)
            
            # 检查登录是否成功
            current_url = page.url
            url_changed = current_url != login_url
            
            # 检查是否存在登录成功后的特征元素
            has_login_element = False
            try:
                page.wait_for_selector('[title="安全生产技术综合管控平台"]', timeout=3000)
                has_login_element = True
            except:
                pass
            
            # 判断登录成功：URL 改变 或 存在特征元素
            login_success = url_changed or has_login_element
            
            if login_success:
                print("✅ 登录成功！正在进入业务页面...")
                try:
                    time.sleep(2)
                    
                    # 点击进入安全生产技术综合管控平台
                    title_selector = '[title="安全生产技术综合管控平台"]'
                    page.wait_for_selector(title_selector, state='visible', timeout=10000)
                    
                    # 等待新标签页打开
                    new_page = None
                    with browser_manager.context.expect_page(timeout=10000) as page_info:
                        page.click(title_selector)
                    new_page = page_info.value
                    
                    print("-> 已成功跳转至：安全生产技术综合管控平台（新标签页）")
                    new_page.wait_for_load_state('domcontentloaded')
                    time.sleep(1)
                    
                    # 点击关闭按钮
                    try:
                        close_btn = new_page.locator('button.ant-btn').filter(has_text=r'关.*闭')
                        close_btn.wait_for(state='visible', timeout=5000)
                        close_btn.click()
                        time.sleep(0.5)
                        print("✓ 已点击关闭按钮")
                    except:
                        # 备用方式：JavaScript点击
                        clicked = new_page.evaluate("""() => {
                            const buttons = Array.from(document.querySelectorAll('button.ant-btn'));
                            const btn = buttons.find(b => {
                                const text = b.textContent || '';
                                return text.includes('关') && text.includes('闭');
                            });
                            if (btn) {
                                btn.click();
                                return true;
                            }
                            return false;
                        }""")
                        if clicked:
                            time.sleep(0.5)
                            print("✓ 已点击关闭按钮（JavaScript方式）")
                    
                    # 跳转到安全环保首页
                    if 'dashboard' in new_page.url:
                        menu_selector = 'li[data-menu-id*="/aqhb/home"]'
                        new_page.wait_for_selector(menu_selector, timeout=10000)
                        new_page.click(menu_selector)
                        print("-> 已成功跳转至：安全环保首页")
                        
                except Exception as biz_error:
                    print(f"登录后业务操作提示: {biz_error}")
                
                print("\n--------------------------------------------------")
                print("提示：请勿关闭终端，关闭浏览器窗口即可退出程序。")
                print("--------------------------------------------------")
                
                # 等待浏览器关闭
                browser_closed = False
                try:
                    # 监听浏览器关闭事件
                    browser = browser_manager.browser
                    if browser:
                        # 持续检查浏览器连接状态，直到断开
                        while True:
                            try:
                                if not browser.is_connected():
                                    print("\n✓ 检测到浏览器已关闭，正在退出程序...")
                                    browser_closed = True
                                    break
                                # 检查所有上下文是否都已关闭（用户关闭所有标签页）
                                contexts = browser.contexts
                                if len(contexts) == 0:
                                    print("\n✓ 检测到所有浏览器标签页已关闭，正在退出程序...")
                                    browser_closed = True
                                    # 关闭浏览器
                                    try:
                                        browser.close()
                                    except:
                                        pass
                                    break
                                time.sleep(0.5)  # 更频繁地检查（每0.5秒）
                            except Exception as e:
                                # 如果浏览器对象已经无效，说明已关闭
                                print(f"\n✓ 浏览器连接已断开，正在退出程序...")
                                browser_closed = True
                                break
                except Exception as e:
                    print(f"\n等待浏览器关闭时出错: {e}")
                
                # 标记浏览器已关闭，避免 finally 块中重复关闭
                if browser_closed:
                    browser_manager.browser = None
            else:
                print("❌ 登录失败：账号密码有误或登录页面未跳转")
            
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
