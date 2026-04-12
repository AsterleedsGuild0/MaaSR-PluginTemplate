"""
示例插件主模块

这个文件展示了如何实现一个基本的 MaaStarResonance 插件。
"""
from typing import Any

from .utils.common_util import get_runtime_config


class ExamplePlugin:
    """示例插件类
    
    这是一个简单的插件示例，展示了插件的基本结构。
    演示如何从 plugin.json 读取元数据。
    """
    
    def __init__(self):
        """初始化插件"""
        # 从 plugin.json 读取元数据
        plugin_info = get_runtime_config()
        self.name = plugin_info.get("display_name", "ExamplePlugin")
        self.version = plugin_info.get("version", "0.0.0")
        self.description = plugin_info.get("description", "")
        self.author = plugin_info.get("author", "")
        
    def start(self) -> bool:
        """启动插件
        
        Returns:
            bool: 启动是否成功
        """
        print(f"{self.name} v{self.version} 已启动")
        return True
        
    def stop(self) -> bool:
        """停止插件
        
        Returns:
            bool: 停止是否成功
        """
        print(f"{self.name} 已停止")
        return True
        
    def get_info(self) -> dict[str, Any]:
        """获取插件信息
        
        Returns:
            dict: 插件信息字典
        """
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author
        }
