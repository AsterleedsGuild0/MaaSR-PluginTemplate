# 开发指南

本文档提供插件开发的详细指南和最佳实践。

## 环境准备

### 必需工具

- Python 3.11+
- Git
- pip

### 推荐工具

- VS Code 或 PyCharm
- Python 虚拟环境管理工具（venv/conda）

## 开发流程

### 1. 初始化开发环境

```bash
# 克隆仓库
git clone https://github.com/your-username/your-plugin.git
cd your-plugin

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装开发依赖
pip install -r requirements-dev.txt  # 如果有的话
```

### 2. 编写插件代码

在 `src/` 目录下创建你的插件模块：

```python
# src/my_plugin.py
from typing import Any

class MyPlugin:
    """我的插件类"""
    
    def __init__(self):
        self.name = "MyPlugin"
        self.version = "0.1.0"
    
    def initialize(self) -> bool:
        """初始化插件"""
        print(f"初始化 {self.name} v{self.version}")
        return True
    
    def execute(self, *args, **kwargs) -> Any:
        """执行插件主要功能"""
        # 实现你的逻辑
        pass
    
    def cleanup(self) -> None:
        """清理资源"""
        pass
```

### 3. 更新配置文件

编辑 `plugin.json`：

```json
{
  "name": "my_plugin",
  "display_name": "我的插件",
  "version": "0.1.0",
  "description": "插件功能描述",
  "author": "你的名字",
  "license": "AGPL-3.0",
  "pyz_file": "lib/my_plugin.pyz",
  "entry_point": "my_plugin",
  "dependencies": [
    "requests>=2.31.0"
  ],
  "system_requirements": {
    "platform": "windows",
    "min_python_version": "3.11",
    "notes": "需要网络连接"
  },
  "exports": {
    "MyPlugin": "my_plugin.MyPlugin"
  }
}
```

### 4. 本地测试

```bash
# 构建插件
python scripts/build_plugin.py

# 检查构建结果
ls dist/
```

### 5. 提交代码

```bash
git add .
git commit -m "feat: 添加新功能"
git push origin main
```

## 插件 API 设计

### 基本接口

建议实现以下标准接口：

```python
class PluginInterface:
    """插件标准接口"""
    
    def initialize(self) -> bool:
        """初始化插件，返回是否成功"""
        pass
    
    def get_info(self) -> dict:
        """获取插件信息"""
        pass
    
    def execute(self, *args, **kwargs):
        """执行主要功能"""
        pass
    
    def cleanup(self) -> None:
        """清理资源"""
        pass
```

### 配置管理

使用 `PluginManager` 管理配置：

```python
from plugin_manager import get_plugin_manager

class MyPlugin:
    def __init__(self):
        self.manager = get_plugin_manager()
        self.config = self.manager.config
        self.version = self.manager.get_version()
```

## 依赖管理

### 添加依赖

在 `plugin.json` 中声明：

```json
{
  "dependencies": [
    "requests>=2.31.0",
    "pillow>=10.0.0",
    "numpy>=1.24.0"
  ]
}
```

### 本地测试依赖

```bash
# 下载依赖到 deps/
python scripts/download_wheels.py

# 安装依赖到虚拟环境
pip install -r requirements.txt
```

## 测试

### 单元测试

创建 `tests/` 目录：

```python
# tests/test_my_plugin.py
import unittest
from src.my_plugin import MyPlugin

class TestMyPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = MyPlugin()
    
    def test_initialize(self):
        self.assertTrue(self.plugin.initialize())
    
    def test_get_info(self):
        info = self.plugin.get_info()
        self.assertIn("name", info)
        self.assertIn("version", info)

if __name__ == "__main__":
    unittest.main()
```

运行测试：

```bash
python -m unittest discover tests
```

## 调试技巧

### 日志记录

```python
import logging

logger = logging.getLogger(__name__)

class MyPlugin:
    def execute(self):
        logger.info("开始执行插件")
        try:
            # 你的代码
            logger.debug("执行详细信息")
        except Exception as e:
            logger.error(f"执行失败: {e}")
```

### 断点调试

在 VS Code 中配置 `.vscode/launch.jsonn```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: 当前文件",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: 构建插件",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/build_plugin.py",
      "console": "integratedTerminal"
    }
  ]
}
```

## 性能优化

### 延迟加载

```python
class MyPlugin:
    def __init__(self):
        self._heavy_resource = None
    
    @property
    def heavy_resource(self):
        if self._heavy_resource is None:
            self._heavy_resource = self._load_heavy_resource()
        return self._heavy_resource
```

### 缓存

```python
from functools import lru_cache

class MyPlugin:
    @lru_cache(maxsize=128)
    def expensive_operation(self, param):
        # 耗时操作
        pass
```

## 发布流程

### 1. 更新版本号

编辑 `plugin.json`：

```json
{
  "version": "0.2.0"
}
```

### 2. 更新 CHANGELOG

```markdown
## [0.2.0] - 2026-04-12

### 新增
- 添加新功能 X
- 支持配置项 Y

### 修复
- 修复 Bug Z
```

### 3. 创建标签

```bash
git add .
git commit -m "chore: bump version to 0.2.0"
git tag v0.2.0
git push origin main --tags
```

### 4. 等待自动发布

GitHub Actions 会自动：
- 构建插件
- 生成 CHANGELOG
- 创建 Release
- 上传构建产物

## 常见问题

### Q: 如何添加系统依赖？

A: 在 `plugin.json` 的 `system_requirements.notes` 中说明：

```json
{
  "system_requirements": {
    "notes": "需要安装 Visual C++ Redistributable"
  }
}
```

### Q: 如何处理跨平台兼容性？

A: 使用 `platform` 模块检测系统：

```python
import platform

class MyPlugin:
    def __init__(self):
        self.os = platform.system()  # 'Windows', 'Linux', 'Dar    
    def execute(self):
        if self.os == "Windows":
            # Windows 特定代码
            pass
        elif self.os == "Linux":
            # Linux 特定代码
            pass
```

### Q: 如何调试 GitHub Actions？

A: 在工作流中添加调试步骤：

```yaml
- name: Debug
  run: |
    ls -la
    python --version
    pip list
```

## 参考资源

- [Python 打包指南](https://packaging.python.org/)
- [GitHub Actions 文档](https://docs.github.com/actions)
- [语义化版本规范](https://semver.org/)

---

有问题？欢迎提交 Issue！
