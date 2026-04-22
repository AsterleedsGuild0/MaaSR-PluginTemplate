# 🚀 快速开始

## 1. 使用模板创建新插件

1. 点击 GitHub 页面上的 "Use this template" 按钮
2. 创建你的插件仓库
3. 克隆到本地：
   ```bash
   git clone https://github.com/your-username/your-plugin-name.git
   cd your-plugin-name
   ```

**推荐安装 VSCode 扩展（可选但推荐）：**

如果你使用 VSCode 进行开发，打开项目后 VSCode 会自动提示安装推荐的扩展。点击"安装"即可一键安装所有推荐扩展，以获得更好的开发体验（包括 Python 支持、代码格式化、调试等功能）。

## 2. 配置插件信息

**只需编辑 `pyproject.toml` 文件**：

```toml
[project]
name = "your-plugin"              # 插件包名（自动推导为插件名：your_plugin）
version = "0.1.0"                 # 版本号
description = "你的插件描述"
authors = [
    { name = "你的名字", email = "your@email.com" },
]
requires-python = ">=3.13"
dependencies = [
    # 在这里添加依赖
    # "requests>=2.31.0",
]

# 插件专属配置（不填则默认从 project.name 推导）
[tool.plugin]
display_name = "你的插件"         # 显示名称
entry_point = "your_plugin"       # 入口点（对应 src/ 下的模块目录名）
```

**重要提示**：
- 所有配置都在 `pyproject.toml` 中
- 不需要手动维护 `plugin.json`（自动生成）
- 版本号只在一个地方维护
- 插件名自动从 `project.name` 推导（连字符转下划线），无需重复配置

## 3. 初始化开发环境

**配置完成后，必须运行以下命令来生成 `plugin.json` 并安装依赖：**

**方式 1：使用 VSCode 启动项（强烈推荐）**
1. 按 `F5` 或点击"运行和调试"
2. 选择 "创建/更新仓库配置"
3. 点击运行

**方式 2：命令行**
```bash
# 安装依赖并注册命令
uv sync

# 根据 pyproject.toml 生成 plugin.json（必需！）
uv run init-dev
```

**⚠️ 重要：每次修改 `pyproject.toml` 后，都需要重新运行上述命令！**

**为什么需要这样做？**
1. **uv sync**：安装/更新依赖、重新安装项目包、注册命令行入口点
2. **uv run init-dev**：从 `pyproject.toml` 读取最新配置并生成 `plugin.json`
3. **plugin.json**：插件运行时会读取这个文件获取名称、版本等元数据
4. 如果不运行这两个命令，插件代码读取到的可能是旧的配置信息

## 4. 开发插件代码

**在 `src/` 目录下编写你的插件核心代码**：

项目采用嵌套模块结构，你的插件代码应该放在 `src/your_plugin_module/` 目录下：

```python
# src/your_plugin_module/your_plugin.py
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

更新 `src/your_plugin_module/__init__.py`：

```python
from .your_plugin import YourPlugin

__all__ = ["YourPlugin"]
```

更新 `src/__main__.py` 作为插件入口：

```python
from your_plugin_module.your_plugin import YourPlugin

if __name__ == "__main__":
    plugin = YourPlugin()
    plugin.start()
```

**在插件代码中读取元数据：**

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
        plugin_info = get_runtime_config()
        self.name = plugin_info.get("display_name", "YourPlugin")
        self.version = plugin_info.get("version", "0.0.0")
        self.author = plugin_info.get("author", "")
```

## 5. 本地构建测试

**方式 1：使用 VSCode 启动项（强烈推荐）**
1. 按 `F5` 或点击"运行和调试"
2. 选择 "构建打包插件"
3. 点击运行

**方式 2：命令行**
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

**构建脚本的自动清理机制：**

打包脚本会自动执行以下清理操作，确保每次构建都是干净的：

1. **删除旧的根目录 `plugin.json`**：确保从 `pyproject.toml` 读取最新配置
2. **删除旧的插件目录**：清理 `dist/your_plugin/` 目录
3. **删除旧的 ZIP 文件**：清理同名的 `.zip` 压缩包
4. **重新生成所有文件**：基于最新配置重新创建所有输出文件

## 6. 发布版本

1. 更新 `pyproject.toml` 中的版本号
2. **使用 VSCode 启动项更新仓库配置 或者 输入如下命令**（重要！）：
   
   **方式 1：使用 VSCode 启动项（强烈推荐）**
   1. 按 `F5` 或点击"运行和调试"
   2. 选择 "创建/更新仓库配置"
   3. 点击运行

   **方式 2：命令行**
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

**注意**：
- 打标签前必须先运行 `uv sync && uv run init-dev` 更新配置
- 标签格式必须是 `v*`（如 `v1.0.0`）才会触发自动发布
- CI/CD 构建时会自动清理旧文件并从 `pyproject.toml` 读取最新配置
