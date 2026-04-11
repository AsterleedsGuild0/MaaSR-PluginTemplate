"""
插件入口点

当插件作为 .pyz 文件运行时的入口。
"""

from .example_plugin import ExamplePlugin

if __name__ == "__main__":
    plugin = ExamplePlugin()
    plugin.start()
