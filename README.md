# MaaStarResonance 插件模板

这是一个用于创建 MaaStarResonance 侧载插件的模板仓库。

## 📋 目录结构

```
MaaSR-PluginTemplate/
├── src/                          # 插件源代码目录
│   ├── __init__.py              # 模块初始化文件
│   ├── example_plugin.py        # 示例插件实现
│   └── plugin_manager.py        # 插件管理接口
├── scripts/                      # 构建和打包脚本
│   ├── build_plugin.py          # 插件构建脚本
│   ├── download_wheels.py       # 依赖下载脚本
│   └── generate_changelog.py   # 变更日志生成脚本
├── .github/workflows/           # GitHub Actions 工作流
│   └── release.yml              # 自动发布工作流
├── plugin.json                  # 插件配置文件
├── pyproject.toml              # Python 项目配置
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

### 2. 配置插件信息

编辑 `plugin.json` 文件，修改插件的基本信息：

```json
{
  "name": "your_plugin_name",
  "display_name": "你的插件名称",
  "version": "0.1.0",
  "description": "插件描述",
  "author": "你的名字",
  "license": "AGPL-3.0",
  "pyz_file": "lib/your_plugin_name.pyz",
  "entry_point": "your_plugin_name",
  "dependencies": [],
  "system_requirements": {
    "platform": "windows",
    "min_python_version": "3.11",
    "notes": ""
  },
  "exports": {
    "YourPluginClass": "your_plugin_name.YourPluginClass"
  }
}
```

### 3. 开发插件代码

在 `src/` 目录下编写你的插件代码：

```python
# src/your_plugin.py
class YourPlugin:
    def __init__(self):
        self.name = "YourPlugin"
        
    def start(self):
        print(f"{self.name} started")
        return True
```

### 4. 本地构建测试

```bash
# 安装依赖
pip install toml

# 构建插件
python scripts/build_plugin.py

# 构建结果在 dist/ 目录下
```

### 5. 发布版本

1. 更新 `plugin.json` 中的版本号
2. 提交代码并打标签：
   ```bash
   git add .
   git commit -m "feat: 新功能描述"
   git tag v0.1.0
   git push origin main --tags
   ```
3. GitHub Actions 会自动构建并发布 Release

## 📦 插件配置说明

### plugin.json 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 插件唯一标识符（英文，用于代码引用） |
| `display_name` | string | ✅ | 插件显示名称（中文，用于 UI 显示） |
| `version` | string | ✅ | 插件版本号（遵循 SemVer） |
| `description` | string | ✅ | 插件功能描述 |
| `author` | string | ✅ | 插件作者 |
| `license` | string | ✅ | 插件许可证 |
| `pyz_file` | string | ✅ | .pyz 文件相对路径 |
| `entry_point` | string | ✅ | Python 模块入口点 |
| `dependencies` | array | ❌ | 依赖的包列表 |
| `system_requirements` | object | ❌ | 系统要求 |
| `exports` | object | ✅ | 插件导出的公共 API |

### 依赖管理

在 `plugin.json` 中声明依赖：

```json
{
  "dependencies": [
    "requests>=2.31.0",
    "pillow>=10.0.0"
  ]
}
```

构建时会自动下载依赖的 wheel 文件到 `deps/` 目录。

## 🛠️ 开发指南

### 插件管理接口

模板提供了 `PluginManager` 类用于管理插件配置：

```python
from plugin_manager import get_plugin_manager

manager = get_plugin_manager()

# 获取插件信息
print(manager.get_name())
print(manager.get_version())
print(manager.get_info())

# 验证配置
is_valid, errors = manager.validate_config()
if not is_valid:
    print("配置错误:", errors)
```

### 构建脚本

#### build_plugin.py

构建插件并打包为标准格式：

```bash
# 基本用法
python scripts/build_plugin.py

# 指定输出目录
python scripts/build_plugin.py --output dist/

# 跳过依赖下载
python scripts/build_plugin.py --skip-deps

# 不创建 ZIP 压缩包
python scripts/build_plugin.py --no-zip
```

#### download_wheels.py

单独下载依赖：

```bash
# 下载依赖到 deps/ 目录
python scripts/download_wheels.py

# 指定平台和 Python 版本
python scripts/download_wheels.py --platform win_amd64 --python-version 3.13 --abi cp313
```

### 变更日志

使用 `generate_changelog.py` 自动生成 CHANGELOG：

```bash
# 生成完整 CHANGELOG
python scripts/generate_changelog.py

# 只生成最新版本
python scripts/generate_changelog.py --latest
```

## 🔄 CI/CD 工作流

### 自动发布流程

当你推送带有 `v*` 标签的提交时，GitHub Actions 会自动：

1. 构建插件
2. 生成 CHANGELOG
3. 创建 GitHub Release
4. 上传插件压缩包置

工作流文件位于 `.github/workflows/release.yml`，包含以下任务：

- **meta**: 获取版本标签
- **build**: 构建插件
- **changelog**: 生成变更日志
- **release**: 创建 GitHub Release

## 📝 最佳实践

### 版本管理

遵循语义化版本规范（SemVer）：

- `v1.0.0`: 主版本号.次版本号.修订号
- `v1.0.0-alpha`: 预发布版本
- `v1.0.0-beta.1`: 带编号的预发布版本

### 提交规范

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

### 目录结构建议

```
src/
├── __init__.py           # 导出公共 API
├── core.py              # 核心功能
├── utils.py             # 工具函数
└── config.py            # 配置管理
```

## 🔌 插件安装

### 用户安装方式

1. 从 GitHub Release 下载插件压缩包
2. 解压到 MaaStarResonance 的 `agent/plugins/` 目录
3. 重启 MaaStarResonance

### 插件目录结构

```
agent/plugins/your_plugin_name/
├── plugin.json          # 插件元数据
├── lib/
│   └── your_plugin_name.pyz  # 插件代码
└── deps/                # 依赖（如果有）
    ├── package1.whl
    └── package2.whl
```

## 🐛 故障排查

### 构建失败

1. 检查 Python 版本是否 >= 3.11
2. 确认 `plugin.json` 格式正确
3. 检查依赖是否可用

### 插件加载失败

1. 验证 `plugin.json` 配置
2. 检查依赖是否完整
3. 查看 MaaStarResonance 日志

## 📚 参考资料

- [MaaStarResonance 主项目](https://github.com/233Official/MaaStarResonance)
- [插件系统设计文档](./2026-04-11-plugin-system-design.md)
- [语义化版本规范](https://semver.org/lang/zh-CN/)
- [约定式提交](https://www.conventionalcommits.org/zh-hans/)

## 📄 许可证

本模板采用 AGPL-3.0 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意**: 这是一个模板仓库，请根据你的实际需求修改代码和配置。
