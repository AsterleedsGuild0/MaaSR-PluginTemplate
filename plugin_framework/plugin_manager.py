"""
插件管理接口

提供插件的基本管理功能，包括版本管理、配置管理等。
"""

import re
from pathlib import Path
from typing import Any

from .config import Config, get_config


class PluginManager:
    """插件管理器
    
    提供插件的配置读取、版本管理等功能。
    使用统一的 Config 类管理配置。
    """
    
    def __init__(self, root_dir: Path | None = None):
        """初始化插件管理器
        
        Args:
            root_dir: 项目根目录
        """
        self._config = get_config(root_dir)
    
    @property
    def config(self) -> dict[str, Any]:
        """获取插件配置
        
        Returns:
            dict: 插件配置字典
        """
        return self._config.plugin_config
    
    def get_version(self) -> str:
        """获取插件版本
        
        Returns:
            str: 版本号
        """
        return self._config.get_version()
    
    def get_name(self) -> str:
        """获取插件名称
        
        Returns:
            str: 插件名称
        """
        return self._config.get_name()
    
    def get_display_name(self) -> str:
        """获取插件显示名称
        
        Returns:
            str: 显示名称
        """
        return self._config.get_display_name()
    
    def get_description(self) -> str:
        """获取插件描述
        
        Returns:
            str: 插件描述
        """
        return self._config.get_description()
    
    def get_author(self) -> str:
        """获取插件作者
        
        Returns:
            str: 作者名称
        """
        return self._config.get_author()
    
    def get_dependencies(self) -> list[str]:
        """获取插件依赖列表
        
        Returns:
            list: 依赖列表
        """
        return self._config.get_dependencies()
    
    def get_exports(self) -> dict[str, str]:
        """获取插件导出的 API
        
        Returns:
            dict: API 映射字典
        """
        return self._config.get("exports", {})
    
    def get_info(self) -> dict[str, Any]:
        """获取插件完整信息
        
        Returns:
            dict: 插件信息字典
        """
        return {
            "name": self.get_name(),
            "display_name": self.get_display_name(),
            "version": self.get_version(),
            "description": self.get_description(),
            "author": self.get_author(),
            "dependencies": self.get_dependencies(),
            "exports": self.get_exports()
        }
    
    def validate_config(self) -> tuple[bool, list[str]]:
        """验证配置文件的完整性
        
        Returns:
            tuple: (是否有效, 错误信息列表)
        """
        errors = []
        
        # 检查必需字段
        if not self.get_name():
            errors.append("缺少插件名称")
        
        version = self.get_version()
        if not version or not self._is_valid_version(version):
            errors.append(f"无效的版本号: {version}")
        
        if not self._config.get_entry_point():
            errors.append("缺少入口点配置")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _is_valid_version(version: str) -> bool:
        """验证版本号格式
        
        Args:
            version: 版本号字符串
            
        Returns:
            bool: 是否有效
        """
        # 简单的语义化版本验证
        pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$"
        return bool(re.match(pattern, version))


# 全局插件管理器实例
_manager: PluginManager | None = None


def get_plugin_manager(root_dir: Path | None = None) -> PluginManager:
    """获取全局插件管理器实例
    
    Args:
        root_dir: 项目根目录
        
    Returns:
        PluginManager: 插件管理器实例
    """
    global _manager
    if _manager is None or root_dir is not None:
        _manager = PluginManager(root_dir)
    return _manager
