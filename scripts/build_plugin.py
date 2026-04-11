#!/usr/bin/env python3
"""
构建插件脚本

将 src/ 目录下的代码打包为 .pyz 格式的插件，并生成标准的插件目录结构。

用法:
    python scripts/build_plugin.py
    python scripts/build_plugin.py --output dist/
    python scripts/build_plugin.py --skip-deps
"""

import argparse
import json
import shutil
import subprocess
import sys
import zipapp
from pathlib import Path


def log_info(msg: str) -> None:
    """打印信息日志"""
    print(f"[INFO] {msg}")


def log_error(msg: str) -> None:
    """打印错误日志"""
    print(f"[ERROR] {msg}", file=sys.stderr)


def log_success(msg: str) -> None:
    """打印成功日志"""
    print(f"[SUCCESS] {msg}")


def read_plugin_config(config_path: Path) -> dict:
    """读取插件配置文件
    
    Args:
        config_path: plugin.json 文件路径
        
    Returns:
        dict: 插件配置字典
    """
    if not config_path.exists():
        log_error(f"插件配置文件不存在: {config_path}")
        sys.exit(1)
        
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        log_error(f"插件配置文件格式错误: {e}")
        sys.exit(1)


def create_pyz(src_dir: Path, output_file: Path, entry_point: str) -> None:
    """创建 .pyz 文件
    
    Args:
        src_dir: 源代码目录
        output_file: 输出的 .pyz 文件路径
        entry_point: Python 模块入口点
    """
    log_info(f"打包 {src_dir} -> {output_file}")
    
    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 使用 zipapp 创建 .pyz 文件
    try:
        zipapp.create_archive(
            source=str(src_dir),
            target=str(output_file),
            interpreter=None,  # 不指定 shebang
            main=None,  # 不指定 __main__.py
            compressed=True
        )
        log_success(f"成功创建 .pyz 文件: {output_file}")
    except Exception as e:
        log_error(f"创建 .pyz 文件失败: {e}")
        sys.exit(1)


def download_dependencies(deps_dir: Path, requirements: list[str]) -> None:
    """下载依赖到 deps/ 目录
    
    Args:
        deps_dir: 依赖目录
        requirements: 依赖列表
    """
    if not requirements:
        log_info("没有需要下载的依赖")
        return
        
    log_info(f"下载依赖到 {deps_dir}")
    deps_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        cmd = [
            sys.executable, "-m", "pip", "download",
            "--dest", str(deps_dir),
            "--only-binary", ":all:",
            *requirements
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        log_success(f"成功下载 {len(requirements)} 个依赖")
    except subprocess.CalledProcessError as e:
        log_error(f"下载依赖失败: {e.stderr.decode()}")
        sys.exit(1)


def build_plugin(
    repo_root: Path,
    output_dir: Path,
    skip_deps: bool = False
) -> Path:
    """构建插件
    
    Args:
        repo_root: 仓库根目录
        output_dir: 输出目录
        skip_deps: 是否跳过依赖下载
        
    Returns:
        Path: 插件目录路径
    """
    # 读取插件配置
    config_path = repo_root / "plugin.json"
    config = read_plugin_config(config_path)
    
    plugin_name = config["name"]
    log_info(f"开始构建插件: {plugin_name}")
    
    # 创建插件目录结构
    plugin_dir = output_dir / plugin_name
    if plugin_dir.exists():
        log_info(f"清理旧的插件目录: {plugin_dir}")
        shutil.rmtree(plugin_dir)
    
    plugin_dir.mkdir(parents=True, exist_ok=True)
    lib_dir = plugin_dir / "lib"
    lib_dir.mkdir(parents=True, exist_ok=True)
    
    # 打包 .pyz 文件
    src_dir = repo_root / "src"
    pyz_file = lib_dir / f"{plugin_name}.pyz"
    create_pyz(src_dir, pyz_file, config["entry_point"])
    # 下载依赖
    if not skip_deps and config.get("dependencies"):
        deps_dir = plugin_dir / "deps"
        # 从配置中提取依赖包名（去掉版本号）
        requirements = []
        for dep in config.get("dependencies", []):
            # 如果是文件路径格式，跳过
            if dep.startswith("deps/"):
                continue
            requirements.append(dep)
        
        if requirements:
            download_dependencies(deps_dir, requirements)
    
    # 复制 plugin.json
    shutil.copy2(config_path, plugin_dir / "plugin.json")
    
    log_success(f"插件构建完成: {plugin_dir}")
    return plugin_dir


def create_zip_package(plugin_dir: Path, output_dir: Path, version: str) -> Path:
    """创建 ZIP 压缩包
    
    Args:
        plugin_dir: 插件目录
        output_dir: 输出目录
        version: 版本号
        
    Returns:
        Path: ZIP 文件路径
    """
    plugin_name = plugin_dir.name
    zip_name = f"{plugin_name}-{version}"
    zip_path = output_dir / f"{zip_name}.zip"
    
    log_info(f"创建 ZIP 压缩包: {zip_path}")
    
    # 创建 ZIP 文件
    shutil.make_archive(
        str(output_dir / zip_name),
        "zip",
        root_dir=str(plugin_dir.parent),
        base_dir=plugin_name
    )
    
    log_success(f"ZIP 压缩包创建完成: {zip_path}")
    return zip_path


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(description="构建 MaaStarResonance 插件")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dist"),
        help="输出目录 (默认: dist/)"
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="跳过依赖下载"
    )
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="不创建 ZIP 压缩包"
    )
    
    args = parser.parse_args()
    
    # 获取仓库根目录
    repo_root = Path(__file__).parent.parent.resolve()
    
    # 构建插件
    plugin_dir = build_plugin(repo_root, args.output, args.skip_deps)
    
    # 创建 ZIP 压缩包
    if not args.no_zip:
        config = read_plugin_config(repo_root / "plugin.json")
        version = config["version"]
        create_zip_package(plugin_dir, args.output, version)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
