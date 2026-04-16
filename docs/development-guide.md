# 🛠️ 开发指南

## 代码组织原则

### 1. src/ - 只放插件核心代码

- ✅ 业务逻辑
- ✅ 数据处理
- ✅ 算法实现
- ❌ 配置管理
- ❌ 构建脚本
- ❌ 框架代码

### 2. plugin_framework/ - 框架和工具代码

- ✅ 配置管理（`config.py`）
- ✅ 插件管理（`plugin_manager.py`）
- ✅ 开发时使用的工具代码
- ❌ 不会被打包到插件中

### 3. scripts/ - 构建和工具脚本

- ✅ 构建脚本
- ✅ 依赖管理
- ✅ 变更日志生成

## 使用框架功能（开发时）

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

## 读取插件元数据

插件运行时可以通过 `get_runtime_config()` 读取 `plugin.json` 中的元数据：

```python
# src/your_plugin_module/your_plugin.py
import sys
from pathlib import Path

# 添加 plugin_framework 到路径（向上两级到项目根目录）
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "plugin_framework"))

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

## 构建脚本

### build_plugin.py

**方式 1：使用 VSCode 启动项（强烈推荐）**
1. 按 `F5` 或点击"运行和调试"
2. 选择 "构建打包插件"
3. 点击运行

**方式 2：命令行**
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

**构建流程说明：**

1. **自动清理**：
   - 删除根目录的旧 `plugin.json`，确保从 `pyproject.toml` 读取最新配置
   - 删除 `dist/` 目录下的旧插件目录
   - 删除同名的旧 ZIP 压缩包

2. **配置读取**：
   - 从 `pyproject.toml` 读取所有配置信息
   - 自动生成符合规范的 `plugin.json`

3. **代码打包**：
   - 将 `src/` 目录打包为 `.pyz` 文件
   - 只包含插件核心代码，不包含框架代码

4. **依赖处理**：
   - 下载依赖的 wheel 文件到 `deps/` 目录
   - 可使用 `--skip-deps` 跳过

5. **输出文件**：
   - 在 `dist/your_plugin/` 生成插件目录（部署用）
   - 在根目录生成 `plugin.json`（开发用）
   - 创建 ZIP 压缩包（可选）

### download_wheels.py

**方式 1：使用 VSCode 启动项（强烈推荐）**
1. 按 `F5` 或点击"运行和调试"
2. 选择 "下载依赖"
3. 点击运行（已预配置 Windows 平台和 Python 3.13）

**方式 2：命令行**
```bash
# 下载依赖到 deps/ 目录
python scripts/download_wheels.py

# 指定平台和 Python 版本
python scripts/download_wheels.py --platform win_amd64 --python-version 3.13
```

## 变更日志

使用 `generate_changelog.py` 自动生成 CHANGELOG：

**方式 1：使用 VSCode 启动项（强烈推荐）**
1. 按 `F5` 或点击"运行和调试"
2. 选择 "生成完整 CHANGELOG"
3. 点击运行

**方式 2：命令行**
```bash
# 生成完整 CHANGELOG
python scripts/generate_changelog.py

# 只生成最新版本
python scripts/generate_changelog.py --latest
```

## 最佳实践

### 1. 保持 src/ 简洁

```python
# ✅ 好的做法 - src/my_plodule/my_plugin.py
class MyPlugin:
    def __init__(self):
        self.name = "MyPlugin"
    
    def execute(self):
        # 业务逻辑
        pass

# ❌ 不好的做法 - 不要在 src/ 中直接导入框架代码
from config import get_config  # 这是框架代码，需要通过 sys.path 添加后才能使用
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

### 4. 模块结构

采用嵌套模块结构，便于组织复杂插件：

```
src/
├── __main__.py              # 插件入口
└── your_plugin_module/      # 主模块
    ├── __init__.py
    ├── core.py              # 核心功能
    ├── utils/               # 工具模块
    │   ├── __init__.py
    │   └── helpers.py
    └── handlers/            # 处理器模块
        ├── __init__.py
        └── event_handler.py
```

### 5. 错误处理

在插件代码中添加适当的错误处理：

```python
class YourPlugin:
    def __init__(self):
        try:
            plugin_info = get_runtime_config()
            self.name = plugin_info.get("display_name", "YourPlugin")
        except FileNotFoundError:
            # 使用默认值
            self.name = "YourPlugin"
        except Exception as e:
            # 记录错误
            print(f"[ERROR] Failed to load config: {e}")
  aise
```
