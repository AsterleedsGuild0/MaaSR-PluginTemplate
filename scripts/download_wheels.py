#!/usr/bin/env python3
"""
下载 Python Wheels 脚本

从 PyPI 下载项目依赖的 wheel 文件到指定目录。

用法:
    python scripts/download_wheels.py
    python scripts/download_wheels.py --platform win_amd64 --python-version 3.13
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def read_plugin_config(config_path: Path) -> dict:
    """读取插件配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def download_wheels(
    dest: Path,
    packages: list[str],
    platform: str | None = None,
    python_version: str | None = None,
    abi: str | None = None
) -> None:
    """下载 wheel 文件
    
    Args:
        dest: 目标目录
        packages: 包列表
        platform: 平台标识
        python_version: Python 版本
        abi: ABI 标识
    """
    dest.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        sys.executable, "-m", "pip", "download",
        "--dest", str(dest),
        "--only-binary", ":all:"
    ]
    
    if platform:
        cmd.extend(["--platform", platform])
    if python_version:
        cmd.extend(["--python-version", python_version])
    if abi:
        cmd.extend(["--abi", abi])
    
    cmd.extend(packages)
    
    print(f"执行命令: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(description="下载 Python Wheels")
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("deps"),
        help="输出目录 (默认: deps/)"
    )
    parser.add_argument("--platform", help="平台标识 (如: win_amd64)")
    parser.add_argument("--python-version", help="Python 版本 (如: 3.13)")
    parser.add_argument("--abi", help="ABI 标识 (如: cp313)")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("plugin.json"),
        help="插件配置文件路径"
    )
    
    args = parser.parse_args()
    
    # 读取配置文件获取依赖列表
    config = read_plugin_config(args.config)
    dependencies = config.get("dependencies", [])
    if not dependencies:
        print("没有需要下载的依赖")
        return 0
    
    # 过滤掉本地文件路径格式的依赖
    packages = [dep for dep in dependencies if not dep.startswith("deps/")]
    
    if not packages:
        print("没有需要从 PyPI 下载的依赖")
        return 0
    
    download_wheels(
        args.dest,
        packages,
        args.platform,
        args.python_version,
        args.abi
    )
    
    print(f"✅ 成功下载 {len(packages)} 个依赖到 {args.dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
