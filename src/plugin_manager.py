"""
插件管理接口

提供插件的基本管理功能，包括版本管理、配置管理等。
"""

import json
import re
from pathlib import Path
from typing import Any


class PluginManager:
    """插件管理器
    
    提供插件的配置读取、版本管理等功能。
    """
    
    def __init__(self, config_path: Path | None = None):
        """初始化插件管理器
        
        Args:
            config_path: 插件配置文件路径，默认为 plugin.json
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "plugin.json"
        
        self.config_path = config_path
        self._config: dict[str, Any] | None = None
    
    @property
    def config(self) -> dict[str, Any]:
        """获取插件配置
        
        Returns:
            dict: 插件配置字典
        """
        if self._config is None:
            self._load_config()
        return self._config or {}
    
    def _load_config(self) -> None:
        """加载插件配置"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)
    
    def get_version(self) -> str:
        """获取插件版本
        
        Returns:
            str: 版本号
        """
        return self.config.get("version", "0.0.0")
    
    def get_name(self) -> str:
        """获取插件名称
        
        Returns:
            str: 插件名称
        """
        return self.config.get("name", "unknown")
    
    def get_display_name(self) -> str:
        """获取插件显示名称
        
        Returns:
            str: 显示名称
        """
        return self.config.get("display_name", self.get_name())
    
    def get_description(self) -> str:
        """获取插件描述
        
        Returns:
            str: 插件描述
        """
        return self.config.get("description", "")
    
    def get_author(self) -> str:
        """获取插件作者
        
        Returns:
            str: 作者名称
        """
        return self.config.get("author", "")
    
    def get_dependencies(self) -> list[str]:
        """获取插件依赖列表
        
        Returns:
            list: 依赖列表
        """
        return self.config.get("dependencies", [])
    
    def get_exports(self) -> dict[str, str]:
        """获取插件导出的 API
        
        Returns:
            dict: API 映射字典
        """
        return self.config.get("exports", {})
    
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
        required_fields = ["name", "version", "entry_point"]
        
        for field in required_fields:
            if field not in self.config:
                errors.append(f"缺少必需字段: {field}")
        
        # 验证版本号格式
        version = self.config.get("version", "")
        if not version or not self._is_valid_version(version):
            errors.append(f"无效的版本号: {version}")
        
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
        pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z]+)?$"
        return bool(re.match(pattern, version))


# 全局插件管理器实例
_manager: PluginManager | None = None


def get_plugin_manager() -> PluginManager:
    """获取全局插件管理器实例
    
    Returns:
        PluginManager: 插件管理器实例
    """
    global _manager
    if _manager is None:
        _manager = PluginManager()
    return _manager
