#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单实例锁管理模块
"""

import os
import sys
import time
import json
import platform
import subprocess
import signal
from pathlib import Path
from typing import Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

if platform.system() != "Windows":
    import fcntl


class LockFile:
    """单实例锁文件管理（优化版）"""
    
    def __init__(self, lock_file_path: str):
        self.lock_file_path = Path(lock_file_path)
        self.lock_file = None
        self.pid = os.getpid()
        self._is_windows = platform.system() == "Windows"
    
    def acquire(self) -> bool:
        """获取锁，如果已有实例运行则尝试关闭它"""
        # 检查并处理旧实例
        if self.lock_file_path.exists():
            try:
                with open(self.lock_file_path, 'r', encoding='utf-8') as f:
                    lock_data = json.load(f)
                    old_pid = lock_data.get('pid')
                    if old_pid and old_pid != self.pid:
                        if self._is_process_running(old_pid):
                            print(f"检测到先前运行的实例 pid={old_pid}，正在尝试关闭...")
                            if self._terminate_process(old_pid):
                                print("已关闭先前实例。")
                            else:
                                print(f"无法关闭先前实例，请手动结束进程或删除文件：{self.lock_file_path}")
                                return False
                        else:
                            print("发现陈旧锁文件（进程不存在），已继续。")
            except Exception as e:
                print(f"读取锁文件时出错：{e}")
        
        # 创建新的锁文件
        try:
            if self._is_windows:
                # Windows: 使用独占模式创建文件
                try:
                    self.lock_file = open(self.lock_file_path, 'x', encoding='utf-8')
                except FileExistsError:
                    raise IOError("锁文件已存在")
            else:
                # Unix: 使用 fcntl 文件锁
                self.lock_file = open(self.lock_file_path, 'w', encoding='utf-8')
                try:
                    fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except IOError:
                    self.lock_file.close()
                    raise
            
            # 写入锁信息
            lock_data = {
                'pid': self.pid,
                'exec': sys.executable,
                'cwd': os.getcwd(),
                'start': int(time.time() * 1000)
            }
            json.dump(lock_data, self.lock_file, indent=2, ensure_ascii=False)
            self.lock_file.flush()
            
            if self._is_windows:
                # Windows: 可以关闭文件
                self.lock_file.close()
                self.lock_file = None
            
            return True
        except (IOError, OSError, FileExistsError) as e:
            if self.lock_file:
                try:
                    self.lock_file.close()
                except:
                    pass
                self.lock_file = None
            print(f"无法获取锁文件：{e}")
            return False
    
    def release(self):
        """释放锁"""
        try:
            if self.lock_file and not self._is_windows:
                # Unix: 释放文件锁并关闭文件
                try:
                    fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
                except:
                    pass
                try:
                    self.lock_file.close()
                except:
                    pass
                self.lock_file = None
            
            # 删除锁文件（仅当是自己的锁时）
            if self.lock_file_path.exists():
                try:
                    with open(self.lock_file_path, 'r', encoding='utf-8') as f:
                        lock_data = json.load(f)
                        if lock_data.get('pid') == self.pid:
                            self.lock_file_path.unlink()
                except:
                    # 如果读取失败，也尝试删除
                    try:
                        self.lock_file_path.unlink()
                    except:
                        pass
        except Exception as e:
            print(f"释放锁文件时出错：{e}")
    
    def _is_process_running(self, pid: int) -> bool:
        """检查进程是否运行"""
        if PSUTIL_AVAILABLE:
            try:
                return psutil.pid_exists(pid)
            except:
                pass
        
        # 兼容方法：尝试发送信号 0
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    
    def _terminate_process(self, pid: int) -> bool:
        """终止进程"""
        try:
            if self._is_windows:
                subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'], 
                             capture_output=True, timeout=5)
            else:
                os.kill(pid, signal.SIGTERM)
                start = time.time()
                while self._is_process_running(pid) and time.time() - start < 4:
                    time.sleep(0.2)
                if self._is_process_running(pid):
                    os.kill(pid, signal.SIGKILL)
            
            time.sleep(0.5)
            return not self._is_process_running(pid)
        except Exception as e:
            print(f"终止进程时出错：{e}")
            return False
