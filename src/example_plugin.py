"""
示例插件主模块

这个文件展示了如何实现一个基本的 MaaStarResonance 插件。
"""
import json
from pathlib import Path
from typing import Any


class ExamplePlugin:
    """示例插件类
    
    这是一个简单的插件示例，展示了插件的基本结构。
    演示如何从 plugin.json 读取元数据。
    """
    
    def __init__(self):
        """初始化插件"""
        # 从 plugin.json 读取元数据
        plugin_info = self.get_runtime_config()
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

    @staticmethod
    def get_runtime_config() -> dict[str, Any]:
        """获取运行时配置（从 plugin.json）

        这个函数会自动检测运行环境：
        - 开发环境：从仓库根目录读取 plugin.json
        - 部署环境（.pyz）：从 .pyz 文件向上两级读取 plugin.json

        Returns:
            dict: plugin.json 的内容

        Raises:
            FileNotFoundError: 如果找不到 plugin.json
        """
        # 获取当前文件的路径
        current_file = Path(__file__).resolve()

        # 尝试多个可能的路径
        possible_paths = [
            # 开发环境：plugin_framework/config.py -> 根目录
            current_file.parent.parent / "plugin.json",
            # 部署环境：lib/xxx.pyz/plugin_framework/config.py -> 插件目录
            current_file.parent.parent.parent.parent / "plugin.json",
        ]

        for plugin_json_path in possible_paths:
            if plugin_json_path.exists():
                with open(plugin_json_path, "r", encoding="utf-8") as f:
                    return json.load(f)

        # 如果都找不到，抛出异常
        raise FileNotFoundError(
            f"无法找到 plugin.json，尝试过的路径：\n" +
            "\n".join(f"  - {p}" for p in possible_paths)
        )
