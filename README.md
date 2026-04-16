# MaaStarResonance 插件模板

这是一个用于创建 MaaStarResonance 侧载插件的模板仓库。

## 📑 目录

- [✨ 主要特性](#-主要特性)
- [📋 项目结构](#-项目结构)
- [🚀 快速开始](./docs/quick-start.md)
  - [1. 使用模板创建新插件](./docs/quick-start.md#1-使用模板创建新插件)
  - [2. 配置插件信息](./docs/quick-start.md#2-配置插件信息)
  - [3. 初始化开发环境](./docs/quick-start.md#3-初始化开发环境)
  - [4. 开发插件代码](./docs/quick-start.md#4-开发插件代码)
  - [5. 本地构建测试](./docs/quick-start.md#5-本地构建测试)
  - [6. 发布版本](./docs/quick-start.md#6-发布版本)
- [🎯 VSCode 启动项说明](./docs/vscode-launch.md)
- [📦 配置说明](./docs/configuration.md)
  - [统一配置系统](./docs/configuration.md#统一配置系统)
  - [pyproject.toml 配置项](./docs/configuration.md#pyprojecttoml-配置项)
  - [依赖管理](./docs/configuration.md#依赖管理)
- [🛠️ 开发指南](./docs/development-guide.md)
  - [代码组织原则](./docs/development-guide.md#代码组织原则)
  - [使用框架功能（开发时）](./docs/development-guide.md#使用框架功能开发时)
  - [读取插件元数据](./docs/development-guide.md#读取插件元数据)
  - [构建脚本](./docs/development-guide.md#构建脚本)
  - [变更日志](./docs/development-guide.md#变更日志)
- [💡 配置更新工作流](./docs/configuration.md#配置更新工作流)
- [🔄 CI/CD 工作流](./docs/cicd.md)
- [📝 最佳实践](./docs/development-guide.md#最佳实践)
- [🔌 插件安装](./docs/installation.md)
- [🐛 故障排查](./docs/troubleshooting.md)
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
│   ├── __main__.py              # 插件入口点
│   └── maasr_plugin_example/    # 插件主模块（根据你的插件名称命名）
│       ├── __init__.py          # 模块初始化
│       ├── example_plugin.py    # 示例插件实现
│       └── utils/               # 工具模块（可选）
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
│   ├── launch.json              # 调试配置（含多个实用启动项）
│   └── tasks.json               # 任务配置
├── docs/                         # 文档目录
│   ├── quick-start.md           # 快速开始指南
│   ├── configuration.md         # 配置说明
│   ├── development-guide.md     # 开发指南
│   ├── vscode-launch.md         # VSCode 启动项说明
│   ├── cicd.md                  # CI/CD 工作流
│   ├── installation.md          # 插件安装指南
│   └── troubleshooting.md       # 故障排查
├── pyproject.toml              # 项目配置（主配置文件）
├── plugin.json                  # 插件元数据（自动生成，不要手动编辑）
└── README.md                    # 本文档
```

## 📄 许可证

本模板采用 AGPL-3.0 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意**: 这是一个模板仓库，请根据实际需求修改。
