"""
配置管理模块

统一管理插件配置，支持从 pyproject.toml 和 plugin.json 读取配置。
"""

import json
import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        import toml as tomllib  # type: ignore


class Config:
    """统一配置管理类
    
    优先级: plugin.json > pyproject.toml
    """
    
    def __init__(self, root_dir: Path | None = None):
        """初始化配置管理器
        
        Args:
            root_dir: 项目根目录，默认为当前文件的父目录
        """
        if root_dir is None:
            root_dir = Path(__file__).parent.parent
        
        self.root_dir = root_dir
        self._plugin_config: dict[str, Any] | None = None
        self._pyproject_config: dict[str, Any] | None = None
    
    @property
    def plugin_config(self) -> dict[str, Any]:
        """获取 plugin.json 配置"""
        if self._plugin_config is None:
            plugin_json = self.root_dir / "plugin.json"
            if plugin_json.exists():
                with open(plugin_json, "r", encoding="utf-8") as f:
                    self._plugin_config = json.load(f)
            else:
                self._plugin_config = {}
        return self._plugin_config
    
    @property
    def pyproject_config(self) -> dict[str, Any]:
        """获取 pyproject.toml 配置"""
        if self._pyproject_config is None:
            pyproject_toml = self.root_dir / "pyproject.toml"
            if pyproject_toml.exists():
                with open(pyproject_toml, "rb") as f:
                    self._pyproject_config = tomllib.load(f)
            else:
                self._pyproject_config = {}
        return self._pyproject_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        优先从 plugin.json 读取，如果不存在则从 pyproject.toml 读取
        
        Args:
            key: 配置键，支持点号分隔的路径，如 "project.version"
            default: 默认值
            
        Returns:
            配置值
        """
        # 先尝试从 plugin.json 读取
        value = self._get_nested(self.plugin_config, key)
        if value is not None:
            return value
        
        # 再尝试从 pyproject.toml 读取
        value = self._get_nested(self.pyproject_config, key)
        if value is not None:
            return value
        
        return default
    
    @staticmethod
    def _get_nested(data: dict, key: str) -> Any:
        """获取嵌套字典的值
        
        Args:
            data: 字典数据
            key: 键路径，如 "project.version"
            
        Returns:
            值或 None
        """
        keys = key.split(".")
        current = data
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        
        return current
    
    def get_version(self) -> str:
        """获取版本号"""
        return self.get("version") or self.get("project.version", "0.0.0")
    
    def get_name(self) -> str:
        """获取插件名称"""
        return self.get("name") or self.get("tool.plugin.name") or self.get("project.name", "unknown")
    
    def get_display_name(self) -> str:
        """获取显示名称"""
        return self.get("display_name") or self.get("tool.plugin.display_name") or self.get_name()
    
    def get_description(self) -> str:
        """获取描述"""
        return self.get("description") or self.get("project.description", "")
    
    def get_author(self) -> str:
        """获取作者"""
        author = self.get("author")
        if author:
            return author
        
        # 从 pyproject.toml 的 authors 列表获取
        authors = self.get("project.authors", [])
        if authors and isinstance(authors, list) and len(authors) > 0:
            first_author = authors[0]
            if isinstance(first_author, dict):
                return first_author.get("name", "")
        
        return ""
    
    def get_dependencies(self) -> list[str]:
        """获取依赖列表"""
        return self.get("dependencies") or self.get("project.dependencies", [])
    
    def get_entry_point(self) -> str:
        """获取入口点"""
        return self.get("entry_point") or self.get("tool.plugin.entry_point") or self.get_name()
    
    def to_plugin_json(self) -> dict[str, Any]:
        """生成 plugin.json 格式的配置
        
        Returns:
            plugin.json 格式的字典
        """
        name = self.get_name()
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "name": name,
            "display_name": self.get_display_name(),
            "version": self.get_version(),
            "description": self.get_description(),
            "author": self.get_author(),
            "license": self.get("license") or self.get("project.license.text", "AGPL-3.0"),
            "pyz_file": f"lib/{name}.pyz",
            "entry_point": self.get_entry_point(),
            "dependencies": self.get_dependencies(),
            "system_requirements": {
                "platform": self.get("system_requirements.platform") 
                           or self.get("tool.plugin.platform", "windows"),
                "min_python_version": self.get("system_requirements.min_python_version")
                                     or self.get("tool.plugin.min_python_version", "3.11"),
                "notes": self.get("system_requirements.notes", "")
            },
            "exports": self.get("exports", {})
        }


# 全局配置实例
_config: Config | None = None


def get_config(root_dir: Path | None = None) -> Config:
    """获取全局配置实例
    
    Args:
        root_dir: 项目根目录
        
    Returns:
        Config: 配置实例
    """
    global _config
    if _config is None or root_dir is not None:
        _config = Config(root_dir)
    return _config
