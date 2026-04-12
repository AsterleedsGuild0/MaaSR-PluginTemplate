"""
插件框架模块

提供插件开发所需的基础设施，包括配置管理和插件管理功能。
这些代码不会被打包到插件中，仅用于开发时使用。
"""

from .config import Config, get_config
from .plugin_manager import PluginManager, get_plugin_manager

__all__ = [
    "Config",
    "get_config",
    "PluginManager",
    "get_plugin_manager",
]
