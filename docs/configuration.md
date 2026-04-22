# 📦 配置说明

## 统一配置系统

本模板使用 **统一配置管理系统**：

- **主配置文件**：`pyproject.toml`（推荐）
- **自动生成**：`plugin.json`（构建时生成）
- **框架支持**：`plugin_framework/config.py`（开发时使用）

## pyproject.toml 配置项

### `[project]` 标准配置

| 配置路径                       | 类型     | 必需 | 说明                          |
|----------------------------|--------|----|-------------------------------|
| `project.name`             | string | ✅  | 项目包名（自动推导为插件名，连字符转下划线） |
| `project.version`          | string | ✅  | 版本号（SemVer）                  |
| `project.description`      | string | ✅  | 项目描述                         |
| `project.authors`          | array  | ✅  | 作者列表                         |
| `project.requires-python`  | string | ✅  | Python 版本要求                    |
| `project.dependencies`     | array  | ❌  | 依赖列表                         |

### `[tool.plugin]` 插件专属配置

仅包含 `[project]` 中无法表达的插件特有字段：

| 配置路径                       | 类型     | 必需 | 说明                                    |
|----------------------------|--------|----|---------------------------------------|
| `tool.plugin.display_name` | string | ❌  | 显示名称（默认使用插件名）                  |
| `tool.plugin.entry_point`  | string | ❌  | 入口点（默认使用插件名，对应 `src/` 下的模块目录名） |

### 自动推导规则

以下字段无需在 `[tool.plugin]` 中重复配置，会自动从 `[project]` 推导：

| plugin.json 字段       | 推导来源                  | 示例                                |
|----------------------|-------------------------|-------------------------------------|
| `name`               | `project.name`（连字符→下划线）| `example-plugin` → `example_plugin` |
| `version`            | `project.version`        | `1.0.0`                             |
| `description`        | `project.description`    |                                     |
| `author`             | `project.authors[0].name`|                                     |
| `license`            | `project.license.text`   |                                     |

## 依赖管理

在 `pyproject.toml` 中声明依赖：

```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "pillow>=10.0.0",
]
```

构建时会自动下载依赖的 wheel 文件到 `deps/` 目录。

## 配置更新工作流

**⚠️ 重要：每次修改 `pyproject.toml` 后的必要步骤**

当你修改了 `pyproject.toml` 中的任何配置（版本号、依赖、插件信息等），必须执行以下步骤：

### 方法 1：VSCode 启动项（强烈推荐）

1. 按 `F5` 或点击"运行和调试"
2. 选择 "创建/更新仓库配置"
3. 点击运行

### 方法 2：命令行

```bash
uv sync          # 同步依赖和项目配置
uv run init-dev  # 重新生成 plugin.json
```

### 为什么需要这样做？

| 命令                | 作用                                         | 不执行的后果                 |
|-------------------|--------------------------------------------|------------------------|
| `uv sync`         | 同步依赖、重新安装项目包、注册命令行入口点                      | 依赖不更新、`init-dev` 命令不可用 |
| `uv run init-dev` | 从 `pyproject.toml` 读取最新配置并生成 `plugin.json` | 插件运行时读取到旧的配置信息         |

### 典型场景

#### 1. 修改版本号

```toml
[project]
version = "1.1.0"  # 从 1.0.0 改为 1.1.0
```
→ 运行 `uv sync && uv run init-dev` → `plugin.json` 更新为 1.1.0

#### 2. 添加依赖

```toml
[project]
dependencies = [
    "requests>=2.31.0",  # 新增
]
```
→ 运行 `uv sync && uv run init-dev` → 安装 requests 并更新配置

#### 3. 修改插件信息

```toml
[tool.plugin]
display_name = "新名称"
```
→ 运行 `uv sync && uv run init-dev` → `plugin.json` 更新显示名称

## 开发依赖 vs 生产依赖

本模板支持区分开发依赖和生产依赖：

```toml
[project]
# 生产依赖：会被打包到插件中
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
# 开发依赖：仅用于本地开发，不会被打包
dev = [
    "pip>=25.3",
    "loguru>=0.7.3",
    "maafw==5.10.0",
]
```

**使用场景**：
- **生产依赖**：插件运行时必需的库
- **开发依赖**：主项目已有的库，本地开发时需要但不需要打包

**安装开发依赖**：
```bash
uv sync --all-extras
```
