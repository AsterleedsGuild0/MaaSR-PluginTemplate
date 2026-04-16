# 🎯 VSCode 启动项说明

本项目已配置多个实用的 VSCode 启动项，**强烈推荐使用启动项来执行常用脚本**，比命令行更方便快捷。

## 如何使用启动项

1. 按 `F5` 或点击左侧"运行和调试"图标
2. 在顶部下拉菜单中选择对应的启动项
3. 点击绿色播放按钮或按 `F5` 运行

## 可用的启动项

| 启动项名称                 | 功能说明                             | 使用场景                      |
|-----------------------|----------------------------------|---------------------------|
| **Python 调试程序: 当前文件** | 调试当前打开的 Python 文件                | 开发调试单个 Python 脚本          |
| **创建/更新仓库配置**         | 执行 `uv sync` + `uv run init-dev` | 修改 `pyproject.toml` 后必须运行 |
| **构建打包插件**            | 执行 `build_plugin.py`             | 构建插件发布包                   |
| **下载依赖**              | 执行 `download_wheels.py`          | 下载插件依赖的 wheel 文件          |
| **生成完整 CHANGELOG**    | 执行 `generate_changelog.py`       | 生成变更日志文档                  |

## 推荐工作流

1. **初次配置或修改配置后**：运行 "创建/更新仓库配置"
2. **开发过程中**：使用 "Python 调试程序: 当前文件" 调试代码
3. **准备发布前**：依次运行 "构建打包插件" → "生成完整 CHANGELOG"

## 启动项配置详情

所有启动项配置位于 `.vscode/launch.json` 文件中，你可以根据需要自定义参数。

### 创建/更新仓库配置

```json
{
  "name": "创建/更新仓库配置",
  "type": "PowerShell",
  "request": "launch",
  "script": "uv sync --all-extras; if ($?) { uv run init-dev }",
  "cwd": "${workspaceFolder}"
}
```

这个启动项会依次执行：
1. `uv sync --all-extras` - 同步所有依赖（包括可选依赖）
2. `uv run init-dev` - 生成 `plugin.json`

### 构建打包插件

```json
{
  "name": "构建打包插件",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/scripts/build_plugin.py",
  "console": "integratedTerminal",
  "args": []
}
```

可以通过修改 `args` 数组添加命令行参数，例如：
```json
"args": ["--skip-deps", "--no-zip"]
```

### 下载依赖

```json
{
  "name": "下载依赖",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/scripts/download_wheels.py",
  "console": "integratedTerminal",
  "args": [
    "--platform", "win_amd64",
    "--python-version", "3.13",
    "--abi", "cp313"
  ]
}
```

已预配置为 Windows 平台和 Python 3.13，可根据需要修改参数。

### 生成完整 CHANGELOG

```json
{
  "name": "生成完整 CHANGELOG",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/scripts/generate_changelog.py",
  "console": "integratedTerminal",
  "envFile": "${workspaceFolder}/.env.local",
  "args": ["--output", "${workspaceFolder}/CHANGELOG.md"]
}
```

如果需要 GitHub Token，可以在 `.env.local` 文件中配置：
```
GITHUB_TOKEN=your_token_here
```
