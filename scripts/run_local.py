"""本地调试启动脚本

模拟主框架的插件加载行为：从 plugin.json 读取入口点，
动态导入模块，自动发现插件类，实例化并启动。
Ctrl+C 优雅退出。

适用于所有遵循 MaaSR 插件规范的插件项目。
"""

import importlib
import inspect
import signal
import sys
import threading
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent
# 将 src 目录加入 sys.path，模拟框架加载 .pyz 后的 import 环境
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from plugin_framework import get_config

_shutdown_event = threading.Event()


def _on_signal(sig, frame):
    _shutdown_event.set()


def _find_plugin_class(module):
    """在模块中查找插件类（具有 start/stop 方法的类）。

    优先从 __all__ 导出中查找，否则扫描模块全部属性。

    Args:
        module: 已导入的模块对象

    Returns:
        找到的插件类，未找到则返回 None
    """
    candidates = []
    names = getattr(module, "__all__", None) or dir(module)

    for name in names:
        obj = getattr(module, name, None)
        if (
            obj is not None
            and inspect.isclass(obj)
            and hasattr(obj, "start")
            and hasattr(obj, "stop")
            and callable(getattr(obj, "start"))
            and callable(getattr(obj, "stop"))
        ):
            candidates.append(obj)

    if len(candidates) == 1:
        return candidates[0]

    # 多个候选时，优先选名称含 Plugin 的
    for cls in candidates:
        if "Plugin" in cls.__name__ or "plugin" in cls.__name__:
            return cls

    return candidates[0] if candidates else None


def main():
    config = get_config(ROOT_DIR)
    entry_point = config.get_entry_point()
    display_name = config.get_display_name()

    print(f"[run_local] 入口点: {entry_point}\n")

    # 动态导入插件模块
    module = importlib.import_module(entry_point)

    # 自动发现插件类
    plugin_cls = _find_plugin_class(module)
    if plugin_cls is None:
        print(f"[run_local] 错误: 模块 '{entry_point}' 中未找到插件类（需具有 start/stop 方法）")
        sys.exit(1)

    print(f"[run_local] 插件类: {plugin_cls.__name__}")

    plugin = plugin_cls()
    plugin.start()

    signal.signal(signal.SIGINT, _on_signal)
    signal.signal(signal.SIGTERM, _on_signal)

    try:
        _shutdown_event.wait()
    except KeyboardInterrupt:
        pass
    finally:
        plugin.stop()
        print(f"[run_local] {display_name} 已停止")


if __name__ == "__main__":
    main()
