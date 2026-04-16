# 🐛 故障排查

## 构建失败

### 问题：Python 版本不兼容

**症状**：
```
ERROR: Python version mismatch
```

**解决方案**：
1. 检查 Python 版本是否 >= 3.11
   ```bash
   python --version
   ```
2. 如果版本过低，升级 Python
3. 确认 `pyproject.toml` 中的 `requires-python` 设置正确

### 问题：pyproject.toml 格式错误

**症状**：
```
ERROR: Failed to parse pyproject.toml
```

**解决方案**：
1. 使用 TOML 验证工具检查格式
2. 确认所有字符串使用引号
3. 检查数组和表的语法是否正确

### 问题：依赖不可用

**症状**：
```
ERROR: Could not find a version that satisfies the requirement
```

**解决方案**：
1. 检查依赖名称和版本号是否正确
2. 确认依赖在 PyPI 上可用
3. 尝试使用更宽松的版本约束

## 插件加载失败

### 问题：plugin.json 未生成

**症状**：
```
FileNotFoundError: plugin.json not found
```

**解决方案**：
1. 运行配置更新命令：
   ```bash
   uv sync
   uv run init-dev
   ```
2. 或使用 VSCode 启动项 "创建/更新仓库配置"

### 问题：配置信息过时

**症状**：
- 插件显示的版本号不正确
- 插件名称未更新

**解决方案**：
1. 确认已修改 `pyproject.toml`
2. 重新运行配置更新命令
3. 重新构建插件

### 问题：依赖缺失

**症状**：
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：
1. 检查 `pyproject.toml` 中是否声明了该依赖
2. 运行 `uv sync` 安装依赖
3. 重新构建插件，确保依赖被打包

## 开发环境问题

### 问题：uv 命令不可用

**症状**：
```
'uv' is not recognized as an internal or external command
```

**解决方案**：
1. 安装 uv：
   ```bash
   pip install uv
   ```
2. 或从官方网站下载安装

### 问题：init-dev 命令不可用

**症状**：
```
ERROR: Script 'init-dev' not found
```

**解决方案**：
1. 运行 `uv sync` 注册命令行入口点
2. 确认 `pyproject.toml` 中配置了 `[project.scripts]`

### 问题：VSCode 启动项无法运行

**症状**：
- 启动项列表为空
- 点击运行无反应

**解决方案**：
1. 确认 `.vscode/launch.json` 文件存在
2. 重新加载 VSCode 窗口
3. 检查 Python 扩展是否已安装

## 构建产物问题

### 问题：.pyz 文件过大

**症状**：
- 构建的 .pyz 文件体积异常大

**解决方案**：
1. 检查 `src/` 目录是否包含不必要的文件
2. 确认没有将测试文件或大型资源文件放入 `src/`
3. 使用 `.gitignore` 排除不需要的文件

### 问题：ZIP 压缩包未生成

**症状**：
- `dist/` 目录下没有 .zip 文件

**解决方案**：
1. 检查是否使用了 `--no-zip` 参数
2. 确认构建脚本执行完整
3. 查看构建日志中的错误信息

## Git 相关问题

### 问题：标签推送失败

**症状**：
```
error: failed to push some refs
```

**解决方案**：
1. 确认标签格式正确（`v*`）
2. 检查是否有权限推送标签
3. 使用 `git push origin --tags` 推送所有标签

### 问题：GitHub Actions 未触发

**症状**：
- 推送标签后没有自动构建

**解决方案**：
1. 确认标签格式为 `v*`
2. 检查 `.github/workflows/release.yml` 是否存在
3. 查看 GitHub Actions 页面的工作流状态

## 运行时问题

### 问题：插件无法读取配置

**症状**：
```
WARNING: plugin.json not found
```

**解决方案**：
1. 确认 `plugin.json` 在正确的位置
2. 检查路径计算逻辑是否正确
3. 验证 `get_runtime_config()` 的实现

### 问题：框架代码导入失败

**症状**：
```
ModuleNotFoundError: No module named 'config'
```

**解决方案**：
1. 确认 `sys.path.insert()` 的路径正确
2. 检查 `plugin_framework/` 目录是否存在
3. 验证相对路径计算是否正确

## 获取帮助

如果以上方法都无法解决问题：

1. 查看项目 Issues：检查是否有类似问题
2. 提交新 Issue：提供详细的错误信息和复现步骤
3. 查看日志：收集完整的错误日志和堆栈跟踪
