# MaaStarResonance 插件模板

这是一个用于创建 MaaStarResonance 侧载插件的模板仓库。

## 📑 目录

- [✨ 主要特性](#-主要特性)
- [📋 项目结构](#-项目结构)
- [🚀 快速开始](#-快速开始)
  - [1. 使用模板创建新插件](#1-使用模板创建新插件)
  - [2. 配置插件信息](#2-配置插件信息)
  - [3. 初始化开发环境](#3-初始化开发环境)
  - [4. 开发插件代码](#4-开发插件代码)
  - [5. 本地构建测试](#5-本地构建测试)
  - [6. 发布版本](#6-发布版本)
- [📦 配置说明](#-配置说明)
  - [统一配置系统](#统一配置系统)
  - [pyproject.toml 配置项](#pyprojecttoml-配置项)
  - [依赖管理](#依赖管理)
- [🛠️ 开发指南](#️-开发指南)
  - [代码组织原则](#代码组织原则)
  - [使用框架功能（开发时）](#使用框架功能开发时)
  - [读取插件元数据](#读取插件元数据)
  - [构建脚本](#构建脚本)
  - [变更日志](#变更日志)
- [💡 配置更新工作流](#-配置更新工作流)
- [🔄 CI/CD 工作流](#-cicd-工作流)
- [📝 最佳实践](#-最佳实践)
- [🔌 插件安装](#-插件安装)
- [🐛 故障排查](#-故障排查)
- [📄 许可证](#-许可证)
- [🤝 贡献](#-贡献)

## ✨ 主要特性

- **清晰的代码结构** - 插件代码与框架代码完全分离
- **统一配置管理** - 使用 `pyproject.toml` 作为单一配置源
- **自动元数据生成** - 自动生成 `plugin.json`，支持运行时读取
- **自动构建** - 一键打包为标准插件格式
- **GitHub Actions** - 自动发布和版本管理
- **完整文档** - 详细的开发指南和示例

## 📋 项目结构

```
MaaSR-PluginTemplate/
├── src/                          # 插件核心代码（会被打包）
│   ├── __init__.py              # 模块初始化
│   ├── __main__.py              # 插件入口点
│   └── example_plugin.py        # 示例插件实现
├── plugin_framework/             # 插件框架（开发时使用，不打包）
│   ├── __init__.py              # 框架初始化
│   ├── config.py                # 统一配置管理
│   └── plugin_manager.py        # 插件管理接口
├── scripts/                      # 构建和打包脚本
│   ├── __init__.py              # 包初始化
│   ├── build_plugin.py          # 插件构建脚本
│   ├── download_wheels.py       # 依赖下载脚本
│   ├── generate_changelog.py   # 变更日志生成脚本
│   └── init_dev.py              # 仓库配置初始化脚本
├── .github/workflows/           # GitHub Actions 工作流
│   └── release.yml              # 自动发布工作流
├── .vscode/                      # VSCode 配置
│   ├── launch.json              # 调试配置（含创建/更新仓库配置启动项）
│   └── tasks.json               # 任务配置
├── pyproject.toml              # 项目配置（主配置文件）
├── plugin.json                  # 插件元数据（自动生成，不要手动编辑）
└── README.md                    # 本文档
```

## 🚀 快速开始

### 1. 使用模板创建新插件

1. 点击 GitHub 页面上的 "Use this template" 按钮
2. 创建你的插件仓库
3. 克隆到本地：
   ```bash
   git clone https://github.com/your-username/your-plugin-name.git
   cd your-plugin-name
   ```

**推荐安装 VSCode 扩展（可选但推荐）：**

如果你使用 VSCode 进行开发，打开项目后 VSCode 会自动提示安装推荐的扩展。点击"安装"即可一键安装所有推荐扩展，以获得更好的开发体验（包括 Python 支持、代码格式化、调试等功能）。

### 2. 配置插件信息

**只需编辑 `pyproject.toml` 文件**：

```toml
[project]
name = "your-plugin"              # 插件包名
version = "0.1.0"                 # 版本号
description = "你的插件描述"
authors = [
    { name = "你的名字", email = "your@email.com" },
]
dependencies = [
    # 在这里添加依赖
    # "requests>=2.31.0",
]

[tool.plugin]
name = "your_plugin"              # 插件模块名（Python 标识符）
display_name = "你的插件"         # 显示名称
entry_point = "your_plugin"       # 入口点
```

**重要提示**：
- 所有配置都在 `pyproject.toml` 中
- 不需要手动维护 `plugin.json`（自动生成）
- 版本号只在一个地方维护

### 3. 初始化开发环境

**配置完成后，必须运行以下命令来生成 `plugin.json` 并安装依赖：**

```bash
# 安装依赖并注册命令
uv sync

# 根据 pyproject.toml 生成 plugin.json（必需！）
uv run init-dev
```

**或者在 VSCode 中（推荐）：**
1. 按 `F5` 或点击"运行和调试"
2. 选择 "创建/更新仓库配置 (uv sync + init-dev)"
3. 点击运行

**或者使用 VSCode 任务：**
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Tasks: Run Task"
3. 选择 "uv sync + init-dev"

**⚠️ 重要：每次修改 `pyproject.toml` 后，都需要重新运行上述命令！**

**为什么需要这样做？**
1. **uv sync**：安装/更新依赖、重新安装项目包、注册命令行入口点
2. **uv run init-dev**：从 `pyproject.toml` 读取最新配置并生成 `plugin.json`
3. **plugin.json**：插件运行时会读取这个文件获取名称、版本等元数据
4. 如果不运行这两个命令，插件代码读取到的可能是旧的配置信息

### 4. 开发插件代码

**在 `src/` 目录下编写你的插件核心代码**：

```python
# src/your_plugin.py
class YourPlugin:
    """你的插件类"""
    
    def __init__(self):
        self.name = "YourPlugin"
        
    def start(self):
        """启动插件"""
        print(f"{self.name} started")
        return True
    
    def execute(self):
        """执行插件主要功能"""
        # 实现你的业务逻辑
        pass
```

更新 `src/__init__.py`：

```python
from .your_plugin import YourPlugin

__all__ = ["YourPlugin"]
```

**在插件代码中读取元数据：**

```python
# src/your_plugin.py
import sys
from pathlib import Path

# 添加 plugin_framework 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "plugin_framework"))

from config import get_runtime_config

class YourPlugin:
    def __init__(self):
        # 从 plugin.json 读取元数据
        plugin_info = get_runtime_config()
        self.name = plugin_info.get("display_name", "YourPlugin")
        self.version = plugin_info.get("version", "0.0.0")
        self.author = plugin_info.get("author", "")
```

### 5. 本地构建测试

```bash
# 构建插件
python scripts/build_plugin.py

# 构建结果在 dist/ 目录下
# dist/your_plugin/
# ├── plugin.json          # 自动生成
# ├── lib/
# │   └── your_plugin.pyz  # 只包含 src/ 的代码
# └── deps/                # 依赖（如果有）

# 同时会在根目录更新 plugin.json（开发用）
```

### 6. 发布版本

1. 更新 `pyproject.toml` 中的版本号
2. **运行配置更新命令**（重要！）：
   ```bash
   uv sync
   uv run init-dev
   ```
3. 提交代码并打标签：
   ```bash
   git add .
   git commit -m "feat: 新功能描述"
   git tag v0.1.0
   git push origin main --tags
   ```
4. GitHub Actions 会自动构建并发布 Release

## 📦 配置说明

### 统一配置系统

本模板使用 **统一配置管理系统**：

- **主配置文件**：`pyproject.toml`（推荐）
- **自动生成**：`plugin.json`（构建时生成）
- **框架支持**：`plugin_framework/config.py`（开发时使用）

### pyproject.toml 配置项

| 配置路径 | 类型 | 必需 | 说明 |
|---------|------|------|------|
| `project.name` | string | ✅ | 项目包名 |
| `project.version` | string | ✅ | 版本号（SemVer） |
| `project.description` | string | ✅ | 项目描述 |
| `project.authors` | array | ✅ | 作者列表 |
| `project.dependencies` | array | ❌ | 依赖列表 |
| `tool.plugin.name` | string | ✅ | 插件模块名 |
| `tool.plugin.display_name` | string | ❌ | 显示名称 |
| `tool.plugin.entry_point` | string | ❌ | 入口点 |

### 依赖管理

在 `pyproject.toml` 中声明依赖：

```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "pillow>=10.0.0",
]
```

构建时会自动下载依赖的 wheel 文件到 `deps/` 目录。

## 🛠️ 开发指南

### 代码组织原则

1. **src/** - 只放插件核心代码
   - ✅ 业务逻辑
   - ✅ 数据处理
   - ✅ 算法实现
   - ❌ 配置管理
   - ❌ 构建脚本
   - ❌ 框架代码

2. **plugin_framework/** - 框架和工具代码
   - ✅ 配置管理（`config.py`）
   - ✅ 插件管理（`plugin_manager.py`）
   - ✅ 开发时使用的工具代码
   - ❌ 不会被打包到插件中

3. **scripts/** - 构建和工具脚本
   - ✅ 构建脚本
   - ✅ 依赖管理
   - ✅ 变更日志生成

### 使用框架功能（开发时）

如果需要在开发时使用配置管理等功能：

```python
# 在测试脚本或开发工具中使用
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "plugin_framework"))

from config import get_config
from plugin_manager import get_plugin_manager

# 获取配置
config = get_config()
print(f"插件: {config.get_name()} v{config.get_version()}")

# 使用插件管理器
manager = get_plugin_manager()
info = manager.get_info()
```

**注意**：框架代码不会被打包到插件中，只在开发时使用。

### 读取插件元数据

插件运行时可以通过 `get_runtime_config()` 读取 `plugin.json` 中的元数据：

```python
# src/your_plugin.py
import sys
from pathlib import Path

# 添加 plugin_framework 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "plugin_framework"))

from config import get_runtime_config

class YourPlugin:
    def __init__(self):
        # 从 plugin.json 读取元数据
        try:
            plugin_info = get_runtime_config()
            self.name = plugin_info.get("display_name", "YourPlugin")
            self.version = plugin_info.get("version", "0.0.0")
            self.description = plugin_info.get("description", "")
            self.author = plugin_info.get("author", "")
        except FileNotFoundError as e:
            # 如果找不到 plugin.json，使用默认值
            print(f"[WARNING] {e}")
            self.name = "YourPlugin"
            self.version = "0.0.0"
```

**工作原理：**
- **开发环境**：从仓库根目录读取 `plugin.json`
- **部署环境**：从 `.pyz` 文件向上两级读取 `plugin.json`
- 自动检测运行环境，无需手动配置路径

### 构建脚本

#### build_plugin.py

```bash
# 基本用法（自动从 pyproject.toml 读取配置）
python scripts/build_plugin.py

# 指定输出目录
python scripts/build_plugin.py --output dist/

# 跳过依赖下载
python scripts/build_plugin.py --skip-deps

# 不创建 ZIP 压缩包
python scripts/build_plugin.py --no-zip
```

#### download_wheels.py

```bash
# 下载依赖到 deps/ 目录
python scripts/download_wheels.py

# 指定平台和 Python 版本
python scripts/download_wheels.py --platform win_amd64 --python-version 3.13
```

### 变更日志

使用 `generate_changelog.py` 自动生成 CHANGELOG：

```bash
# 生成完整 CHANGELOG
python scripts/generate_changelog.py

# 只生成最新版本
python scripts/geangelog.py --latest
```

## 🔄 CI/CD 工作流

### 自动发布流程

当你推送带有 `v*` 标签的提交时，GitHub Actions 会自动：

1. 从 `pyproject.toml` 读取配置
2. 构建插件（只打包 `src/` 目录）
3. 生成 CHANGELOG
4. 创建 GitHub Release
5. 上传插件压缩包

工作流文件位于 `.github/workflows/release.yml`。

## 💡 配置更新工作流

**⚠️ 重要：每次修改 `pyproject.toml` 后的必要步骤**

当你修改了 `pyproject.toml` 中的任何配置（版本号、依赖、插件信息等），必须执行以下步骤：

### 方法 1：命令行（推荐）

```bash
uv sync          # 同步依赖和项目配置
uv run init-dev  # 重新生成 plugin.json
```

### 方法 2：VSCode 启动项

1. 按 `F5` 或点击"运行和调试"
2. 选择 "创建/更新仓库配置 (uv sync + init-dev)"
3. 点击运行

### 方法 3：VSCode 任务

1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Tasks: Run Task"
3. 选择 "uv sync + init-dev"

### 为什么需要这样做？

| 命令 | 作用 | 不执行的后果 |
|------|------|-------------|
| `uv sync` | 同步依赖、重新安装项目包、注册命令行入口点 | 依赖不更新、`init-dev` 命令不可用 |
| `uv run init-dev` | 从 `pyproject.toml` 读取最新配置并生成 `plugin.json` | 插件运行时读取到旧的配置信息 |

**典型场景：**

1. **修改版本号**：
   ```toml
   [project]
   version = "1.1.0"  # 从 1.0.0 改为 1.1.0
   ```
   → 运行 `uv sync && uv run init-dev` → `plugin.json` 更新为 1.1.0

2. **添加依赖**：
   ```toml
   [project]
   dependencies = [
       "requests>=2.31.0",  # 新增
   ]
   ```
   → 运行 `uv sync && uv run init-dev` → 安装 requests 并更新配置

3. **修改插件信息**：
   ```toml
   [tool.plugin]
   display_name = "新名称"
   ```
   → 运行 `uv sync && uv run init-dev` → `plugin.json` 更新显示名称

## 🔄 CI/CD 工作流

### 自动发布流程

当你推送带有 `v*` 标签的提交时，GitHub Actions 会自动：

1. 从 `pyproject.toml` 读取配置
2. 构建插件（只打包 `src/` 目录）
3. 生成 CHANGELOG
4. 创建 GitHub Release
5. 上传插件压缩包

工作流文件位于 `.github/workflows/release.yml`。

## 📝 最佳实践

### 1. 保持 src/ 简洁

```python
# ✅ 好的做法 - src/my_plugin.py
class MyPlugin:
    def __init__(self):
        self.name = "MyPlugin"
    
    def execute(self):
        # 业务逻辑
        pass

# ❌ 不好的做法 - 不要在 src/ 中导入框架代码
from config import get_config  # 这是框架代码，不应该在 src/ 中
```

### 2. 使用框架功能（开发时）

```python
# ✅ 在测试脚本或开发工具中使用框架
# tests/test_plugin.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "plugin_framework"))

from config import get_config
from plugin_manager import get_plugin_manager

def test_plugin_config():
    config = get_config()
    assert config.get_name() == "my_plugin"
```

### 3. 版本管理

只在 `pyproject.toml` 中维护版本号：

```toml
[project]
version = "1.0.0"  # 只在这里修改版本号
```

## 🔌 插件安装

1. 从 GitHub Release 下载插件压缩包
2. 解压到 MaaStarResonance 的 `agent/plugins/` 目录
3. 重启 MaaStarResonance

### 插件目录结构

```
agent/plugins/your_plugin/
├── plugin.json          # 插件元数据（自动生成）
├── lib/
│   └── your_plugin.pyz  # 只包含 src/ 的代码
└── deps/                # 依赖（如果有）
    └── *.whl
```

## 🐛 故障排查

### 构建失败

1. 检查 Python 版本是否 >= 3.11
2. 确认 `pyproject.toml` 格式正确
3. 检查依赖是否可用

### 插件加载失败

1. 验证 `pyproject.toml` 配置
2. 检查依赖是否完整
3. 查看 MaaStarResonance 日志

## 📄 许可证

本模板采用 AGPL-3.0 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意**: 这是一个模板仓库，请根据实际需求修改。
