"""
示例插件

这是插件的核心代码，只包含插件的业务逻辑。
"""

from maasr_plugin_example.example_plugin import ExamplePlugin

# 模块级单例，供主程序插件加载器自动启动
_instance = ExamplePlugin()


def start() -> bool:
    """启动插件（由主程序插件加载器自动调用）。"""
    return _instance.start()


def stop() -> bool:
    """停止插件。"""
    return _instance.stop()


def get_info() -> dict:
    """获取插件信息。"""
    return _instance.get_info()


__all__ = ["ExamplePlugin", "start", "stop", "get_info"]
