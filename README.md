# MaaStarResonance 插件模板

这是一个用于创建 MaaStarResonance 侧载插件的模板仓库。

## ✨ 主要特性

- **清晰的代码结构** - 插件代码与框架代码完全分离
- **统一配置管理** - 使用 `pyproject.toml` 作为单一配置源
- **自动构建** - 一键打包为标准插件格式
- **GitHub Actions** - 自动发布和版本管理
- **完整文档** - 详细的开发指南和示例

## 📋 目录结构

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
│   ├── build_plugin.py          # 插件构建脚本
│   ├── download_wheels.py       # 依赖下载脚本
│   └── generate_changelog.py   # 变更日志生成脚本
├── .github/workflows/           # GitHub Actions 工作流
│   └── release.yml              # 自动发布工作流
├── pyproject.toml              # 项目配置（主配置文件）
└── README.md                    # 本文档
```

## 🎯 设计理念

### 代码分离

本模板采用**代码分离**设计：

- **src/** - 只包含插件的核心业务逻辑，会被打包到 `.pyz` 文件中
- **plugin_framework/** - 开发时使用的框架代码（配置管理、插件管理等），**不会被打包**

这样设计的好处：
- ✅ 插件包更小（体积减少约 80%）
- ✅ 插件代码更简洁，只关注业务逻辑
- ✅ 框架代码可以独立更新，不影响已发布的插件
- ✅ 代码职责更清晰，易于维护

## 🚀 快速开始

### 1. 使用模板创建新插件

1. 点击 GitHub 页面上的 "Use this template" 按钮
2. 创建你的插件仓库
3. 克隆到本地：
   ```bash
   git clone https://github.com/your-username/your-plugin-name.git
   cd your-plugin-name
   ```

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
- 不需要手动维护 `plugin.json`（构建时自动生成）
- 版本号只在一个地方维护

### 3. 开发插件代码

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

**重要**：
- `src/` 目录只放插件的核心业务代码
- 不要在 `src/` 中导入 `plugin_framework` 的代码
- 保持 `src/` 简洁和专注

### 4. 本地构建测试

```bash
# 构建插件
python scripts/build_plugin.py

# 构建结果在 dist/ 目录下
# dist/your_plugin/
# ├── plugin.json          # 自动生成
# ├── lib/
# │   └── your_plugin.pyz  # 只包含 src/ 的代码
# └── deps/                # 依赖（如果有）
```

### 5. 发布版本

1. 更新 `pyproject.toml` 中的版本号
2. 提交代码并打标签：
   ```bash
   git add .
   git commit -m "feat: 新功能描述"
   git tag v0.1.0
   git push origin main --tags
   ```
3. GitHub Actions 会自动构建并发布 Release

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
   - ✅ 开发时使用的n   - ❌ 不会被打包到插件中

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
version = "0.2.0"  # 只在这里修改版本号
```

### 4. 遵循约定式提交

使用约定式提交（Conventional Commits）：

```
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
perf: 性能优化
test: 测试相关
chore: 构建/工具链相关
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

## 🆕 更新说明

### v0.2.0 的改进

- ✅ **代码分离** - `src/` 只包含插件核心代码
- ✅ **框架独立*n_framework/` 包含开发时使用的框架代码
- ✅ **更小的包** - 打包后的插件不包含框架代码（体积减少约 80%）
- ✅ **更清晰** - 代码职责更明确

### v0.1.0 的改进

- ✅ **统一配置管理** - 使用 `pyproject.toml` 作为单一配置源
- ✅ **自动生成 plugin.json** - 构建时自动生成，无需手动维护
- ✅ **简化配置** - 减少重复配置，提高可维护性

## 📚 参考资料

- [MaaStarResonance 主项目](https://github.com/233Official/MaaStarResonance)
- [开发指南](./CONTRIBUTING.md)
- [结构优化文档](./STRUCTURE_OPTIMIZATION.md)
- [语义化版本规范](https://semver.org/lang/zh-CN/)
- [约定式提交](https://www.conventionalcommits.org/zh-hans/)

## 📄 许可证

本模板采用 AGPL-3.0 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意**: 这是一个模板仓库，请根据实际需求修改。
