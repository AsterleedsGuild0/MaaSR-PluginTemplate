#!/usr/bin/env python3
"""
开发环境初始化脚本

在 uv sync 后运行，生成开发所需的配置文件。

用法:
    uv run init-dev
    或
    python scripts/init_dev.py
"""

import json
import sys
from pathlib import Path

from plugin_framework.config import get_config


def log_info(msg: str) -> None:
    """打印信息日志"""
    print(f"[INFO] {msg}")


def log_success(msg: str) -> None:
    """打印成功日志"""
    print(f"[SUCCESS] {msg}")


def generate_plugin_json(repo_root: Path) -> None:
    """生成根目录的 plugin.json
    
    Args:
        repo_root: 仓库根目录
    """
    plugin_json_path = repo_root / "plugin.json"
    
    # 删除旧的 plugin.json，确保从 pyproject.toml 读取最新配置
    if plugin_json_path.exists():
        plugin_json_path.unlink()
    
    config = get_config(repo_root)
    plugin_json = config.to_plugin_json()
    
    with open(plugin_json_path, "w", encoding="utf-8") as f:
        json.dump(plugin_json, f, ensure_ascii=False, indent=2)
    
    log_success(f"生成 plugin.json: {plugin_json_path}")


def main() -> int:
    """主函数"""
    log_info("开始初始化开发环境...")
    
    # 获取仓库根目录
    repo_root = Path(__file__).parent.parent.resolve()
    
    # 生成 plugin.json
    generate_plugin_json(repo_root)
    
    log_success("开发环境初始化完成！")
    return 0


if __name__ == "__main__":
    sys.exit(main())
