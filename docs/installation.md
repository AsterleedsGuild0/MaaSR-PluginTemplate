# 🔌 插件安装

## 安装步骤

1. 从 GitHub Release 下载插件压缩包
2. 解压到 MaaStarResonance 的 `agent/plugins/` 目录
3. 重启 MaaStarResonance

## 插件目录结构

```
agent/plugins/your_plugin/
├── plugin.json          # 插件元数据（自动生成）
├── lib/
│   └── your_plugin.pyz  # 只包含 src/ 的代码
└── deps/                # 依赖（如果有）
    └── *.whl
```

## 验证安装

安装完成后，可以通过以下方式验证：

1. 查看 MaaStarResonance 日志，确认插件已加载
2. 在插件列表中查看你的插件
3. 测试插件功能是否正常

## 故障排查

### 插件未显示

1. 确认插件目录结构正确
2. 检查 `plugin.json` 格式是否正确
3. 查看 MaaStarResonance 日志中的错误信息

### 插件加载失败

1. 验证 `pyproject.toml` 配置
2. 检查依赖是否完整
3. 确认 Python 版本兼容性（>= 3.11）
4. 查看 MaaStarResonance 日志

### 依赖缺失

1. 确认 `deps/` 目录存在
2. 检查所需的 wheel 文件是否都在
3. 验证依赖版本是否兼容

## 卸载插件

1. 关闭 MaaStarResonance
2. 删除 `agent/plugins/your_plugin/` 目录
3. 重启 MaaStarResonance

## 更新插件

1. 下载新版本的插件压缩包
2. 关闭 MaaStarResonance
3. 删除旧版本插件目录
4. 解压新版本到 `agent/plugins/` 目录
5. 重启 MaaStarResonance
