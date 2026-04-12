import json
from pathlib import Path
from typing import Any


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