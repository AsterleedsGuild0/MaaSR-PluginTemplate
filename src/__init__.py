"""
MaaStarResonance 侧载插件模板

这是一个示例插件，展示如何创建 MaaStarResonance 的侧载插件。
"""

__version__ = "0.1.0"
__author__ = "AZMIAO"

from .example_plugin import ExamplePlugin
from .plugin_manager import PluginManager, get_plugin_manager

__all__ = ["ExamplePlugin", "PluginManager", "get_plugin_manager"]
