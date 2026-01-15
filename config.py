#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional


def get_base_dir() -> Path:
    """获取程序基准目录（兼容打包环境）"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path.cwd()


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: Optional[Path] = None):
        self.base_dir = get_base_dir()
        self.config_file = config_file or (self.base_dir / "config.json")
        self._config: Dict[str, Any] = {}
    
    def load(self) -> Dict[str, Any]:
        """加载配置"""
        if not self.config_file.exists():
            self._create_default()
            return self._config
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            return self._config
        except Exception as e:
            raise RuntimeError(f"加载配置文件失败: {e}")
    
    def save(self, config: Dict[str, Any]):
        """保存配置"""
        self._config = config
        try:
            # 确保目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"保存配置文件失败: {e} (路径: {self.config_file})")
    
    def _create_default(self):
        """创建默认配置"""
        default_config = {
            "username": "你的账号",
            "password": "你的密码",
            "slow_mo": 50,  # 操作延迟（毫秒）
        }
        self.save(default_config)
        self._config = default_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)
    
    @property
    def username(self) -> str:
        """用户名"""
        return self.get('username', '')
    
    @property
    def password(self) -> str:
        """密码"""
        return self.get('password', '')
    
    @property
    def slow_mo(self) -> int:
        """操作延迟"""
        return self.get('slow_mo', 50)
