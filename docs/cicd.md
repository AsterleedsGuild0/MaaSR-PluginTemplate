# 🔄 CI/CD 工作流

## 自动发布流程

当你推送带有 `v*` 标签的提交时，GitHub Actions 会自动：

1. 从 `pyproject.toml` 读取配置
2. 构建插件（只打包 `src/` 目录）
3. 生成 CHANGELOG
4. 创建 GitHub Release
5. 上传插件压缩包

工作流文件位于 `.github/workflows/release.yml`。

## 触发条件

自动发布会在以下情况触发：

- 推送标签格式为 `v*`（例如：`v1.0.0`, `v2.1.3`）
- 标签必须符合语义化版本规范（SemVer）

## 发布步骤

### 1. 更新版本号

编辑 `pyproject.toml`：

```toml
[project]
version = "1.0.0"  # 更新版本号
```

### 2. 更新配置

**方式 1：使用 VSCode 启动项（强烈推荐）**
1. 按 `F5` 或点击"运行和调试"
2. 选择 "创建/更新仓库配置"
3. 点击运行

**方式 2：命令行**
```bash
uv sync
uv run init-dev
```

### 3. 提交并打标签

```bash
# 提交更改
git add .
git commit -m "chore: bump version to 1.0.0"

# 创建标签
git tag v1.0.0

# 推送到远程（包括标签）
git push origin main --tags
```

### 4. 等待自动构建

GitHub Actions 会自动：
- 检出代码
- 设置 Python 环境
- 安装依赖
- 构建插件
- 生成 CHANGELOG
- 创建 Release
- 上传构建产物

## 工作流配置

`.github/workflows/release.yml` 的主要配置：

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Build plugin
        run: |
          pip install uv
          uv sync
          uv run init-dev
          python scripts/build_plugin.py
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*.zip
```

## 注意事项

1. **版本号一致性**：确保 `pyproject.toml` 中的版本号与 Git 标签一致
2. **配置更新**：打标签前必须运行 `uv sync && uv run init-dev`
3. **标签格式**：必须以 `v` 开头（如 `v1.0.0`）
4. **权限设置**：确保 GitHub Actions 有创建 Release 的权限

## 手动触发构建

如果需要手动触发构建，可以在 GitHub Actions 页面手动运行工作流（需要在 workflow 文件中添加 `workflow_dispatch` 触发器）。

## 故障排查

### 构建失败

1. 检查 GitHub Actions 日志
2. 确认 `pyproject.toml` 格式正确
3. 验证依赖是否可用
4. 检查 Python 版本兼容性

### Release 未创建

1. 确认标签格式正确（`v*`）
2. 检查 GitHub Actions 权限
3. 查看工作流日志中的错误信息

### 构建产物缺失

1. 确认 `build_plugin.py` 执行成功
2. 检查 `dist/` 目录是否生成
3. 验证 ZIP 文件是否创建
